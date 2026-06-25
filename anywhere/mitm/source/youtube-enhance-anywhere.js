var yt_init_ok = false;
var yt_proto_b64 = "__YOUTUBE_RESPONSE_JS_BASE64__";

async function process(ctx) {
  if (!yt_init_ok) {
    try {
      Anywhere.log.info("[YT] initializing protobuf engine...");

      // Surge compatibility stubs required by the vendored protobuf engine.
      globalThis.$persistentStore = {
        read: function(key) { return null; },
        write: function(key, val) {}
      };
      globalThis.$argument = "{}";
      globalThis.$done = function() {};

      eval(Anywhere.codec.utf8.decode(Anywhere.codec.base64.decode(yt_proto_b64)));
      if (typeof globalThis.__yt_or === "function") {
        yt_init_ok = true;
        Anywhere.log.info("[YT] init OK - engine ready");
      } else {
        Anywhere.log.error("[YT] init FAILED");
        return;
      }
    } catch (e) {
      Anywhere.log.error("[YT] init error: " + (e && e.message ? e.message : String(e)));
      return;
    }
  }

  try {
    var url = ctx.url;
    var handler = globalThis.__yt_or(url);
    if (!handler) return;

    handler.fromBinary(ctx.body);
    await handler.pure();

    if (handler.needProcess) {
      ctx.body = handler.toBinary();
      Anywhere.log.debug("[YT] done: " + url.substring(0, 60));
    }
  } catch (e) {
    Anywhere.log.warning("[YT] error: " + (e && e.message ? e.message : String(e)).substring(0, 120));
  }
}
