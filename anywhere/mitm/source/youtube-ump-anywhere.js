var yt_ump_b64 = "__YOUTUBE_UMP_JS_BASE64__";

// Anywhere runs the Maasea UMP engine (the pre-worker local build) inside a
// Surge environment shim. It decrypts the onesie initplayback stream with the
// key the response engine cached in $persistentStore, strips the ad placements
// and re-encrypts; on any failure the stream is passed through untouched.

function headerObject(list) {
  var o = {};
  for (var i = 0; i < list.length; i++) {
    o[list[i][0]] = list[i][1];
    o[list[i][0].toLowerCase()] = list[i][1];
  }
  return o;
}

function flag(name, fallback) {
  var v = Anywhere.params.get(name);
  if (v === undefined || v === "") return fallback;
  return v === "true";
}

async function process(ctx) {
  var result = await new Promise(function(resolve) {
    try {
      // Same fixed non-music agent as the response shim, so both engines read
      // and write the same per-platform key slot.
      globalThis.$request = {
        url: ctx.url,
        method: ctx.method,
        headers: { "user-agent": "com.google.ios.youtube" }
      };
      globalThis.$response = {
        status: ctx.status,
        headers: headerObject(ctx.headers),
        body: ctx.body
      };
      globalThis.$argument = JSON.stringify({
        captionLang: "off",
        blockUpload: flag("blockUpload", true),
        blockImmersive: flag("blockImmersive", true),
        blockShorts: flag("blockShorts", false),
        debug: false
      });
      globalThis.$persistentStore = {
        read: function(key) {
          var v = Anywhere.store.getString(key, true);
          return v === undefined ? null : v;
        },
        // Surge order: write(value, key).
        write: function(val, key) {
          try { Anywhere.store.set(key, String(val), true); }
          catch (e) { Anywhere.log.warning("[YT-UMP] store: " + e); }
          return true;
        }
      };
      globalThis.$notification = { post: function() {} };
      globalThis.$httpClient = {};
      // The engine finishes asynchronously and always ends in $done.
      globalThis.$done = function(r) { resolve(r || {}); };
      globalThis.console = { log: function(m) { Anywhere.log.info("[YT-UMP] " + m); } };

      eval(Anywhere.codec.utf8.decode(Anywhere.codec.base64.decode(yt_ump_b64)));
    } catch (e) {
      Anywhere.log.warning("[YT-UMP] error: " + (e && e.message ? e.message : String(e)).substring(0, 120));
      resolve(null);
    }
  });

  if (!result) return;
  if (result.status) {
    // Upstream answers an empty text/plain 200 here. A response script cannot
    // change headers, and an empty UMP body stalls the player, so pass the
    // stream through untouched; the request engine handles the stale-key case.
    Anywhere.log.info("[YT-UMP] left initplayback untouched");
  } else if (result.body) {
    var before = ctx.body.length;
    var changed = !sameBytes(ctx.body, result.body);
    ctx.body = result.body;
    // Release builds drop debug logs, so report the outcome at info.
    Anywhere.log.info(changed
      ? "[YT-UMP] onesie player response rewritten (" + before + " -> " + result.body.length + " bytes)"
      : "[YT-UMP] no onesie player part, stream unchanged");
  }
}

function sameBytes(a, b) {
  if (a.length !== b.length) return false;
  for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
  return true;
}
