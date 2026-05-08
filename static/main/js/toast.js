const DURATION = 5000;

const ICONS = {
  success: "fa-check",
  error: "fa-times",
  warning: "fa-exclamation",
  info: "fa-info",
};

const TITLES = {
  success: "Success",
  error: "Error",
  warning: "Warning",
  info: "Notice",
};

function dismissToast(toast) {
  if (toast.dataset.dismissed) return;
  toast.dataset.dismissed = "1";
  clearTimeout(toast._timer);
  toast.classList.add("toast-hiding");
  toast.addEventListener("animationend", () => toast.remove(), { once: true });
}

function showToast(type, title, message, duration) {
  duration = duration || DURATION;
  const container = document.getElementById("toast-container");

  const toast = document.createElement("div");
  toast.className = "toast toast-" + type;
  toast.setAttribute("role", "alert");
  toast.dataset.duration = duration;

  toast.innerHTML =
    '<div class="toast-icon-wrap">' +
    '<i class="fa ' +
    (ICONS[type] || "fa-info") +
    '"></i>' +
    "</div>" +
    '<div class="toast-body">' +
    '<div class="toast-title">' +
    (title || TITLES[type] || "Notice") +
    "</div>" +
    '<div class="toast-message">' +
    message +
    "</div>" +
    "</div>" +
    '<button class="toast-dismiss" aria-label="Dismiss"><i class="fa fa-times"></i></button>' +
    '<div class="toast-progress" style="animation-duration:' +
    duration +
    'ms;"></div>';

  container.appendChild(toast);

  toast
    .querySelector(".toast-dismiss")
    .addEventListener("click", () => dismissToast(toast));

  toast._timer = setTimeout(() => dismissToast(toast), duration);
}

/* Boot Django-rendered toasts already in the DOM */
document.querySelectorAll(".toast").forEach((toast) => {
  const duration = parseInt(toast.dataset.duration) || DURATION;
  const progress = toast.querySelector(".toast-progress");
  if (progress) progress.style.animationDuration = duration + "ms";

  toast
    .querySelector(".toast-dismiss")
    ?.addEventListener("click", () => dismissToast(toast));
  toast._timer = setTimeout(() => dismissToast(toast), duration);
});
