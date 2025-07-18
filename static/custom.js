document.addEventListener("DOMContentLoaded", function () {
  // Auto-resize textarea
  const textarea = document.querySelector("textarea");
  if (textarea) {
    textarea.addEventListener("input", () => {
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    });

    // Trigger auto-resize on load in case there's pre-filled content
    textarea.dispatchEvent(new Event('input'));
  }

  // Show spinner and disable button on form submission
  const form = document.querySelector("form");
  const button = form?.querySelector("button[type='submit']");
  const resultContainer = document.querySelector(".results");

  if (form && button) {
    form.addEventListener("submit", () => {
      // Prevent double click
      button.disabled = true;
      button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Analyzing...`;

      // Clear previous results (optional)
      if (resultContainer) {
        resultContainer.innerHTML = "";
      }
    });
  }

  // Smooth scroll to result section (if available after results load)
  const observer = new MutationObserver((mutationsList, observer) => {
    for (const mutation of mutationsList) {
      if (mutation.type === "childList" && mutation.addedNodes.length > 0) {
        const resultCard = document.querySelector(".results");
        if (resultCard) {
          resultCard.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }
    }
  });

  if (document.querySelector(".results")) {
    observer.observe(document.querySelector(".results"), {
      childList: true,
      subtree: true
    });
  }
});