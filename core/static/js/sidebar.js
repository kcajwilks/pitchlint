document.addEventListener("DOMContentLoaded", function () {
  var root = document.documentElement;
  var toggle = document.querySelector(".js-sidebar-toggle");
  if (!toggle) {
    return;
  }

  var collapsed = localStorage.getItem("sidebar_collapsed") === "true";
  if (collapsed) {
    root.classList.add("sidebar-collapsed");
  }

  toggle.addEventListener("click", function () {
    root.classList.toggle("sidebar-collapsed");
    localStorage.setItem("sidebar_collapsed", root.classList.contains("sidebar-collapsed"));
  });
});
