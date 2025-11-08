

// register.html file
function previewPhoto(event) {
      const input = event.target;
      const preview = document.getElementById('photoPreview');

      if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
          preview.innerHTML = `<img class="w-50 h-50 shadow-sm object-fit-cover border border-1 border-light rounded" src="${e.target.result}" alt="Passport Photo">`;
          preview.classList = "display:'inline',border='2px'"
        };
        reader.readAsDataURL(input.files[0]);
      } else {
        preview.innerHTML = `<i class="bi bi-person-bounding-box fs-1 text-secondary"></i>`;
      }
    }





