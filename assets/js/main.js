// FocusPsychology — site behaviour: mobile nav + contact form submission

document.addEventListener("DOMContentLoaded", function () {
  /* Mobile nav toggle */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* Contact form submission via Web3Forms (https://web3forms.com) */
  var form = document.getElementById("contact-form");
  if (!form) return;

  var status = document.getElementById("form-status");
  var submitBtn = form.querySelector("button[type='submit']");

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    // Honeypot: if filled, silently drop (bot submission)
    var honeypot = form.querySelector("input[name='botcheck']");
    if (honeypot && honeypot.value) {
      return;
    }

    var accessKey = form.querySelector("input[name='access_key']").value;
    if (!accessKey || accessKey.indexOf("REPLACE_WITH") !== -1) {
      showStatus("error", "The contact form isn't fully set up yet — please email us directly using the address on this page.");
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Sending…";

    var formData = new FormData(form);

    fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { Accept: "application/json" },
      body: formData,
    })
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (data.success) {
          form.reset();
          showStatus("success", "Thanks for getting in touch — we'll reply as soon as we can.");
        } else {
          showStatus("error", "Sorry, something went wrong sending your message. Please try again or email us directly.");
        }
      })
      .catch(function () {
        showStatus("error", "Sorry, something went wrong sending your message. Please try again or email us directly.");
      })
      .finally(function () {
        submitBtn.disabled = false;
        submitBtn.textContent = "Send message";
      });
  });

  function showStatus(type, message) {
    status.textContent = message;
    status.className = "form-status is-visible " + type;
    status.setAttribute("role", type === "error" ? "alert" : "status");
    status.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
});
