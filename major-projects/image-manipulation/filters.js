/**
 * Applies a grayscale filter to the image data.
 * @param {Uint8ClampedArray} data - Raw RGBA pixel bytes.
 * @returns {Uint8ClampedArray} New array with grayscale pixel bytes.
 */
export function applyGrayscale(data) {
    const output = new Uint8ClampedArray(data.length);
    for(let i=0; i<data.length; i+=4) {
        const r = data[i];
        const g = data[i+1];
        const b = data[i+2];
        output[i+3] = data[i+3]; // A unchanged
        
        const average = Math.floor((r+g+b)/3);
        output[i] = average;
        output[i+1] = average;
        output[i+2] = average;
    }
    return output;
}

/**
 * Applies a sepia filter to the image data.
 * @param {Uint8ClampedArray} data - Raw RGBA pixel bytes.
 * @returns {Uint8ClampedArray} New array with sepia pixel bytes.
 */
export function applySepia(data) {
    const output = new Uint8ClampedArray(data.length);
    for(let i=0; i<data.length; i+=4) {
        const r = data[i];
        const g = data[i+1];
        const b = data[i+2];
        output[i+3] = data[i+3]; // A unchanged
        
        output[i] = Math.round(Math.min(255, 0.393*r+0.769*g+0.189*b));
        output[i+1] = Math.round(Math.min(255, 0.349*r+0.686*g+0.168*b));
        output[i+2] = Math.round(Math.min(255, 0.272*r+0.534*g+0.131*b));
    }
    return output;
}

/**
 * Flips the image horizontally (mirror).
 * @param {Uint8ClampedArray} data - Raw RGBA pixel bytes.
 * @param {number} width - Image width.
 * @param {number} height - Image height.
 * @returns {Uint8ClampedArray} New array with mirrored pixel bytes.
 */
export function applyMirror(data, width, height) {
    const output = new Uint8ClampedArray(data.length);
    for(let y=0; y<height; y++) {
        for(let x=0; x<width; x++) {
            const srcIdx = (y*width+x)*4;
            const destIdx = (y*width+(width-1-x))*4;
            output[destIdx] = data[srcIdx];
            output[destIdx+1] = data[srcIdx+1];
            output[destIdx+2] = data[srcIdx+2];
            output[destIdx+3] = data[srcIdx+3];
        }
    }
    return output;
}

