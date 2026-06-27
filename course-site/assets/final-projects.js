(function () {
  "use strict";

  var data = window.RPDFinalProjects || { stats: {}, projects: [] };
  var CATEGORY_OPTIONS = [
    { id: "all", label: "전체" },
    { id: "character", label: "캐릭터형" },
    { id: "industrial", label: "산업형" },
    { id: "vehicle", label: "차량형" },
    { id: "web", label: "웹페이지형" }
  ];
  var CATEGORY_LABELS = {
    character: "캐릭터형",
    industrial: "산업형",
    vehicle: "차량형",
    web: "웹페이지형"
  };

  var state = {
    query: "",
    category: "all",
    activeId: ""
  };

  var els = {
    review: document.querySelector(".final-review"),
    layout: document.querySelector(".final-layout"),
    stats: document.getElementById("finalStats"),
    search: document.getElementById("finalSearch"),
    filterChips: document.getElementById("finalFilterChips"),
    gallerySection: document.getElementById("finalGallerySection"),
    galleryRail: document.getElementById("finalGalleryRail"),
    galleryMeta: document.getElementById("finalGalleryMeta"),
    galleryMetaIndex: document.getElementById("finalGalleryMetaIndex"),
    galleryMetaCaption: document.getElementById("finalGalleryMetaCaption"),
    count: document.getElementById("finalResultCount"),
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

  function enrichProject(project) {
    return {
      project: project,
      category: inferCategory(project),
      tags: getProjectTags(project)
    };
  }

  function inferCategory(project) {
    var links = project.links || [];
    var linkText = links.map(function (item) {
      return [item.label, item.url, item.kind].join(" ");
    }).join(" ").toLowerCase();

    if (links.some(function (item) {
      return item.kind === "웹페이지" || item.kind === "작품 페이지";
    })) {
      return "web";
    }
    if (/tesla|vehicle|car|automotive|차량/.test(linkText)) {
      return "vehicle";
    }
    var imageCount = (project.media || []).filter(function (item) {
      return item.type === "image";
    }).length;
    if (imageCount >= 4) return "character";
    return "industrial";
  }

  function getProjectTags(project) {
    var tags = [];
    var imageCount = (project.media || []).filter(function (item) {
      return item.type === "image";
    }).length;
    var videoCount = (project.videos || []).length;
    var links = project.links || [];

    if (imageCount) tags.push("Render");
    if (videoCount) tags.push("MP4");
    if (links.some(function (item) {
      return item.kind === "웹페이지" || item.kind === "작품 페이지";
    })) {
      tags.push("Web");
    }
    if (links.some(function (item) { return item.kind === "Behance"; })) {
      tags.push("Behance");
    }
    if (links.some(function (item) { return item.kind === "발표 자료"; })) {
      tags.push("Deck");
    }
    if (!tags.length) tags.push("Archive");
    return tags;
  }

  function addStat(label, value) {
    return el("div", { className: "final-stat" }, [
      el("dt", { textContent: label }),
      el("dd", { textContent: String(value) })
    ]);
  }

  function renderStats() {
    if (!els.stats) return;
    els.stats.textContent = "";
    els.stats.appendChild(addStat("작품", data.stats.works || 0));
    els.stats.appendChild(addStat("영상", data.stats.videos || 0));
    els.stats.appendChild(addStat("링크", data.stats.links || 0));
    els.stats.appendChild(addStat("형식", data.stats.format || "갤러리"));
  }

  function renderFilterChips() {
    if (!els.filterChips) return;
    els.filterChips.textContent = "";
    CATEGORY_OPTIONS.forEach(function (option) {
      var btn = el("button", {
        className: "rpd-filter-chip" + (state.category === option.id ? " is-active" : ""),
        type: "button",
        "data-category": option.id,
        textContent: option.label
      });
      btn.addEventListener("click", function () {
        state.category = option.id;
        renderFilterChips();
        render();
      });
      els.filterChips.appendChild(btn);
    });
  }

  function projectSearchText(project) {
    var meta = enrichProject(project);
    return [
      project.code,
      project.title,
      meta.category,
      CATEGORY_LABELS[meta.category],
      meta.tags.join(" "),
      "RPD 2026",
      "Week 15",
      (project.links || []).map(function (item) { return item.label; }).join(" ")
    ].join(" ").toLowerCase();
  }

  function getFilteredProjects() {
    var query = state.query.trim().toLowerCase();
    return data.projects.filter(function (project) {
      var meta = enrichProject(project);
      if (state.category !== "all" && meta.category !== state.category) return false;
      if (query && projectSearchText(project).indexOf(query) === -1) return false;
      return true;
    });
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
    return (project.media || []).filter(function (item) {
      return item.role !== "process";
    });
  }

  function getProcessMedia(project) {
    return (project.media || []).filter(function (item) {
      return item.role === "process";
    });
  }

  function getProjectMeta(project) {
    var parts = [];
    var renderCount = getRenderMedia(project).length;
    if (renderCount) parts.push("미리보기 " + renderCount + "장");
    if ((project.videos || []).length) parts.push("영상 " + project.videos.length + "개");
    if ((project.links || []).length) parts.push("링크 " + project.links.length + "개");
    return parts.length ? parts.join(" · ") : "이미지 기록";
  }

  function setGalleryMeta(project, index, isIdle) {
    if (!els.galleryMetaIndex || !els.galleryMetaCaption) return;
    if (!project) {
      els.galleryMetaIndex.textContent = "( — )";
      els.galleryMetaCaption.textContent = "커서를 올리면 작품이 확대됩니다";
      if (els.galleryMeta) els.galleryMeta.classList.add("is-idle");
      return;
    }
    els.galleryMetaIndex.textContent = "( " + String(index + 1).padStart(2, "0") + " )";
    els.galleryMetaCaption.textContent = project.code + " · " + getProjectTags(project).join(" · ");
    if (els.galleryMeta) els.galleryMeta.classList.toggle("is-idle", Boolean(isIdle));
  }

  function bindGalleryPanelMeta(panel, project, index) {
    function showMeta() {
      setGalleryMeta(project, index, false);
    }
    function resetMeta() {
      if (!els.galleryRail || !els.galleryRail.matches(":hover")) {
        setGalleryMeta(null, 0, true);
      }
    }
    panel.addEventListener("mouseenter", showMeta);
    panel.addEventListener("focus", showMeta);
    panel.addEventListener("mouseleave", resetMeta);
    panel.addEventListener("blur", resetMeta);
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
      panel.appendChild(el("span", {
        className: "final-gallery-panel-index",
        textContent: String(index + 1).padStart(2, "0")
      }));
      bindGalleryPanelMeta(panel, project, index);
      els.galleryRail.appendChild(panel);
    });

    setGalleryMeta(null, 0, true);
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
    cell.appendChild(el("figcaption", { textContent: (item.type === "video" ? "영상" : "렌더") + " " + String(index + 1).padStart(2, "0") }));
    return cell;
  }

  function renderHeroMedia(cover, project) {
    var cell = el("div", { className: "final-editorial-cell is-hero-media is-span-2" });
    var mediaWrap = el("div", { className: "final-editorial-media is-hero" });

    if (!cover) {
      mediaWrap.appendChild(el("div", { className: "final-card-empty", textContent: "미리보기 없음" }));
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

  function renderProcessFold(project) {
    var items = getProcessMedia(project);
    if (!items.length) return null;
    var grid = el("div", { className: "final-process-grid" });
    items.forEach(function (item, index) {
      grid.appendChild(el("figure", { className: "final-process-card" }, [
        el("img", {
          src: item.src,
          alt: project.code + " 제작 메모 " + (index + 1),
          loading: "lazy"
        }),
        el("figcaption", { textContent: "메모 " + String(index + 1).padStart(2, "0") })
      ]));
    });
    var fold = el("details", { className: "final-process-fold" }, [
      el("summary", { textContent: "AI · 제작 메모 (" + items.length + ")" }),
      grid
    ]);
    return el("div", { className: "final-editorial-cell is-span-4 is-process" }, [fold]);
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
      el("span", { className: "final-web-embed-kind", textContent: link.kind || "웹페이지" }),
      el("strong", { textContent: link.label || project.code + " 웹" }),
      el("b", { textContent: "웹페이지 열기 →" })
    ]));
    cell.appendChild(panel);
    cell.appendChild(el("p", {
      className: "final-web-embed-note",
      textContent: "이 페이지는 보안 정책상 미리보기 임베드가 불가합니다. 버튼을 누르면 새 탭에서 열립니다."
    }));
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
        el("span", { className: "final-web-embed-kind", textContent: link.kind || "웹페이지" }),
        el("strong", { textContent: link.label || project.code + " 웹" })
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
    cell.appendChild(el("p", {
      className: "final-web-embed-note",
      textContent: "미리보기에서 바로 클릭·탐색할 수 있습니다. 더 넓게 보려면 전체 화면을 누르세요."
    }));
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
    row.appendChild(el("p", {
      className: "final-detail-nav-copy",
      textContent: getProjectMeta(project) + "를 기록한 Week 15 최종 결과물입니다."
    }));
    row.appendChild(next);
    return row;
  }

  function renderDetail(project) {
    els.detail.textContent = "";
    if (!project) return;

    var meta = enrichProject(project);
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
      el("p", { className: "final-detail-kicker", textContent: "RPD 2026 · Week 15" }),
      el("h2", { textContent: project.title }),
      el("p", { className: "final-editorial-sub", textContent: CATEGORY_LABELS[meta.category] || meta.category }),
      el("div", { className: "final-detail-tags" }, meta.tags.map(function (tag) {
        return el("span", { className: "final-chip", textContent: tag });
      }))
    ]);
    grid.appendChild(titleCell);

    var metaCell = el("div", { className: "final-editorial-cell is-hero-meta" }, [
      el("dl", { className: "final-editorial-meta-list" }, [
        el("div", {}, [
          el("dt", { textContent: "기록" }),
          el("dd", { textContent: getProjectMeta(project) })
        ]),
        el("div", {}, [
          el("dt", { textContent: "유형" }),
          el("dd", { textContent: CATEGORY_LABELS[meta.category] || meta.category })
        ])
      ])
    ]);
    var links = renderDetailLinks(project);
    if (links) metaCell.appendChild(links);
    grid.appendChild(metaCell);

    remainingMedia.forEach(function (item, index) {
      grid.appendChild(renderEditorialMediaCell(item, project, index));
    });

    renderWebEmbeds(project).forEach(function (embedCell) {
      grid.appendChild(embedCell);
    });

    var processFold = renderProcessFold(project);
    if (processFold) grid.appendChild(processFold);

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
    if (els.count) els.count.textContent = galleryCount + " works";
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
  renderStats();
  renderFilterChips();
  if (els.search) {
    els.search.addEventListener("input", function () {
      state.query = els.search.value || "";
      render();
    });
  }
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
