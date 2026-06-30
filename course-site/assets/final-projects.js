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
    galleryStage: document.getElementById("finalGalleryStage"),
    galleryRail: document.getElementById("finalGalleryRail"),
    galleryMetaHost: document.getElementById("finalGalleryMetaHost"),
    galleryMeta: document.getElementById("finalGalleryMeta"),
    galleryMetaIndex: document.getElementById("finalGalleryMetaIndex"),
    galleryMetaCaption: document.getElementById("finalGalleryMetaCaption"),
    galleryFootnote: document.getElementById("finalGalleryFootnote"),
    galleryBack: document.getElementById("finalGalleryBack"),
    galleryToolsToggle: document.getElementById("finalGalleryToolsToggle"),
    galleryToolsPanel: document.getElementById("finalGalleryToolsPanel"),
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
    var filterWrap = els.filterChips.closest(".final-filter-wrap");
    if (filterWrap) filterWrap.hidden = true;
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

  var galleryActivePanel = null;

  function setGalleryMeta(project, index) {
    if (!els.galleryMetaIndex || !els.galleryMetaCaption || !els.galleryMeta) return;
    if (!project) {
      els.galleryMeta.hidden = true;
      return;
    }
    var number = String(index + 1).padStart(2, "0");
    els.galleryMetaIndex.textContent = "(" + number + ")";
    els.galleryMetaCaption.textContent = "PROJECT " + number + "\nRPD 2026 FINAL\nARCHIVE";
    els.galleryMeta.hidden = false;
  }

  function positionGalleryMeta(panel) {
    if (!panel || !els.galleryMeta || !els.galleryMetaHost) return;
    var hostRect = els.galleryMetaHost.getBoundingClientRect();
    var panelRect = panel.getBoundingClientRect();
    var metaWidth = Math.min(180, hostRect.width);
    var maxLeft = Math.max(0, hostRect.width - metaWidth);
    var left = Math.max(0, Math.min(maxLeft, panelRect.left - hostRect.left));
    els.galleryMeta.style.transform = "translateX(" + left + "px)";
  }

  function setGalleryActivePanel(panel, project, index) {
    if (galleryActivePanel && galleryActivePanel !== panel) {
      galleryActivePanel.classList.remove("is-active");
    }
    galleryActivePanel = panel || null;
    if (panel) {
      panel.classList.add("is-active");
      setGalleryMeta(project, index);
      positionGalleryMeta(panel);
      window.requestAnimationFrame(function () {
        positionGalleryMeta(panel);
      });
      window.setTimeout(function () {
        positionGalleryMeta(panel);
      }, 220);
    } else {
      setGalleryMeta(null, 0);
    }
  }

  function bindGalleryPanelMeta(panel, project, index) {
    function showMeta() {
      setGalleryActivePanel(panel, project, index);
    }
    function resetMeta() {
      if (!els.galleryRail || els.galleryRail.matches(":hover")) return;
      if (galleryActivePanel) galleryActivePanel.classList.remove("is-active");
      galleryActivePanel = null;
      setGalleryMeta(null, 0);
    }
    panel.addEventListener("mouseenter", showMeta);
    panel.addEventListener("focus", showMeta);
    panel.addEventListener("mouseleave", resetMeta);
    panel.addEventListener("blur", resetMeta);
  }

  function updateGalleryFootnote(count) {
    if (!els.galleryFootnote) return;
    var stats = data.stats || {};
    var works = count != null ? count : (stats.works || 0);
    els.galleryFootnote.textContent = "FINAL ARCHIVE · " + works + " WORKS";
  }

  function galleryCardClass(project, index) {
    var meta = enrichProject(project);
    var classes = ["final-gallery-panel", "is-category-" + meta.category];
    if (index === 0 || index % 11 === 0) {
      classes.push("is-featured");
    } else if (index % 7 === 4 || index % 7 === 6) {
      classes.push("is-wide");
    } else if (index % 5 === 3) {
      classes.push("is-tall");
    }
    return classes.join(" ");
  }

  function toggleGalleryTools(forceOpen) {
    if (!els.galleryToolsPanel || !els.galleryToolsToggle) return;
    var open = typeof forceOpen === "boolean"
      ? forceOpen
      : els.galleryToolsPanel.hidden;
    els.galleryToolsPanel.hidden = !open;
    els.galleryToolsToggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (open && els.search) els.search.focus();
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
      var meta = enrichProject(project);
      var label = CATEGORY_LABELS[meta.category] || "작품";
      var panel = el("a", {
        className: galleryCardClass(project, index),
        href: "#" + encodeURIComponent(project.id),
        role: "listitem",
        "data-project-id": project.id,
        "aria-label": project.code + " " + label + " " + getProjectMeta(project) + " 상세 보기"
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
      bindGalleryPanelMeta(panel, project, index);
      els.galleryRail.appendChild(panel);
    });

    galleryActivePanel = null;
    if (ordered.length) {
      var firstPanel = els.galleryRail.querySelector(".final-gallery-panel");
      if (firstPanel) setGalleryActivePanel(firstPanel, ordered[0], 0);
    } else {
      setGalleryMeta(null, 0);
    }
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

  function orderRenderMedia(project) {
    var media = getRenderMedia(project);
    var cover = bestCover(project);
    var coverSrc = cover ? cover.src : "";
    if (!coverSrc) return media;
    var coverItem = media.find(function (item) { return item.src === coverSrc; });
    var rest = media.filter(function (item) { return item.src !== coverSrc; });
    return coverItem ? [coverItem].concat(rest) : media;
  }

  function setMainMedia(container, item, project) {
    container.textContent = "";
    if (item.type === "video" && item.videoSrc) {
      container.appendChild(el("video", {
        src: item.videoSrc,
        poster: item.src,
        controls: "",
        playsinline: "",
        preload: "metadata",
        "aria-label": project.code + " 영상"
      }));
      return;
    }
    container.appendChild(el("img", {
      src: item.src,
      alt: project.code + " 작품",
      loading: "eager"
    }));
  }

  function renderMediaGallery(project) {
    var media = orderRenderMedia(project);
    if (!media.length) return null;
    var active = media[0];
    var main = el("div", { className: "final-media-main" });
    setMainMedia(main, active, project);
    if (media.length === 1) {
      return el("div", { className: "final-media-strip" }, [main]);
    }
    var thumbs = el("div", { className: "final-media-thumbs" });
    media.forEach(function (item, index) {
      var thumb = el("button", {
        className: "final-media-thumb" + (index === 0 ? " is-active" : "") + (item.type === "video" ? " has-video" : ""),
        type: "button",
        "aria-label": item.type === "video" ? project.code + " 영상 선택" : project.code + " 이미지 선택"
      }, [el("img", { src: item.src, alt: "" })]);
      thumb.addEventListener("click", function () {
        setMainMedia(main, item, project);
        thumbs.querySelectorAll(".final-media-thumb").forEach(function (node) {
          node.classList.remove("is-active");
        });
        thumb.classList.add("is-active");
      });
      thumbs.appendChild(thumb);
    });
    return el("div", { className: "final-media-strip" }, [main, thumbs]);
  }

  function renderRenderStoryboard(project) {
    var items = getRenderMedia(project).filter(function (item) {
      return item.type === "image";
    });
    if (items.length < 3) return null;
    var board = el("div", { className: "final-storyboard" });
    items.forEach(function (item, index) {
      board.appendChild(el("figure", { className: "final-story-card" }, [
        el("img", {
          src: item.src,
          alt: project.code + " 렌더 " + (index + 1),
          loading: "lazy"
        }),
        el("figcaption", {}, [
          el("span", { textContent: "렌더 " + String(index + 1).padStart(2, "0") }),
          el("b", { textContent: "이미지" })
        ])
      ]));
    });
    return el("section", { className: "final-section" }, [
      el("h3", { textContent: "렌더 이미지" }),
      board
    ]);
  }

  function getPresentationLinks(project) {
    return (project.links || []).filter(function (link) {
      return link.kind === "발표 자료";
    });
  }

  function getGoogleSlidesEmbedUrl(url) {
    var normalized = normalizeEmbedUrl(url);
    if (!normalized) return "";
    var match = normalized.match(/\/presentation\/d\/([a-zA-Z0-9-_]+)/);
    if (!match) return "";
    return "https://docs.google.com/presentation/d/" + match[1] + "/embed?start=false&loop=false&delayms=3000";
  }

  function getPresentationOpenUrl(link) {
    return normalizeEmbedUrl(link.url) || link.url || "";
  }

  function isPdfUrl(url) {
    return /\.pdf(?:[?#]|$)/i.test(url || "");
  }

  function getPresentationProvider(link) {
    var url = normalizeEmbedUrl(link.url) || link.url || "";
    if (isPdfUrl(url)) return "PDF";
    try {
      var host = new URL(url).hostname.toLowerCase();
      if (host === "canva.link" || host.endsWith(".canva.com") || host === "canva.com") return "Canva";
      if (host === "docs.google.com") return "Google Slides";
    } catch (error) {
      return link.kind || "발표 자료";
    }
    return link.provider || link.kind || "발표 자료";
  }

  function getPresentationPreview(link, project) {
    if (link.previewSrc) {
      return {
        type: "image",
        src: link.previewSrc
      };
    }
    return bestCover(project);
  }

  function getPresentationEmbed(link) {
    var url = normalizeEmbedUrl(link.url) || link.url || "";
    var slidesEmbed = getGoogleSlidesEmbedUrl(url);
    if (slidesEmbed) return { mode: "iframe", url: slidesEmbed };
    if (isPdfUrl(url)) return { mode: "iframe", url: url };
    return { mode: "external", url: url };
  }

  function renderPresentationLaunch(link, project, embedUrl) {
    var preview = getPresentationPreview(link, project);
    var provider = getPresentationProvider(link);
    var panel = el("a", {
      className: "final-web-launch-panel final-presentation-launch",
      href: resolveProjectLinkUrl(embedUrl),
      target: "_blank",
      rel: "noopener",
      "aria-label": (link.label || project.code + " 발표 자료") + " 열기"
    });
    if (preview) {
      var previewFrame = el("div", { className: "final-presentation-launch-preview" });
      previewFrame.appendChild(el("img", {
        className: "final-web-launch-cover",
        src: preview.src,
        alt: "",
        loading: "lazy"
      }));
      panel.appendChild(previewFrame);
    }
    panel.appendChild(el("div", { className: "final-web-launch-copy" }, [
      el("span", { className: "final-web-embed-kind", textContent: provider }),
      el("strong", { textContent: link.label || project.code + " 발표" }),
      el("b", { textContent: provider === "Canva" ? "Canva에서 열기" : "원본 열기" })
    ]));
    return panel;
  }

  function renderPresentationBlock(link, project, index) {
    var embed = getPresentationEmbed(link);
    var embedUrl = embed.url;
    var openUrl = getPresentationOpenUrl(link);
    if (!embedUrl) return null;
    var block = el("article", {
      className: "final-presentation-block is-presentation-embed",
      "aria-label": link.label || project.code + " 발표 자료"
    });

    if (embed.mode === "iframe") {
      var title = (link.label || project.code) + " 발표 자료 " + (index + 1);
      block.appendChild(el("div", { className: "final-web-embed-head" }, [
        el("div", { className: "final-web-embed-title" }, [
          el("span", { className: "final-web-embed-kind", textContent: link.kind || "발표 자료" }),
          el("strong", { textContent: link.label || project.code + " 발표" })
        ]),
        el("a", {
          className: "final-web-embed-open",
          href: openUrl,
          target: "_blank",
          rel: "noopener",
          textContent: "새 탭에서 열기"
        })
      ]));
      var frame = el("div", { className: "final-presentation-frame is-loading" });
      var iframe = el("iframe", {
        src: embedUrl,
        title: title,
        referrerpolicy: "no-referrer-when-downgrade",
        allow: "autoplay; fullscreen",
        allowfullscreen: ""
      });
      iframe.addEventListener("load", function () {
        frame.classList.remove("is-loading");
      });
      frame.appendChild(iframe);
      block.appendChild(frame);
      block.appendChild(el("p", {
        className: "final-web-embed-note",
        textContent: "슬라이드를 페이지 안에서 넘겨볼 수 있습니다. 더 크게 보려면 새 탭에서 열기를 누르세요."
      }));
      return block;
    }

    block.appendChild(renderPresentationLaunch(link, project, embedUrl));
    return block;
  }

  function renderPresentationSection(project) {
    var links = getPresentationLinks(project);
    if (!links.length) return null;
    var stack = el("div", { className: "final-presentation-stack" });
    links.forEach(function (link, index) {
      var block = renderPresentationBlock(link, project, index);
      if (block) stack.appendChild(block);
    });
    if (!stack.children.length) return null;
    return el("section", { className: "final-section final-section-presentation" }, [
      el("h3", { textContent: "발표 자료" }),
      stack
    ]);
  }

  function renderAiSection(project) {
    var items = getProcessMedia(project);
    if (!items.length) return null;
    var grid = el("div", { className: "final-ai-grid" });
    items.forEach(function (item, index) {
      var label = "AI " + String(index + 1).padStart(2, "0");
      var alt = project.code + " AI 활용 " + (index + 1);
      var card = el("figure", {
        className: "final-ai-card",
        role: "button",
        tabindex: "0",
        "aria-label": alt + " 확대 보기"
      });
      card.appendChild(el("div", { className: "final-ai-card-media" }, [
        el("img", {
          src: item.src,
          alt: alt,
          loading: "lazy"
        })
      ]));
      card.appendChild(el("figcaption", { textContent: label + " · 확대" }));
      card.addEventListener("click", function () {
        openAiImageViewer(item.src, alt, label);
      });
      card.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          openAiImageViewer(item.src, alt, label);
        }
      });
      grid.appendChild(card);
    });
    return el("section", { className: "final-section final-section-ai" }, [
      el("h3", { textContent: "AI 활용" }),
      el("p", {
        className: "final-section-note",
        textContent: "프롬프트, 생성 과정, 레퍼런스 등 AI 도구를 거친 제작 기록입니다. 카드를 누르면 원본 크기로 볼 수 있습니다."
      }),
      grid
    ]);
  }

  function renderDetailWebSection(project) {
    var embedCells = renderWebEmbeds(project);
    if (!embedCells.length) return null;
    var stack = el("div", { className: "final-web-embed-stack" });
    embedCells.forEach(function (cell) { stack.appendChild(cell); });
    return el("section", { className: "final-section final-section-web" }, [
      el("h3", { textContent: "웹 작품" }),
      stack
    ]);
  }

  function getEmbeddableLinks(project) {
    return (project.links || []).filter(isEmbeddableLink);
  }

  function getExternalLinks(project) {
    return (project.links || []).filter(function (link) {
      return !isEmbeddableLink(link) && link.kind !== "발표 자료";
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

  function closeAiImageViewer() {
    var existing = document.querySelector(".final-ai-viewer");
    if (existing) existing.remove();
    document.body.classList.remove("final-ai-viewer-open");
  }

  function closeAllViewers() {
    closeWebViewer();
    closeAiImageViewer();
  }

  function openAiImageViewer(src, alt, label) {
    closeAiImageViewer();
    var viewer = el("div", {
      className: "final-ai-viewer",
      role: "dialog",
      "aria-modal": "true",
      "aria-label": alt || "AI 활용 이미지"
    });
    var toolbar = el("div", { className: "final-web-viewer-bar" }, [
      el("strong", { textContent: label || "AI 활용" }),
      el("div", { className: "final-web-viewer-actions" }, [
        el("button", {
          className: "final-web-viewer-close",
          type: "button",
          textContent: "닫기"
        })
      ])
    ]);
    var frame = el("div", { className: "final-ai-viewer-frame" });
    frame.appendChild(el("img", {
      src: src,
      alt: alt || "",
      className: "final-ai-viewer-image"
    }));
    viewer.appendChild(toolbar);
    viewer.appendChild(frame);
    viewer.querySelector(".final-web-viewer-close").addEventListener("click", closeAiImageViewer);
    viewer.addEventListener("click", function (event) {
      if (event.target === viewer) closeAiImageViewer();
    });
    document.body.appendChild(viewer);
    document.body.classList.add("final-ai-viewer-open");
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

  function renderExternalLinkCell(link, project) {
    var cover = bestCover(project);
    var cell = el("section", {
      className: "final-editorial-cell is-span-4 is-web-launch",
      "aria-label": project.code + " 링크"
    });
    var panel = el("a", {
      className: "final-web-launch-panel",
      href: link.url,
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
      el("strong", { textContent: project.code }),
      el("b", { textContent: "열기 →" })
    ]));
    cell.appendChild(panel);
    return cell;
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
      el("strong", { textContent: project.code }),
      el("b", { textContent: "열기 →" })
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

    var title = project.code + " 미리보기 " + (index + 1);
    var cell = el("section", {
      className: "final-editorial-cell is-span-4 is-web-embed",
      "aria-label": project.code
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
        el("strong", { textContent: project.code })
      ]),
      actions
    ]);
    var frame = el("div", { className: "final-web-embed-frame" });
    var iframe = createWebIframe(embedUrl, title);
    frame.appendChild(iframe);
    actions.querySelector("button").addEventListener("click", function () {
      openWebViewer(embedUrl, project.code);
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
      var href = resolveProjectLinkUrl(link.url);
      if (!href) return;
      list.appendChild(el("a", {
        className: "final-link",
        href: href,
        target: "_blank",
        rel: "noopener"
      }, [
        el("span", { textContent: link.label || link.kind || "Link" }),
        el("b", { textContent: "열기" })
      ]));
    });
    return list.children.length ? list : null;
  }

  function renderDetailNavRow(project, adjacent) {
    var row = el("div", { className: "final-detail-step-row" });
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

    var adjacent = getAdjacentProjects(project);

    var sheet = el("article", { className: "final-detail-sheet" });
    var back = el("button", { className: "final-detail-back", type: "button", textContent: "목록으로" });
    back.addEventListener("click", showProjectList);
    sheet.appendChild(el("div", { className: "final-detail-nav" }, [
      back,
      el("span", { textContent: project.code })
    ]));

    sheet.appendChild(el("div", { className: "final-detail-header" }, [
      el("p", { className: "final-detail-kicker", textContent: "RPD 2026 · Week 15" }),
      el("h2", { textContent: project.title })
    ]));

    var body = el("div", { className: "final-detail-body" });
    var gallery = renderMediaGallery(project);
    if (gallery) {
      body.appendChild(el("section", { className: "final-section" }, [
        el("h3", { textContent: "작품 미디어" }),
        gallery
      ]));
    } else {
      body.appendChild(el("div", {
        className: "final-card-empty",
        textContent: "등록된 렌더·영상 미리보기가 없습니다."
      }));
    }

    var storyboard = renderRenderStoryboard(project);
    if (storyboard) body.appendChild(storyboard);

    var presentationSection = renderPresentationSection(project);
    if (presentationSection) body.appendChild(presentationSection);

    var links = renderDetailLinks(project);
    if (links) {
      body.appendChild(el("section", { className: "final-section" }, [
        el("h3", { textContent: "외부 링크" }),
        links
      ]));
    }

    var webSection = renderDetailWebSection(project);
    if (webSection) body.appendChild(webSection);

    var aiSection = renderAiSection(project);
    if (aiSection) body.appendChild(aiSection);

    body.appendChild(renderDetailNavRow(project, adjacent));
    sheet.appendChild(body);
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
    updateGalleryFootnote(galleryCount);
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
      if (!project) return;
      if (window.matchMedia("(hover: none)").matches && galleryActivePanel !== panel) {
        event.preventDefault();
        var index = Array.prototype.indexOf.call(els.galleryRail.children, panel);
        setGalleryActivePanel(panel, project, index);
        return;
      }
      openProject(project);
    });
  }
  if (els.galleryBack) {
    els.galleryBack.addEventListener("click", function () {
      if (window.history.length > 1) window.history.back();
      else window.location.href = "index.html";
    });
  }
  if (els.galleryToolsToggle) {
    els.galleryToolsToggle.addEventListener("click", function () {
      toggleGalleryTools();
    });
  }
  window.addEventListener("resize", function () {
    if (galleryActivePanel) positionGalleryMeta(galleryActivePanel);
  });
  window.addEventListener("hashchange", onRouteChange);
  window.addEventListener("popstate", onRouteChange);
  window.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeAllViewers();
  });
  render();
})();
