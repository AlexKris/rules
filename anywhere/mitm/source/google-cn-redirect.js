function process(ctx) {
  if (ctx.phase !== "request" || !ctx.url) return;

  var original = String(ctx.url);
  var target = original.replace(
    /^https?:\/\/(?:www\.)?(?:g|google)\.cn(?=[:\/?#]|$)/i,
    "https://www.google.com"
  );

  if (target === original) {
    target = original.replace(
      /^https?:\/\/(?:ditu|maps)\.google\.cn(?=[:\/?#]|$)/i,
      "https://maps.google.com"
    );
  }

  if (target === original) return;

  Anywhere.respond({
    status: 307,
    headers: [["Location", target]],
    body: ""
  });
}
