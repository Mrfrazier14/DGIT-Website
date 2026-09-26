// DivineGuard IT Services LLC — site scripts

document.addEventListener("DOMContentLoaded", function () {
  // Mobile nav toggle
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var isOpen = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });

    links.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Only select a service already defined in the existing contact form.
  var service = document.getElementById("service");
  var requestedService = new URLSearchParams(window.location.search).get("service");
  if (service && requestedService) {
    var matches = Array.from(service.options).some(function (option) {
      return option.value === requestedService;
    });
    if (matches) service.value = requestedService;
  }

  // Footer year
  var yearEl = document.getElementById("year");
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

});
