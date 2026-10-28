/* AIS portfolio — reveal on scroll + lightbox + nav shadow. Zero dependencies. */
(function () {
  "use strict";

  /* ---- reveal on scroll ---- */
  var revealEls = document.querySelectorAll(".reveal");
  if (revealEls.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- certificate lightbox ---- */
  var box = document.querySelector(".lightbox");
  var boxImg = box && box.querySelector("img");
  var openers = document.querySelectorAll("[data-lightbox]");
  openers.forEach(function (el) {
    el.addEventListener("click", function () {
      if (!box || !boxImg) return;
      boxImg.src = el.getAttribute("data-lightbox");
      boxImg.alt = el.querySelector("img") ? el.querySelector("img").alt : "";
      box.setAttribute("data-open", "true");
      document.documentElement.style.overflow = "hidden";
    });
  });
  function close() {
    if (!box) return;
    box.setAttribute("data-open", "false");
    document.documentElement.style.overflow = "";
  }
  if (box) {
    box.addEventListener("click", function (e) {
      if (e.target === box || e.target.classList.contains("lightbox__close")) close();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  /* ---- nav hairline shadow on scroll ---- */
  var nav = document.querySelector(".nav");
  if (nav) {
    var onScr = function () {
      if (window.scrollY > 8) nav.classList.add("is-scrolled");
      else nav.classList.remove("is-scrolled");
    };
    window.addEventListener("scroll", onScr, { passive: true });
    onScr();
  }
})();
