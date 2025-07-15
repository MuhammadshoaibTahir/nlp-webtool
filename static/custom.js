document.addEventListener("DOMContentLoaded", function () {
  // Auto-resize textarea
  const textarea = document.querySelector("textarea");
  if (textarea) {
    textarea.addEventListener("input", () => {
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    });
  }

  // Scroll to results after analysis
  const resultSection = document.querySelector(".card");
  if (resultSection) {
    resultSection.scrollIntoView({ behavior: "smooth" });
  }

  // Optional: Show spinner on button click
  const form = document.querySelector("form");
  const button = form?.querySelector("button");
  if (form && button) {
    form.addEventListener("submit", () => {
      button.disabled = true;
      button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Analyzing...`;
    });
  }
});
