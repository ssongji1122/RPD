(function () {
  "use strict";

  var data = window.RPDFinalProjects || { stats: {}, projects: [] };
  var state = {
    activeId: ""
  };

  var els = {
    review: document.querySelector(".final-review"),
    layout: document.querySelector(".final-layout"),
    gallerySection: document.getElementById("finalGallerySection"),
    galleryRail: document.getElementById("finalGalleryRail"),
    detail: document.getElementById("finalDetail")
  };

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (key) {
      if (key === "className") node.className = attrs[key];
      else if (key === "textContent") node.textContent = attrs[key];
      else node.setAttribute(key, attrs[key]);
    });
    (children || []).forEach(function (child) {
      if (typeof child === "string") node.appendChild(document.createTextNode(child));
      else if (child) node.appendChild(child);
    });
    return node;
  }

  function projectNumber(project) {
    return parseInt(String(project.id).replace("project-", ""), 10) || 0;
  }

  function sortProjects(projects) {
    return projects.slice().sort(function (a, b) {
      return projectNumber(a) - projectNumber(b);
    });
  }

  function getFilteredProjects() {
    return data.projects.slice();
  }

  function getAllProjectsSorted() {
    return sortProjects(data.projects);
  }

  function getProjectById(id) {
    return data.projects.find(function (project) { return project.id === id; }) || null;
  }

  function getAdjacentProjects(project) {
    var ordered = getAllProjectsSorted();
    var index = ordered.findIndex(function (item) { return item.id === project.id; });
    return {
      prev: index > 0 ? ordered[index - 1] : null,
      next: index >= 0 && index < ordered.length - 1 ? ordered[index + 1] : null
    };
  }

  function activeIdFromUrl() {
    return location.hash ? decodeURIComponent(location.hash.slice(1)) : "";
  }

  function openProject(project) {
    if (!project) return;
    closeWebViewer();
    state.activeId = project.id;
    var targetHash = "#" + encodeURIComponent(project.id);
    if (location.hash !== targetHash) {
      location.hash = project.id;
    }
    render();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function showProjectList() {
    closeWebViewer();
    state.activeId = "";
    if (location.hash) {
      history.replaceState("", document.title, location.pathname + location.search);
    }
    render();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function bestCover(project) {
    var media = project.media || [];
    if (project.coverSrc) {
      var coverItem = media.find(function (item) { return item.src === project.coverSrc; });
      if (coverItem) return coverItem;
      return { type: "image", src: project.coverSrc };
    }
    var render = media.find(function (item) {
      return item.role !== "process" && item.type === "image";
    });
    if (render) return render;
    var video = media.find(function (item) { return item.type === "video"; });
    if (video) return video;
    return media[0] || null;
  }

  function getRenderMedia(project) {
    return project.media || [];
  }

  function renderGalleryRail(projects) {
    var ordered = sortProjects(projects);
    if (!els.galleryRail) return ordered.length;

    els.galleryRail.textContent = "";
    if (!ordered.length) {
      els.galleryRail.appendChild(el("div", {
        className: "final-empty-state",
        textContent: "조건에 맞는 작품이 없습니다."
      }));
      return 0;
    }

    ordered.forEach(function (project, index) {
      var cover = bestCover(project);
      var panel = el("a", {
        className: "final-gallery-panel",
        href: "#" + encodeURIComponent(project.id),
        role: "listitem",
        "data-project-id": project.id,
        "aria-label": project.code + " 상세 보기"
      });
      var frame = el("div", { className: "final-gallery-panel-frame" });
      if (cover) {
        frame.appendChild(el("img", {
          src: cover.src,
          alt: "",
          loading: index < 10 ? "eager" : "lazy",
          draggable: "false"
        }));
      } else {
        frame.appendChild(el("div", { className: "final-card-empty", textContent: "—" }));
      }
      panel.appendChild(frame);
      els.galleryRail.appendChild(panel);
    });

    return ordered.length;
  }

  function editorialSpan(index, item) {
    if (item.type === "video") return 2;
    return index % 3 === 1 ? 2 : 1;
  }

  function renderEditorialMediaCell(item, project, index) {
    var span = editorialSpan(index, item);
    var cell = el("figure", {
      className: "final-editorial-cell is-media is-span-" + span
    });
    var mediaWrap = el("div", { className: "final-editorial-media" });

    if (item.type === "video" && item.videoSrc) {
      mediaWrap.appendChild(el("video", {
        src: item.videoSrc,
        poster: item.src,
        controls: "",
        playsinline: "",
        preload: "metadata",
        "aria-label": project.code + " 영상 " + (index + 1)
      }));
    } else {
      mediaWrap.appendChild(el("img", {
        src: item.src,
        alt: project.code + " 장면 " + (index + 1),
        loading: "lazy"
      }));
    }

    cell.appendChild(mediaWrap);
    return cell;
  }

  function renderHeroMedia(cover, project) {
    var cell = el("div", { className: "final-editorial-cell is-hero-media is-span-2" });
    var mediaWrap = el("div", { className: "final-editorial-media is-hero" });

    if (!cover) {
      mediaWrap.appendChild(el("div", { className: "final-card-empty", textContent: "—" }));
    } else if (cover.type === "video" && cover.videoSrc) {
      mediaWrap.appendChild(el("video", {
        src: cover.videoSrc,
        poster: cover.src,
        controls: "",
        playsinline: "",
        preload: "metadata",
        "aria-label": project.code + " 대표 영상"
      }));
    } else {
      mediaWrap.appendChild(el("img", {
        src: cover.src,
        alt: project.code + " 대표 이미지",
        loading: "eager"
      }));
    }

    cell.appendChild(mediaWrap);
    return cell;
  }

  function getEmbeddableLinks(project) {
    return (project.links || []).filter(isEmbeddableLink);
  }

  function getExternalLinks(project) {
    return (project.links || []).filter(function (link) {
      return !isEmbeddableLink(link);
    });
  }

  function isEmbeddableLink(link) {
    return link.kind === "웹페이지" || link.kind === "작품 페이지";
  }

  function normalizeEmbedUrl(url) {
    if (!url) return "";
    try {
      var parsed = new URL(url);
      if (parsed.protocol !== "http:" && parsed.protocol !== "https:") return "";
      if (parsed.protocol === "http:") {
        parsed.protocol = "https:";
      }
      return parsed.href;
    } catch (error) {
      return "";
    }
  }

  function getEmbedMode(url) {
    var normalized = normalizeEmbedUrl(url);
    if (!normalized) return { mode: "external", url: url || "" };
    var host = new URL(normalized).hostname.toLowerCase();
    var blocked = /(^|\.)notion\.(so|site)$/.test(host)
      || host === "docs.google.com"
      || host === "canva.link"
      || host.endsWith("behance.net")
      || host.endsWith("mixboard.google.com")
      || host.endsWith("21st.dev")
      || host.endsWith("google.com");
    if (blocked) return { mode: "external", url: normalized };
    return { mode: "iframe", url: normalized };
  }

  function createWebIframe(url, title) {
    return el("iframe", {
      src: url,
      title: title,
      referrerpolicy: "no-referrer-when-downgrade",
      allow: "autoplay; fullscreen; clipboard-read; clipboard-write",
      allowfullscreen: ""
    });
  }

  function closeWebViewer() {
    var existing = document.querySelector(".final-web-viewer");
    if (existing) existing.remove();
    document.body.classList.remove("final-web-viewer-open");
  }

  function openWebViewer(url, title) {
    closeWebViewer();
    var viewer = el("div", {
      className: "final-web-viewer",
      role: "dialog",
      "aria-modal": "true",
      "aria-label": title || "웹페이지 미리보기"
    });
    var toolbar = el("div", { className: "final-web-viewer-bar" }, [
      el("strong", { textContent: title || "웹페이지" }),
      el("div", { className: "final-web-viewer-actions" }, [
        el("a", {
          className: "final-web-embed-open",
          href: url,
          target: "_blank",
          rel: "noopener",
          textContent: "새 탭에서 열기"
        }),
        el("button", {
          className: "final-web-viewer-close",
          type: "button",
          textContent: "닫기"
        })
      ])
    ]);
    var frame = el("div", { className: "final-web-viewer-frame" });
    frame.appendChild(createWebIframe(url, title || "웹페이지 전체 화면"));
    viewer.appendChild(toolbar);
    viewer.appendChild(frame);
    viewer.querySelector(".final-web-viewer-close").addEventListener("click", closeWebViewer);
    viewer.addEventListener("click", function (event) {
      if (event.target === viewer) closeWebViewer();
    });
    document.body.appendChild(viewer);
    document.body.classList.add("final-web-viewer-open");
  }

  function renderWebLaunchCell(link, project, embedUrl) {
    var cover = bestCover(project);
    var cell = el("section", {
      className: "final-editorial-cell is-span-4 is-web-launch",
      "aria-label": link.label || project.code + " 웹페이지"
    });
    var panel = el("a", {
      className: "final-web-launch-panel",
      href: embedUrl,
      target: "_blank",
      rel: "noopener"
    });
    if (cover) {
      panel.appendChild(el("img", {
        className: "final-web-launch-cover",
        src: cover.src,
        alt: "",
        loading: "lazy"
      }));
    }
    panel.appendChild(el("div", { className: "final-web-launch-copy" }, [
      el("strong", { textContent: link.label || project.code }),
      el("b", { textContent: "열기" })
    ]));
    cell.appendChild(panel);
    return cell;
  }

  function renderWebEmbedCell(link, project, index) {
    var policy = getEmbedMode(link.url);
    var embedUrl = policy.url;
    if (!embedUrl) return null;

    if (policy.mode === "external") {
      return renderWebLaunchCell(link, project, embedUrl);
    }

    var title = (link.label || project.code) + " 웹페이지 미리보기 " + (index + 1);
    var cell = el("section", {
      className: "final-editorial-cell is-span-4 is-web-embed",
      "aria-label": link.label || project.code + " 웹페이지"
    });
    var actions = el("div", { className: "final-web-embed-actions" }, [
      el("button", {
        className: "final-web-embed-open is-inline",
        type: "button",
        textContent: "전체 화면"
      }),
      el("a", {
        className: "final-web-embed-open",
        href: embedUrl,
        target: "_blank",
        rel: "noopener",
        textContent: "새 탭에서 열기"
      })
    ]);
    var head = el("div", { className: "final-web-embed-head" }, [
      el("div", { className: "final-web-embed-title" }, [
        el("strong", { textContent: link.label || project.code })
      ]),
      actions
    ]);
    var frame = el("div", { className: "final-web-embed-frame" });
    var iframe = createWebIframe(embedUrl, title);
    frame.appendChild(iframe);
    actions.querySelector("button").addEventListener("click", function () {
      openWebViewer(embedUrl, link.label || project.code + " 웹");
    });
    frame.addEventListener("click", function () {
      iframe.focus();
    });
    cell.appendChild(head);
    cell.appendChild(frame);
    return cell;
  }

  function renderWebEmbeds(project) {
    return getEmbeddableLinks(project).map(function (link, index) {
      return renderWebEmbedCell(link, project, index);
    }).filter(Boolean);
  }

  function renderDetailLinks(project) {
    var links = getExternalLinks(project);
    if (!links.length) return null;
    var list = el("div", { className: "final-detail-link-stack" });
    links.forEach(function (link) {
      list.appendChild(el("a", {
        className: "final-link",
        href: link.url,
        target: "_blank",
        rel: "noopener"
      }, [
        el("span", { textContent: link.label }),
        el("b", { textContent: "열기" })
      ]));
    });
    return list;
  }

  function renderDetailNavRow(project, adjacent) {
    var row = el("div", { className: "final-editorial-cell is-span-4 is-detail-nav" });
    var prev = adjacent.prev
      ? el("button", {
        className: "final-detail-step",
        type: "button",
        textContent: "← " + adjacent.prev.code
      })
      : el("span", { className: "final-detail-step is-disabled", textContent: "← 이전 작품" });
    if (adjacent.prev) {
      prev.addEventListener("click", function () { openProject(adjacent.prev); });
    }

    var next = adjacent.next
      ? el("button", {
        className: "final-detail-step",
        type: "button",
        textContent: adjacent.next.code + " →"
      })
      : el("span", { className: "final-detail-step is-disabled", textContent: "다음 작품 →" });
    if (adjacent.next) {
      next.addEventListener("click", function () { openProject(adjacent.next); });
    }

    row.appendChild(prev);
    row.appendChild(next);
    return row;
  }

  function renderDetail(project) {
    els.detail.textContent = "";
    if (!project) return;

    var cover = bestCover(project);
    var coverSrc = cover ? cover.src : "";
    var remainingMedia = getRenderMedia(project).filter(function (item) {
      return item.src !== coverSrc;
    });
    var adjacent = getAdjacentProjects(project);

    var sheet = el("article", { className: "final-detail-sheet" });
    var back = el("button", { className: "final-detail-back", type: "button", textContent: "목록으로" });
    back.addEventListener("click", showProjectList);
    sheet.appendChild(el("div", { className: "final-detail-nav" }, [
      back,
      el("span", { textContent: project.code })
    ]));

    var grid = el("div", { className: "final-editorial-grid" });
    grid.appendChild(renderHeroMedia(cover, project));

    var titleCell = el("div", { className: "final-editorial-cell is-hero-copy" }, [
      el("h2", { textContent: project.title })
    ]);
    grid.appendChild(titleCell);

    var links = renderDetailLinks(project);
    if (links) {
      grid.appendChild(el("div", { className: "final-editorial-cell is-span-2 is-hero-meta" }, [links]));
    }

    remainingMedia.forEach(function (item, index) {
      grid.appendChild(renderEditorialMediaCell(item, project, index));
    });

    renderWebEmbeds(project).forEach(function (embedCell) {
      grid.appendChild(embedCell);
    });

    grid.appendChild(renderDetailNavRow(project, adjacent));
    sheet.appendChild(grid);
    els.detail.appendChild(sheet);
  }

  function render() {
    var projects = getFilteredProjects();
    var activeProject = getProjectById(state.activeId);
    var isDetailView = Boolean(activeProject);

    if (els.review) els.review.dataset.view = isDetailView ? "detail" : "list";
    if (els.layout) els.layout.dataset.view = isDetailView ? "detail" : "list";

    if (isDetailView) {
      renderDetail(activeProject);
      return;
    }

    var galleryCount = renderGalleryRail(projects);
    if (els.gallerySection) els.gallerySection.hidden = galleryCount === 0;
  }

  function hydrateFromUrl() {
    state.activeId = activeIdFromUrl();
  }

  function onRouteChange() {
    hydrateFromUrl();
    render();
    if (state.activeId) {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  hydrateFromUrl();
  if (els.galleryRail) {
    els.galleryRail.addEventListener("click", function (event) {
      var panel = event.target.closest(".final-gallery-panel");
      if (!panel) return;
      var project = getProjectById(panel.getAttribute("data-project-id") || "");
      if (project) openProject(project);
    });
  }
  window.addEventListener("hashchange", onRouteChange);
  window.addEventListener("popstate", onRouteChange);
  window.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeWebViewer();
  });
  render();
})();
