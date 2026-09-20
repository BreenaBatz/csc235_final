document.addEventListener("DOMContentLoaded", function() {
  console.log("Dragonfire Meadery app script loaded.");

document.querySelectorAll(".btn").forEach(btn => {
    btn.addEventListener("mouseenter", () => btn.classList.add("shadow-lg"));
    btn.addEventListener("mouseleave", () => btn.classList.remove("shadow-lg"));
});

});
