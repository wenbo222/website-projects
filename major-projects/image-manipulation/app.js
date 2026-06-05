import {decodeImage, encodeImage} from './canvas.js';
import {applyGrayscale, applySepia, applyMirror} from './filters.js';

const imageInput = document.getElementById('image-input');
const grayscaleBtn = document.getElementById('grayscale-btn');
const sepiaBtn = document.getElementById('sepia-btn');
const mirrorBtn = document.getElementById('mirror-btn');
const resetBtn = document.getElementById('reset-btn');
const downloadBtn = document.getElementById('download-btn');
const previewContainer = document.getElementById('preview-container');
const infoText = document.getElementById('info-text');

/** @type {{width: number, height: number, data: Uint8ClampedArray}|null} */
let originalImage = null;
/** @type {Uint8ClampedArray|null} */
let currentImageData = null;
let currentWidth = 0;
let currentHeight = 0;

/**
 * Enables or disables the filter action and reset buttons.
 * @param {boolean} enabled - Whether the buttons should be enabled or not.
 */
function toggleButtons(enabled) {
    grayscaleBtn.disabled = sepiaBtn.disabled = mirrorBtn.disabled = resetBtn.disabled = downloadBtn.disabled = !enabled;
}

/**
 * Updates the image preview based on the current data.
 */
function updatePreview() {
    if (!currentImageData) return;
    const dataUrl = encodeImage(currentImageData, currentWidth, currentHeight);
    // Clear preview container and insert img
    previewContainer.innerHTML = '';
    const img = document.createElement('img');
    img.src = dataUrl;
    img.alt = 'Preview';
    img.classList.add('show');
    previewContainer.appendChild(img);
    infoText.innerHTML = `Dimensions: ${currentWidth} x ${currentHeight} | Bytes: ${currentImageData.length.toLocaleString()}`;
}

// Handle Image Upload
imageInput.addEventListener('change', async () => {
    const file = imageInput.files[0];
    if (!file) return;
    if (!file.type.startsWith('image/')) {
        previewContainer.innerHTML = `<p class="error-message">Error: Please select a valid image file.</p>`;
        toggleButtons(false);
        originalImage = null;
        currentImageData = null;
        return;
    }
    try {
        previewContainer.innerHTML = '<p class="loading">Decoding image...</p>';
        originalImage = await decodeImage(file);
        currentImageData = new Uint8ClampedArray(originalImage.data);
        currentWidth = originalImage.width;
        currentHeight = originalImage.height;
        updatePreview();
        toggleButtons(true);
    } catch (error) {
        previewContainer.innerHTML = `<p class="error-message">Error decoding image: ${error.message}</p>`;
        toggleButtons(false);
    }
});

// Filters
grayscaleBtn.addEventListener('click', () => {
    if (!currentImageData) return;
    currentImageData = applyGrayscale(currentImageData);
    updatePreview();
});
sepiaBtn.addEventListener('click', () => {
    if (!currentImageData) return;
    currentImageData = applySepia(currentImageData);
    updatePreview();
});
mirrorBtn.addEventListener('click', () => {
    if (!currentImageData) return;
    currentImageData = applyMirror(currentImageData, currentWidth, currentHeight);
    updatePreview();
});

// Reset image to original upload state
resetBtn.addEventListener('click', () => {
    if (!originalImage) return;
    currentImageData = new Uint8ClampedArray(originalImage.data);
    currentWidth = originalImage.width;
    currentHeight = originalImage.height;
    updatePreview();
});

// Download modified image
downloadBtn.addEventListener('click', () => {
    if (!currentImageData) return;
    const dataUrl = encodeImage(currentImageData, currentWidth, currentHeight);
    const link = document.createElement('a');
    link.href = dataUrl;
    link.download = 'modified-image.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});
