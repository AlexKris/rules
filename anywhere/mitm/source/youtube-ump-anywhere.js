var yt_ump_b64 = "__YOUTUBE_UMP_JS_BASE64__";

// Anywhere runs the Maasea UMP engine (the pre-worker local build) on the
// onesie initplayback response. It decrypts the embedded player response with
// a key captured by youtube-onesie-anywhere.js, strips the ad placements and
// re-encrypts. Each stored key is tried newest first; if none works the stream
// passes through untouched and a key refresh is requested.

var KEY_STORE = "yt:onesie:keys";
var REFRESH_STORE = "yt:onesie:refresh";

function loadKeys() {
  try {
    var keys = JSON.parse(Anywhere.store.getString(KEY_STORE, true) || "[]");
    return Array.isArray(keys) ? keys.slice(0, 4) : [];
  } catch (e) {
    return [];
  }
}

function sameBytes(a, b) {
  if (a.length !== b.length) return false;
  for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
  return true;
}

function runEngine(ctx, pair, errors) {
  return new Promise(function(resolve) {
    try {
      globalThis.$request = {
        url: ctx.url,
        method: ctx.method,
        headers: { "user-agent": "com.google.ios.youtube" }
      };
      globalThis.$response = { status: ctx.status, headers: {}, body: ctx.body };
      globalThis.$argument = "{}";
      globalThis.$persistentStore = {
        read: function(key) {
          return key === "YouTubeConfig" ? JSON.stringify({ youtube: pair, youtubeMusic: pair }) : null;
        },
        write: function() { return true; }
      };
      globalThis.$notification = { post: function() {} };
      globalThis.$httpClient = {};
      // Success hands back { body }; the engine's failure path adds a status.
      globalThis.$done = function(r) {
        var v = r && r.response ? r.response : (r || {});
        resolve(!v.status && v.body instanceof Uint8Array && v.body.length ? v.body : null);
      };
      globalThis.console = { log: function(m) { errors.push(String(m)); } };

      eval(Anywhere.codec.utf8.decode(Anywhere.codec.base64.decode(yt_ump_b64)));
    } catch (e) {
      errors.push(e && e.message ? e.message : String(e));
      resolve(null);
    }
  });
}

async function process(ctx) {
  if (!ctx.body || !ctx.body.length) return;
  var keys = loadKeys();
  var errors = [];
  for (var i = 0; i < keys.length; i++) {
    var output = await runEngine(ctx, keys[i], errors);
    if (!output) continue;
    var before = ctx.body.length;
    var changed = !sameBytes(ctx.body, output);
    ctx.body = output;
    Anywhere.log.info(changed
      ? "[YT-UMP] onesie player response rewritten with key #" + (i + 1) + " (" + before + " -> " + output.length + " bytes)"
      : "[YT-UMP] no onesie player part, stream unchanged");
    return;
  }
  try { Anywhere.store.set(REFRESH_STORE, "1", true); } catch (e) {}
  Anywhere.log.info("[YT-UMP] " + (keys.length ? "no stored key decrypts this stream" : "no onesie key yet")
    + ", passing it through" + (errors.length ? " (" + errors[errors.length - 1].substring(0, 80) + ")" : ""));
}
