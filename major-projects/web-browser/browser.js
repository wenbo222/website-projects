// TO-DO: Find a more reliable API to handle HTML fetch requests
const urlForm = document.getElementById('url-form');
const urlInput = document.getElementById('url-input');
const viewport = document.getElementById('browser-viewport');

urlForm.addEventListener('submit', (e) => {
    e.preventDefault();
    let targetUrl = urlInput.value.trim();
    if (!targetUrl) return;
    if (!/^https?:\/\//i.test(targetUrl)) { // Add HTTPS if missing
        targetUrl = 'https://'+targetUrl;
    }
    urlInput.value = targetUrl;
    loadURL(targetUrl);
});

viewport.addEventListener('load', () => {
    try {
        const iframeDoc = viewport.contentWindow.document;
        const currentUrl = urlInput.value;
        
        // Handle clicks within website
        iframeDoc.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (link) {
                const href = link.href;
                if (href && !href.startsWith('javascript:') && !href.startsWith('data:') && !href.startsWith('vbscript:')) {
                    // If it is still on the same page, let the default behavior handle it
                    try {
                        const currentUrlObj = new URL(currentUrl);
                        const targetUrlObj = new URL(href);
                        if (currentUrlObj.origin===targetUrlObj.origin && currentUrlObj.pathname===targetUrlObj.pathname) {
                            return;
                        }
                    } catch (err) {
                        // Fallback to loading URL if URL parsing fails
                    }
                    e.preventDefault();
                    urlInput.value = href;
                    loadURL(href);
                }
            }
        }, true); // Capture clicks on the way down instead of when they bubble up
        
        // Intercept form submissions inside the iframe
        iframeDoc.addEventListener('submit', (e) => {
            const form = e.target;
            const action = form.action;
            if (action) {
                const method = (form.getAttribute('method') || 'get').toLowerCase();
                if (method==='get') {
                    e.preventDefault();
                    const formData = new FormData(form);
                    const params = new URLSearchParams(formData).toString();
                    urlInput.value = action.includes('?') ? `${action}&${params}` : `${action}?${params}`;
                    loadURL(urlInput.value);
                }
            }
        }, true); // Capture submits on the way down instead of when they bubble up
    } catch (error) {
        // Ignore cross-origin access errors during initial load / blank page states
    }
});

/**
 * Fetches the HTML content of a URL via a CORS proxy and injects it into the viewport.
 * @param {string} url - The absolute URL to be loaded.
 * @returns {Promise<void>}
 */
async function loadURL(url) {
    try {
        // Fetch website HTML
        const proxyUrl = `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`;
        const response = await fetch(proxyUrl);
        if (!response.ok) {
            throw new Error(`Failed to fetch URL. HTTP status: ${response.status}`);
        }
        const htmlText = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlText, 'text/html');
        
        // Ensure a <base> tag exists to convert from relative to absolute URL
        let baseTag = doc.querySelector('base');
        if (!baseTag) {
            baseTag = doc.createElement('base');
            doc.head.insertBefore(baseTag, doc.head.firstChild);
        }
        baseTag.setAttribute('href', url);

        // Prevent opening links in new tabs/windows
        doc.querySelectorAll('a').forEach(link => {
            if (link.hasAttribute('target')) {
                link.removeAttribute('target');
            }
        });
        viewport.srcdoc = doc.documentElement.outerHTML; // Inject the modified document
    } catch (error) {
        viewport.srcdoc = `
            <div style="font-family: sans-serif; padding: 20px; color: #741a23; background-color: #ccbebf; border: 1px solid #f8bac0; border-radius: 4px; margin: 20px;">
                <h4>Error loading page</h4>
                <p>${error.message}</p>
                <p>Make sure the URL is correct; if so, please try again.</p>
            </div>
        `;
    }
}
