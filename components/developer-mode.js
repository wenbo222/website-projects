import {ProjectFilesMap} from './project-files-map.js';

let prismLoadingPromise = null;

class DeveloperMode extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({mode: 'open'});
        this._observer = null;
    }

    async connectedCallback() {
        const currentPath = window.location.pathname;
        let matchKey = null;
        for (const key of Object.keys(ProjectFilesMap)) {
            if (currentPath.endsWith(key)) {
                matchKey = key;
                break;
            }
        }

        if (!matchKey) return;

        const files = ProjectFilesMap[matchKey];
        let html = `
            <style>
                @import url('https://cdn.jsdelivr.net/npm/prismjs@1.30.0/themes/prism-tomorrow.min.css');
                
                :host {
                    display: block;
                    max-width: 75rem;
                    margin: 3rem auto 2rem auto;
                    padding: 0 1rem;
                    font-family: Arial, Helvetica, sans-serif;
                }

                /* Code block styling */
                .dev-mode-title {
                    font-size: 1.5rem;
                    font-weight: 700;
                    margin-bottom: 1.5rem;
                    color: var(--page-text);
                    text-align: center;
                }
                .code-card {
                    background: var(--container-bg);
                    border: 1px solid var(--border-color);
                    border-radius: 0.75rem;
                    overflow: hidden;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    margin-bottom: 2rem;
                }
                .code-header {
                    background: rgba(128, 128, 128, 0.08);
                    padding: 0.75rem 1.25rem;
                    border-bottom: 1px solid var(--border-color);
                }
                .filename {
                    font-size: 0.85rem;
                    font-family: monospace;
                    color: var(--page-text);
                    font-weight: 600;
                }
                pre[class*="language-"] {
                    margin: 0 !important;
                    padding: 1.25rem !important;
                    background: transparent !important;
                    font-size: 0.95rem !important;
                }
                code[class*="language-"] {
                    text-shadow: none !important;
                    color: var(--page-text) !important;
                }
                
                /* Light mode */
                .token.comment, .token.prolog, .token.doctype, .token.namespace { color: #3c4248 !important; }
                .token.punctuation { color: #222222 !important; }
                .token.keyword, .token.operator, .token.tag, .token.attr-name, .token.selector, .token.important { color: #8e121e !important; }
                .token.string, .token.attr-value, .token.regex, .token.variable { color: #042347 !important; }
                .token.function, .token.property, .token.atrule, .token.builtin { color: #4b0082 !important; }
                .token.number, .token.boolean { color: #005000 !important; }
                .token.class-name { color: #5d2d0b !important; }

                /* Dark mode */
                :host([data-theme="dark"]) .token.comment, :host([data-theme="dark"]) .token.prolog, :host([data-theme="dark"]) .token.doctype, :host([data-theme="dark"]) .token.namespace { color: #d1d5db !important; }
                :host([data-theme="dark"]) .token.punctuation { color: #ffffff !important; }
                :host([data-theme="dark"]) .token.keyword, :host([data-theme="dark"]) .token.operator, :host([data-theme="dark"]) .token.tag, :host([data-theme="dark"]) .token.attr-name, :host([data-theme="dark"]) .token.selector, :host([data-theme="dark"]) .token.important { color: #ffbcbc !important; }
                :host([data-theme="dark"]) .token.string, :host([data-theme="dark"]) .token.attr-value, :host([data-theme="dark"]) .token.regex, :host([data-theme="dark"]) .token.variable { color: #cce6ff !important; }
                :host([data-theme="dark"]) .token.function, :host([data-theme="dark"]) .token.property, :host([data-theme="dark"]) .token.atrule, :host([data-theme="dark"]) .token.builtin { color: #e1d5ff !important; }
                :host([data-theme="dark"]) .token.number, :host([data-theme="dark"]) .token.boolean { color: #b2ffcc !important; }
                :host([data-theme="dark"]) .token.class-name { color: #ffe0b2 !important; }
            </style>
            
            <div class="dev-mode-container">
                <hr style="margin-bottom: 2rem; border: none; border-top: 1px solid var(--border-color, #cccccc);">
                <h2 class="dev-mode-title">Developer Mode: Source Code</h2>
        `;

        for (const file of files) {
            html += `
                <div class="code-card">
                    <div class="code-header">
                        <div class="filename">${file}</div>
                    </div>
                    <pre><code id="code-${file.replace(/\./g, '-')}" class="language-${this.getLanguage(file)}">Loading...</code></pre>
                </div>
            `;
        }
        
        html += `</div>`; // closing dev-mode-container
        this.shadowRoot.innerHTML = html;
        await this.loadPrism();

        // Fetch and display code
        for (const file of files) {
            try {
                // Ensure we fetch relative to the current html directory
                const response = await fetch(file);
                const codeEl = this.shadowRoot.getElementById(`code-${file.replace(/\./g, '-')}`);
                if (response.ok) {
                    const text = await response.text();
                    codeEl.textContent = text;
                    if (window.Prism) {
                        window.Prism.highlightElement(codeEl);
                    }
                } else {
                    codeEl.textContent = `Error loading ${file}: ${response.statusText}`;
                }
            } catch (err) {
                const codeEl = this.shadowRoot.getElementById(`code-${file.replace(/\./g, '-')}`);
                if (codeEl) {
                    codeEl.textContent = `Error loading ${file}: ${err.message}`;
                }
            }
        }

        // Keep theme in sync
        const updateTheme = () => {
            if (document.documentElement.getAttribute('data-theme')==='dark') {
                this.setAttribute('data-theme', 'dark');
            } else {
                this.removeAttribute('data-theme');
            }
        };
        updateTheme();
        this._observer = new MutationObserver(updateTheme);
        this._observer.observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
    }

    disconnectedCallback() {
        if (this._observer) {
            this._observer.disconnect();
            this._observer = null;
        }
    }

    getLanguage(filename) {
        if (filename.endsWith('.js')) return 'javascript';
        if (filename.endsWith('.css')) return 'css';
        if (filename.endsWith('.html')) return 'html';
        if (filename.endsWith('.py')) return 'python';
        return 'none';
    }

    async loadPrism() {
        if (window.Prism) return Promise.resolve();
        if (prismLoadingPromise) return prismLoadingPromise;

        prismLoadingPromise = new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/prismjs@1.30.0/prism.min.js';
            script.addEventListener('load', () => {
                const pyScript = document.createElement('script');
                pyScript.src = 'https://cdn.jsdelivr.net/npm/prismjs@1.30.0/components/prism-python.min.js';
                pyScript.addEventListener('load', resolve);
                pyScript.addEventListener('error', resolve); // Continue even if python fails
                document.head.appendChild(pyScript);
            });
            script.addEventListener('error', (err) => {
                prismLoadingPromise = null; 
                reject(err);
            });
            document.head.appendChild(script);
        });
        return prismLoadingPromise;
    }
}

customElements.define('developer-mode', DeveloperMode);
