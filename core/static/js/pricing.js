document.addEventListener("DOMContentLoaded", function () {
  var container = document.querySelector("[data-pricing-toggle]");
  if (!container) {
    return;
  }

  var buttons = container.querySelectorAll(".js-pricing-interval");
  var amountEls = document.querySelectorAll(".js-plan-amount");
  var intervalInputs = document.querySelectorAll(".js-plan-interval");

  function setInterval(interval) {
    buttons.forEach(function (btn) {
      var isActive = btn.dataset.interval === interval;
      btn.classList.toggle("active", isActive);
      btn.classList.toggle("btn-primary", isActive);
      btn.classList.toggle("btn-outline-secondary", !isActive);
    });

    amountEls.forEach(function (el) {
      var nextAmount = interval === "yearly" ? el.dataset.amountYearly : el.dataset.amountMonthly;
      var suffix = interval === "yearly" ? "/yr" : "/mo";
      el.textContent = nextAmount || "Contact";
      if (el.nextElementSibling) {
        el.nextElementSibling.textContent = suffix;
      }
    });

    intervalInputs.forEach(function (input) {
      input.value = interval;
    });
  }

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setInterval(btn.dataset.interval);
    });
  });

  setInterval("monthly");
});
