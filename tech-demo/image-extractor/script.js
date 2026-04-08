// TO-DO: use Canvas API to extract image as byte array
// TO-DO: use the byte array to reconstruct the image
const imageInput = document.getElementById('image-input');
const extractBtn = document.getElementById('extract-btn');
const imageOutput = document.getElementById('image-output');

imageInput.addEventListener('change', () => {
    extractBtn.disabled = !imageInput.files[0];
});

extractBtn.addEventListener('click', () => {
    const file = imageInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.addEventListener("load", () => {
            const img = document.createElement('img');
            img.src = reader.result;
            imageOutput.innerHTML = "";
            imageOutput.appendChild(img);
        });
        reader.readAsDataURL(file);
    } else {
        imageOutput.innerHTML = "You just found a bug!";
    }
});