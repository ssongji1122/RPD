(function () {
  "use strict";

  function escapeAttr(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function previewFor(item) {
    var source = String(item.preview_url || item.url || "");
    var original = String(item.url || source);
    var url;
    try {
      url = new URL(source, window.location.href);
    } catch (_) {
      return null;
    }
    var host = url.hostname.replace(/^www\./, "");
    var id = "";
    if (host === "youtu.be") {
      id = url.pathname.split("/").filter(Boolean)[0] || "";
    } else if (host === "youtube.com" || host === "m.youtube.com" || host === "youtube-nocookie.com") {
      if (url.pathname === "/watch") id = url.searchParams.get("v") || "";
      else {
        var match = url.pathname.match(/^\/(?:embed|shorts|live)\/([^/]+)/);
        id = match ? match[1] : "";
      }
    }
    if (/^[A-Za-z0-9_-]{11}$/.test(id)) {
      return {
        kind: "iframe",
        provider: "YouTube",
        original: original,
        src: "https://www.youtube-nocookie.com/embed/" + id + "?rel=0",
      };
    }
    if (/\.(?:mp4|webm|mov|m4v)(?:$|[?#])/i.test(url.toString())) {
      return { kind: "video", provider: "Video", original: original, src: url.toString() };
    }
    return null;
  }

  function render(item) {
    var preview = previewFor(item);
    var title = String(item.title || "영상");
    if (!preview) {
      return '<a class="doc-link" href="' + escapeAttr(item.url) + '" target="_blank" rel="noopener noreferrer">' +
        '<span class="doc-link-main">' + escapeAttr(title) + ' ↗</span></a>';
    }
    var media = preview.kind === "iframe"
      ? '<iframe src="' + escapeAttr(preview.src) + '" title="' + escapeAttr(title) + ' 영상 미리보기" loading="lazy" tabindex="-1" aria-hidden="true" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
      : '<video src="' + escapeAttr(preview.src) + '" preload="metadata" muted playsinline tabindex="-1" aria-hidden="true"></video>';
    return '<article class="source-video-preview">' +
      '<div class="source-video-preview-media">' + media +
        '<a class="source-video-preview-hit" href="' + escapeAttr(preview.original) + '" target="_blank" rel="noopener noreferrer" aria-label="' + escapeAttr(title) + ' 원본 영상 열기"></a>' +
      '</div>' +
      '<div class="source-video-preview-meta">' +
        '<a href="' + escapeAttr(preview.original) + '" target="_blank" rel="noopener noreferrer">' + escapeAttr(title) + '</a>' +
        (item.description ? '<p>' + escapeAttr(item.description) + '</p>' : '') +
        '<span>' + preview.provider + ' · 미리보기 선택 시 원본 영상 열기</span>' +
      '</div>' +
    '</article>';
  }

  window.RPDVideoPreview = { previewFor: previewFor, render: render };
})();
