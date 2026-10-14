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

// The engine only inspects richItemContents. Browse responses also carry
// full-width "preview" sponsor cards one level up (root 10 -> 49399797 -> 32),
// so those are removed here before the engine runs. A card is dropped only when
// it uses one of the sponsor layouts and carries ad tracking markers.
function asciiBytes(s) {
  var b = new Uint8Array(s.length);
  for (var i = 0; i < s.length; i++) b[i] = s.charCodeAt(i);
  return b;
}

var SPONSOR_LAYOUTS = [
  "full_width_square_image_layout.eml-fe",
  "full_width_portrait_image_layout.eml-fe",
  "video_display_button_group_layout.eml-fe"
].map(asciiBytes);
var PAGEAD = asciiBytes("pagead");
var AD_MARKERS = ["googleads", "adview", "activeview"].map(asciiBytes);

function hasBytes(hay, needle) {
  var last = hay.length - needle.length;
  for (var i = hay.indexOf(needle[0]); i >= 0 && i <= last; i = hay.indexOf(needle[0], i + 1)) {
    var j = 1;
    while (j < needle.length && hay[i + j] === needle[j]) j++;
    if (j === needle.length) return true;
  }
  return false;
}

function hasAny(hay, needles) {
  for (var i = 0; i < needles.length; i++) if (hasBytes(hay, needles[i])) return true;
  return false;
}

function isSponsorCard(bytes) {
  return bytes.length >= 1024 && bytes.length < 900000
    && hasAny(bytes, SPONSOR_LAYOUTS) && hasBytes(bytes, PAGEAD) && hasAny(bytes, AD_MARKERS);
}

function stripBrowseSponsorCards(ctx) {
  if (!/\/youtubei\/v1\/browse(?:\?|$)/.test(ctx.url || "") || !ctx.body || !hasBytes(ctx.body, PAGEAD)) return;
  try {
    var pb = Anywhere.codec.protobuf;
    var root = pb.decode(ctx.body);
    var removed = 0;
    for (var i = 0; i < root.length; i++) {
      if (root[i].field !== 10 || root[i].wire !== 2) continue;
      var content = pb.decode(root[i].value);
      var contentChanged = false;
      for (var j = 0; j < content.length; j++) {
        if (content[j].field !== 49399797 || content[j].wire !== 2) continue;
        var items = pb.decode(content[j].value);
        var kept = items.filter(function(it) {
          return !(it.field === 32 && it.wire === 2 && isSponsorCard(it.value));
        });
        if (kept.length === items.length) continue;
        removed += items.length - kept.length;
        content[j] = { field: content[j].field, wire: 2, value: pb.encode(kept) };
        contentChanged = true;
      }
      if (contentChanged) root[i] = { field: root[i].field, wire: 2, value: pb.encode(content) };
    }
    if (removed) {
      ctx.body = pb.encode(root);
      Anywhere.log.info("[YT] removed " + removed + " sponsor card(s) from browse");
    }
  } catch (e) {
    // Unexpected wire data: leave the response to the engine unchanged.
  }
}

function process(ctx) {
  var result = null;
  stripBrowseSponsorCards(ctx);
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
      // Surge order: write(value, key).
      write: function(val, key) {
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
