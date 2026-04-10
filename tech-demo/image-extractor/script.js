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
            const img = new Image();
            img.addEventListener('load', () => {
                // Extract image as byte array
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
                const byteArray = ctx.getImageData(0, 0, canvas.width, canvas.height).data;

                // Reconstruct image from byte array
                const reconstructedImageData = new ImageData(
                    new Uint8ClampedArray(byteArray),
                    canvas.width,
                    canvas.height
                );
                const resultCanvas = document.createElement('canvas');
                resultCanvas.width = canvas.width;
                resultCanvas.height = canvas.height;
                const resultCtx = resultCanvas.getContext('2d');
                resultCtx.putImageData(reconstructedImageData, 0, 0);

                // Convert back to image for display
                const reconstructedImg = document.createElement('img');
                reconstructedImg.src = resultCanvas.toDataURL();
                reconstructedImg.classList.add('show');
                imageOutput.innerHTML = "";
                imageOutput.appendChild(reconstructedImg);

                // Add a small info overlay
                const info = document.createElement('div');
                info.style.cssText = 'margin-top: 1rem; font-size: 0.9rem; color: var(--page-text); opacity: 0.8;';
                info.innerHTML = `<strong>Success!</strong> Reconstructed from ${byteArray.length.toLocaleString()} raw bytes.`;
                imageOutput.appendChild(info);
            });
            img.src = reader.result;
        });
        reader.readAsDataURL(file);
    } else {
        imageOutput.innerHTML = "You just found a bug!";
    }
});
