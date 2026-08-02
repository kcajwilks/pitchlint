function resolveTheme(theme) {
  if (theme === "system") {
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  return theme;
}

function applyTheme(theme) {
  var resolved = resolveTheme(theme);
  document.documentElement.setAttribute("data-bs-theme", resolved);
  document.querySelectorAll(".js-theme-btn").forEach(function (btn) {
    btn.classList.toggle("active", btn.dataset.themeValue === theme);
  });
}

document.addEventListener("DOMContentLoaded", function () {
  var current = localStorage.getItem("theme") || "system";
  applyTheme(current);

  document.querySelectorAll(".js-theme-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var theme = btn.dataset.themeValue;
      localStorage.setItem("theme", theme);
      applyTheme(theme);
    });
  });

  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
    if ((localStorage.getItem("theme") || "system") === "system") {
      applyTheme("system");
    }
  });
});
