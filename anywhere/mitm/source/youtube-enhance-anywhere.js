var yt_engine_b64 = "__YOUTUBE_RESPONSE_JS_BASE64__";

// Anywhere runs the unmodified Maasea engine inside a Surge environment shim.
// The engine reads $request / $response, keeps its ad cache in $persistentStore,
// and hands the rewritten body back through $done.

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

function process(ctx) {
  var result = null;
  try {
    // Only the response is available here. The engine reads the request
    // user-agent solely to pick a per-platform state key, so a fixed
    // non-music agent is enough.
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
      write: function(key, val) {
        try { Anywhere.store.set(key, String(val), true); }
        catch (e) { Anywhere.log.warning("[YT] store: " + e); }
        return true;
      }
    };
    globalThis.$notification = { post: function() {} };
    globalThis.$httpClient = {};
    globalThis.$done = function(r) { result = r || {}; };
    globalThis.console = { log: function(m) { Anywhere.log.info("[YT] " + m); } };

    eval(Anywhere.codec.utf8.decode(Anywhere.codec.base64.decode(yt_engine_b64)));
  } catch (e) {
    Anywhere.log.warning("[YT] error: " + (e && e.message ? e.message : String(e)).substring(0, 120));
    return;
  }

  if (result && result.body) {
    ctx.body = result.body;
    Anywhere.log.debug("[YT] done: " + ctx.url.substring(0, 60));
  }
}
