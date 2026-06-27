// app.js
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// 스크롤 인뷰 reveal
if (!reduce && "IntersectionObserver" in window) {
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
    }
  }, { threshold: 0.15 });
  document.querySelectorAll("[data-reveal]").forEach((el) => io.observe(el));
} else {
  document.querySelectorAll("[data-reveal]").forEach((el) => el.classList.add("is-in"));
}

// 영상 클릭 재생(자동재생 금지) — 영상 자산 확보 후 동작
document.querySelectorAll(".media__play").forEach((btn) => {
  btn.addEventListener("click", () => {
    const video = btn.parentElement.querySelector("video");
    if (!video) return;
    video.setAttribute("controls", "");
    btn.remove();
    video.play();
  });
});
