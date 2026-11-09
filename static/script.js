document.addEventListener("DOMContentLoaded", function () {

const input = document.getElementById("imageInput");
const preview = document.getElementById("previewImage");
const content = document.getElementById("uploadContent");
const form = document.getElementById("detectForm");
const loading = document.getElementById("loadingBox");
const chooseBtn = document.getElementById("chooseBtn");

loading.style.display = "none";

// buka file explorer
chooseBtn.addEventListener("click", () => {
input.click();
});

// preview gambar
input.addEventListener("change", function () {

const file = this.files[0];

if(file){

preview.src = URL.createObjectURL(file);
preview.style.display = "block";
content.style.display = "none";

}

});

// submit form
form.addEventListener("submit", function(e){

if(input.files.length === 0){

e.preventDefault();
alert("Silakan pilih gambar terlebih dahulu!");

return;

}

loading.style.display = "flex";

});

});