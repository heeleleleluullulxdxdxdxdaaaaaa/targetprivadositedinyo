
function toggleFullscreen(img) {
  const modal = document.getElementById("fullscreenModal");
  const modalImg = document.getElementById("fullscreenImage");

  modal.style.display = "block";
  modalImg.src = img.src;

  setTimeout(() => {
      modal.classList.add("active");
      modalImg.classList.add("active");
  });
}

function closeFullscreen() {
  const modal = document.getElementById("fullscreenModal");
  const modalImg = document.getElementById("fullscreenImage");

  modal.classList.remove("active");
  modalImg.classList.remove("active");
  setTimeout(() => {
      modal.style.display = "none";
  }, 300);
}