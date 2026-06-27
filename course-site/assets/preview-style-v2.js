(function () {
  "use strict";

  var data = window.RPDFinalProjects || { projects: [], featuredIds: [] };
  var strip = document.getElementById("previewCarousel");
  var indexEl = document.getElementById("galleryIndex");
  var captionEl = document.getElementById("galleryCaption");
  var openBtn = document.getElementById("openDetail");
  var backBtn = document.getElementById("previewBack");
  var heroBtn = document.getElementById("previewGalleryHero");
  var heroImage = document.getElementById("previewGalleryHeroImage");

  var slides = [];
  var activeIndex = 0;
  var projects = [];

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

  function pickProjects() {
    var featured = data.featuredIds || [];
    return featured.map(function (id) {
      return data.projects.find(function (project) { return project.id === id; });
    }).filter(Boolean);
  }

  function tags(project) {
    var parts = [];
    var images = (project.media || []).filter(function (m) { return m.type === "image"; }).length;
    var videos = (project.videos || []).length;
    var web = (project.links || []).some(function (l) {
      return l.kind === "웹페이지" || l.kind === "작품 페이지";
    });
    if (images) parts.push("Render");
    if (videos) parts.push("MP4");
    if (web) parts.push("Web");
    return parts.length ? parts.join(" · ") : "Archive";
  }

  function updateMeta(project) {
    if (!project) return;
    if (indexEl) {
      indexEl.textContent = "( " + String(activeIndex + 1).padStart(2, "0") + " )";
    }
    if (captionEl) {
      captionEl.textContent = project.code + " · " + tags(project);
    }
    if (heroImage && heroBtn) {
      var media = bestCover(project);
      if (media) {
        heroImage.src = media.src;
        heroImage.alt = project.code + " 대표 렌더";
        heroImage.hidden = false;
      } else {
        heroImage.removeAttribute("src");
        heroImage.alt = "";
        heroImage.hidden = true;
      }
    }
  }

  function setActive(index) {
    if (!projects.length) return;
    activeIndex = Math.max(0, Math.min(index, projects.length - 1));
    slides.forEach(function (slide, i) {
      slide.classList.toggle("is-active", i === activeIndex);
      slide.setAttribute("aria-selected", i === activeIndex ? "true" : "false");
    });
    updateMeta(projects[activeIndex]);
  }

  function renderStrip(list) {
    if (!strip) return;
    projects = list;
    strip.textContent = "";
    slides = projects.map(function (project, index) {
      var media = bestCover(project);
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "preview-strip-slide" + (index === activeIndex ? " is-active" : "");
      btn.setAttribute("role", "tab");
      btn.setAttribute("aria-selected", index === activeIndex ? "true" : "false");
      btn.setAttribute("aria-label", project.code + " 선택");

      var frame = document.createElement("div");
      frame.className = "preview-strip-frame";
      if (media) {
        var img = document.createElement("img");
        img.src = media.src;
        img.alt = "";
        img.loading = index < 8 ? "eager" : "lazy";
        frame.appendChild(img);
      }
      btn.appendChild(frame);

      btn.addEventListener("click", function () {
        setActive(index);
      });

      strip.appendChild(btn);
      return btn;
    });
    setActive(activeIndex);
  }

  function openActiveProject() {
    var project = projects[activeIndex];
    if (project) {
      window.location.href = "final-projects.html#" + encodeURIComponent(project.id);
    }
  }

  if (openBtn) openBtn.addEventListener("click", openActiveProject);
  if (heroBtn) heroBtn.addEventListener("click", openActiveProject);
  if (backBtn) {
    backBtn.addEventListener("click", function () {
      window.history.back();
    });
  }

  renderStrip(pickProjects());
})();
