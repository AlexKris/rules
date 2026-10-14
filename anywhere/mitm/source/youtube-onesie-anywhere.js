// Onesie key gate for YouTube in Anywhere.
//
// YouTube can fetch the player response through an encrypted onesie
// initplayback request on googlevideo.com instead of v1/player. The ads in that
// path can only be stripped when the key is known, so this script:
// - captures onesie key pairs from config / log_event responses (newest first,
//   up to 4, because the client may still use an older one);
// - lets an initplayback request through only when its key is one of them, and
//   otherwise answers an empty 200 so the client falls back to v1/player, whose
//   ads the response engine removes.
// A native header-delete rule drops x-youtube-hot-hash-data on log_event so the
// server keeps sending the hot config that carries the key. Replaying log_event
// through Anywhere.http does not work: its browser TLS fingerprint makes Google
// front ends answer a fatal unexpected_message alert.

var KEY_STORE = "yt:onesie:keys";
var MAX_KEYS = 4;
// responseContext -> globalConfigGroup -> hotConfigGroup -> mediaHotConfig -> onesieHotConfig
var HOT_CONFIG_PATH = [1, 16, 7, 138536474, 146311580];
// OnesieRequest -> encryptedInnertubeRequest -> encryptedClientKey
var REQUEST_KEY_PATH = [3, 5];

function loadKeys() {
  try {
    var keys = JSON.parse(Anywhere.store.getString(KEY_STORE, true) || "[]");
    return Array.isArray(keys) ? keys.filter(function(k) {
      return k && typeof k.clientKey === "string" && typeof k.encryptKey === "string";
    }).slice(0, MAX_KEYS) : [];
  } catch (e) {
    return [];
  }
}

function lastBytesField(bytes, field) {
  var entries = Anywhere.codec.protobuf.decode(bytes);
  for (var i = entries.length - 1; i >= 0; i--) {
    if (entries[i].field === field && entries[i].wire === 2) return entries[i].value;
  }
  return null;
}

function nested(bytes, path) {
  var current = bytes;
  for (var i = 0; i < path.length && current; i++) current = lastBytesField(current, path[i]);
  return current;
}

function sameBytes(a, b) {
  if (!a || !b || a.length !== b.length) return false;
  for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
  return true;
}

function captureKeys(body) {
  try {
    var hot = nested(body, HOT_CONFIG_PATH);
    if (!hot) return;
    var client = lastBytesField(hot, 1);
    var encrypt = lastBytesField(hot, 2);
    if (!client || !client.length || !encrypt || !encrypt.length) return;
    var pair = {
      clientKey: Anywhere.codec.base64.encode(client),
      encryptKey: Anywhere.codec.base64.encode(encrypt)
    };
    var keys = loadKeys();
    if (keys.length && keys[0].clientKey === pair.clientKey && keys[0].encryptKey === pair.encryptKey) return;
    keys = keys.filter(function(k) {
      return k.clientKey !== pair.clientKey || k.encryptKey !== pair.encryptKey;
    });
    keys.unshift(pair);
    Anywhere.store.set(KEY_STORE, JSON.stringify(keys.slice(0, MAX_KEYS)), true);
    Anywhere.log.info("[YT-KEY] onesie key captured (" + Math.min(keys.length, MAX_KEYS) + " stored)");
  } catch (e) {}
}

function gateInitPlayback(ctx) {
  // Redirect discovery uses bodyless GETs on the same endpoint.
  if (ctx.method === "GET" || ctx.method === "HEAD" || !ctx.body || !ctx.body.length) return;
  var requestKey = null;
  try { requestKey = nested(ctx.body, REQUEST_KEY_PATH); } catch (e) {}
  var keys = loadKeys();
  for (var i = 0; requestKey && i < keys.length; i++) {
    try {
      if (sameBytes(requestKey, Anywhere.codec.base64.decode(keys[i].encryptKey))) {
        Anywhere.log.info("[YT-KEY] initplayback key is stored key #" + (i + 1) + ", passing");
        return;
      }
    } catch (e) {}
  }
  Anywhere.log.info(keys.length
    ? "[YT-KEY] initplayback key unknown, answering empty so the client uses v1/player"
    : "[YT-KEY] no onesie key yet, answering empty so the client uses v1/player");
  Anywhere.respond({ status: 200, headers: [["Content-Type", "text/plain"]], body: new Uint8Array(0) });
}

function process(ctx) {
  var url = String(ctx.url || "");
  if (ctx.phase === "response") {
    if (/\/youtubei\/v1\/(?:config|log_event)(?:\?|$)/.test(url) && ctx.body && ctx.body.length) captureKeys(ctx.body);
  } else if (/^https?:\/\/[\w-]+\.googlevideo\.com\/initplayback/.test(url)) {
    gateInitPlayback(ctx);
  }
}
