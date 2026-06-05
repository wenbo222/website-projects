/**
 * Decodes a File object (image) into an image width, height, and raw RGBA Uint8ClampedArray.
 * @param {File} file - The uploaded image file.
 * @returns {Promise<{width: number, height: number, data: Uint8ClampedArray}>}
 */
export function decodeImage(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.addEventListener('load', () => {
            const img = new Image();
            img.addEventListener('load', () => {
                const canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);
                
                const imageData = ctx.getImageData(0, 0, img.width, img.height);
                resolve({
                    width: img.width,
                    height: img.height,
                    data: imageData.data
                });
            });
            img.addEventListener('error', (err) => reject(new Error('Failed to load image element: '+err.message)));
            img.src = reader.result;
        });
        reader.addEventListener('error', (err) => reject(new Error('Failed to read file: '+err.message)));
        reader.readAsDataURL(file);
    });
}

/**
 * Encodes a Uint8ClampedArray (RGBA) into a Data URL representing a reconstructed PNG image.
 * @param {Uint8ClampedArray} data - Raw RGBA pixel bytes.
 * @param {number} width - Image width.
 * @param {number} height - Image height.
 * @returns {string} Data URL.
 */
export function encodeImage(data, width, height) {
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    
    const imageData = new ImageData(
        new Uint8ClampedArray(data),
        width,
        height
    );
    ctx.putImageData(imageData, 0, 0);
    return canvas.toDataURL();
}
