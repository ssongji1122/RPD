(function () {
  "use strict";

  var data = window.RPDFinalProjects || { stats: {}, projects: [] };
  var state = {
    query: "",
    activeId: ""
  };

  var els = {
    stats: document.getElementById("finalStats"),
    search: document.getElementById("finalSearch"),
    count: document.getElementById("finalResultCount"),
    grid: document.getElementById("finalGrid"),
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

  function projectSearchText(project) {
    return [
      project.code,
      project.title,
      "RPD 2026",
      "Week 15",
      (project.links || []).map(function (item) { return item.label; }).join(" ")
    ].join(" ").toLowerCase();
  }

  function getFilteredProjects() {
    var query = state.query.trim().toLowerCase();
    return data.projects.filter(function (project) {
      if (query && projectSearchText(project).indexOf(query) === -1) return false;
      return true;
    });
  }

  function mediaCover(project) {
    return (project.media || [])[0] || null;
  }

  function renderCard(project) {
    var cover = mediaCover(project);
    var card = el("button", {
      className: "final-card" + (project.id === state.activeId ? " is-active" : ""),
      type: "button",
      "data-project-id": project.id,
      "aria-label": project.code + " 작품 보기"
    });
    var media = el("div", { className: "final-card-media" });
    if (cover) {
      media.appendChild(el("img", { src: cover.src, alt: project.code + " 미리보기", loading: "lazy" }));
    } else {
      media.appendChild(el("div", { className: "final-card-empty", textContent: "미리보기 없음" }));
    }
    card.appendChild(media);
    card.appendChild(el("div", { className: "final-card-body" }, [
      el("div", { className: "final-card-meta" }, [
        el("span", { textContent: "RPD 2026" }),
        el("span", { textContent: project.code })
      ]),
      el("h3", { textContent: project.title }),
      el("p", { textContent: getProjectMeta(project) })
    ]));
    card.addEventListener("click", function () {
      state.activeId = project.id;
      location.hash = project.id;
      render();
      els.detail.scrollIntoView({ block: "nearest" });
    });
    return card;
  }

  function renderMedia(project) {
    var media = project.media || [];
    if (!media.length) {
      return el("div", { className: "final-card-empty", textContent: "등록된 미리보기가 없습니다." });
    }
    var active = media[0];
    var main = el("div", { className: "final-media-main" });
    setMainMedia(main, active, project);
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
    container.appendChild(el("img", { src: item.src, alt: project.code + " 작품" }));
  }

  function getProjectMeta(project) {
    var parts = [];
    var storyboardCount = getStoryboardItems(project).length;
    if (storyboardCount >= 3) parts.push("스토리보드 " + storyboardCount + "장");
    if ((project.videos || []).length) parts.push("영상 " + project.videos.length + "개");
    if ((project.links || []).length) parts.push("링크 " + project.links.length + "개");
    return parts.length ? parts.join(" · ") : "이미지 기록";
  }

  function getStoryboardItems(project) {
    return (project.media || []).slice(0, 12).map(function (item, index) {
      return {
        src: item.src,
        type: item.type === "video" ? "영상 장면" : "이미지 장면",
        label: "장면 " + String(index + 1).padStart(2, "0")
      };
    });
  }

  function renderStoryboard(project) {
    var items = getStoryboardItems(project);
    if (items.length < 3) return null;
    var board = el("div", { className: "final-storyboard" });
    items.forEach(function (item) {
      board.appendChild(el("figure", { className: "final-story-card" }, [
        el("img", { src: item.src, alt: project.code + " " + item.label, loading: "lazy" }),
        el("figcaption", {}, [
          el("span", { textContent: item.label }),
          el("b", { textContent: item.type })
        ])
      ]));
    });
    return el("section", { className: "final-section" }, [
      el("h3", { textContent: "스토리보드 / 장면 흐름" }),
      board
    ]);
  }

  function renderLinks(project) {
    var links = project.links || [];
    if (!links.length) return null;
    var list = el("div", { className: "final-link-list" });
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
    return el("section", { className: "final-section" }, [
      el("h3", { textContent: "외부 작품 링크" }),
      list
    ]);
  }

  function renderVideos(project) {
    var videos = project.videos || [];
    if (!videos.length) return null;
    var list = el("div", { className: "final-video-list" });
    videos.forEach(function (video, index) {
      list.appendChild(el("video", {
        src: video.src,
        poster: video.poster || "",
        controls: "",
        playsinline: "",
        preload: "metadata",
        "aria-label": project.code + " 영상 " + (index + 1)
      }));
    });
    return el("section", { className: "final-section" }, [
      el("h3", { textContent: "영상" }),
      list
    ]);
  }

  function renderDetail(project) {
    els.detail.textContent = "";
    if (!project) {
      els.detail.appendChild(el("p", { className: "final-detail-summary", textContent: "왼쪽에서 작품을 선택하면 큰 미리보기가 표시됩니다." }));
      return;
    }
    els.detail.appendChild(el("div", { className: "final-detail-kicker", textContent: "RPD 2026 · " + project.code }));
    els.detail.appendChild(el("h2", { textContent: project.title }));
    els.detail.appendChild(el("p", { className: "final-detail-summary", textContent: getProjectMeta(project) + "를 함께 담은 최종 결과물 기록입니다." }));
    els.detail.appendChild(renderMedia(project));
    var storyboard = renderStoryboard(project);
    if (storyboard) els.detail.appendChild(storyboard);
    var videos = renderVideos(project);
    if (videos) els.detail.appendChild(videos);
    var links = renderLinks(project);
    if (links) els.detail.appendChild(links);
  }

  function render() {
    var projects = getFilteredProjects();
    if (!state.activeId || !data.projects.some(function (project) { return project.id === state.activeId; })) {
      state.activeId = projects[0] ? projects[0].id : "";
    }
    els.count.textContent = projects.length + " works";
    els.grid.textContent = "";
    if (!projects.length) {
      els.grid.appendChild(el("div", { className: "final-empty-state", textContent: "조건에 맞는 작품이 없습니다." }));
    } else {
      projects.forEach(function (project) {
        els.grid.appendChild(renderCard(project));
      });
    }
    renderDetail(data.projects.find(function (project) { return project.id === state.activeId; }));
  }

  function hydrateFromUrl() {
    state.activeId = location.hash ? decodeURIComponent(location.hash.slice(1)) : "";
  }

  hydrateFromUrl();
  renderStats();
  els.search.addEventListener("input", function () {
    state.query = els.search.value || "";
    render();
  });
  window.addEventListener("hashchange", function () {
    state.activeId = location.hash ? decodeURIComponent(location.hash.slice(1)) : state.activeId;
    render();
  });
  render();
})();
