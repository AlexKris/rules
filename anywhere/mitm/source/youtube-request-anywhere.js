var yt_request_b64 = "__YOUTUBE_REQUEST_JS_BASE64__";

// Anywhere runs the Maasea request engine (the pre-worker local build) on the
// onesie initplayback request. It compares the client's encrypted key with the
// one the response engine cached; on a mismatch it answers an empty 200 so the
// client falls back to v1/player (which the response engine cleans) and clears
// the stale key. The upstream log_event branch edits request headers, which
// Anywhere scripts cannot do, so only initplayback is routed here.

function flag(name, fallback) {
  var v = Anywhere.params.get(name);
  if (v === undefined || v === "") return fallback;
  return v === "true";
}

function process(ctx) {
  // Redirect discovery uses bodyless GETs on the same endpoint; the engine
  // would clear the cached key on those, so skip them.
  if (ctx.method === "GET" || ctx.method === "HEAD") return;
  if (!ctx.body || !ctx.body.length) return;

  var result = null;
  try {
    globalThis.$request = {
      url: ctx.url,
      method: ctx.method,
      headers: { "user-agent": "com.google.ios.youtube" },
      body: ctx.body
    };
    globalThis.$response = {};
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
        catch (e) { Anywhere.log.warning("[YT-REQ] store: " + e); }
        return true;
      }
    };
    globalThis.$notification = { post: function() {} };
    globalThis.$httpClient = {};
    globalThis.$done = function(r) { result = r || {}; };
    globalThis.console = { log: function(m) { Anywhere.log.info("[YT-REQ] " + m); } };

    eval(Anywhere.codec.utf8.decode(Anywhere.codec.base64.decode(yt_request_b64)));
  } catch (e) {
    Anywhere.log.warning("[YT-REQ] error: " + (e && e.message ? e.message : String(e)).substring(0, 120));
    return;
  }

  if (result && result.status) {
    Anywhere.log.info("[YT-REQ] key mismatch, answering empty initplayback");
    Anywhere.respond({
      status: result.status,
      headers: [["Content-Type", "application/x-protobuf"]],
      body: new Uint8Array(0)
    });
  }
}
