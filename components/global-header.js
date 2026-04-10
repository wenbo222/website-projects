// TO-DO: Add logo and search functionality
class GlobalHeader extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({mode: 'open'});
    }

    connectedCallback() {
        const rootUrl = new URL('../', import.meta.url).href;

        this.shadowRoot.innerHTML = `
            <style>
                /* Heading theme styling */
                *, *::before, *::after {
                    box-sizing: border-box;
                }
                :host {
                    display: block;
                    position: relative;
                    font-family: Arial, Helvetica, sans-serif;
                    --bg-color: #ffffff;
                    --text-color: #333333;
                    --text-hover: #000000;
                    --border-color: #eaeaea;
                    --search-bg: #f5f5f5;
                    --search-icon: #666666;
                    --dropdown-bg: #ffffff;
                    --dropdown-hover: #f0f0f0;
                    --btn-outline-border: #333333;
                    --btn-outline-hover: rgba(0, 0, 0, 0.05);
                    --btn-filled-bg: #333333;
                    --btn-filled-text: #fff;
                    --menu-group-title: #666666;
                    --hamburger-line: #333333;
                }
                :host([data-theme="dark"]) {
                    --bg-color: #1b1b1b;
                    --text-color: #ffffff;
                    --text-hover: #e2e2e2;
                    --border-color: #333333;
                    --search-bg: #333333;
                    --search-icon: #aaaaaa;
                    --dropdown-bg: #1b1b1b;
                    --dropdown-hover: #333333;
                    --btn-outline-border: #ffffff;
                    --btn-outline-hover: rgba(255, 255, 255, 0.1);
                    --btn-filled-bg: #ffffff;
                    --btn-filled-text: #000000;
                    --menu-group-title: #aaaaaa;
                    --hamburger-line: #ffffff;
                }

                /* Title styling */
                header {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 0 1.5rem;
                    height: 3.75rem;
                    background-color: var(--bg-color);
                    color: var(--text-color);
                    border-bottom: 1px solid var(--border-color);
                    transition: background-color 0.3s, color 0.3s;
                }
                .logo-container {
                    display: flex;
                    align-items: center;
                    text-decoration: none;
                    color: var(--text-color);
                    font-weight: 700;
                    font-size: 1.1rem;
                    transition: color 0.2s;
                    flex-shrink: 0;
                    white-space: nowrap;
                }
                .logo-container:hover {
                    color: var(--text-hover);
                }
                .logo {
                    width: 2rem;
                    height: 2rem;
                    background-color: var(--text-color);
                    border-radius: 0.25rem;
                    margin-right: 0.8rem;
                    display: inline-block;
                    transition: background-color 0.3s;
                }

                /* Search bar styling */
                .search-bar {
                    display: flex;
                    align-items: center;
                    background: var(--search-bg);
                    border-radius: 1.25rem;
                    padding: 0.3rem 0.8rem;
                    margin-left: 2rem;
                    flex-grow: 1;
                    max-width: 25rem;
                    transition: background 0.3s;
                }
                .search-bar svg {
                    stroke: var(--search-icon);
                }
                .search-bar input {
                    background: none;
                    border: none;
                    color: var(--text-color);
                    outline: none;
                    width: 100%;
                    font-size: 0.9rem;
                    margin-left: 0.5rem;
                }
                .search-bar input::placeholder {
                    color: var(--search-icon);
                }

                /* Dropdown styling */
                .nav-links {
                    display: flex;
                    align-items: center;
                    gap: 1.5rem;
                    margin-left: 2rem;
                    flex-shrink: 0;
                    white-space: nowrap;
                }
                .dropdown {
                    position: relative;
                    display: inline-block;
                }
                .dropbtn {
                    color: var(--text-color);
                    text-decoration: none;
                    font-size: 0.95rem;
                    font-weight: 500;
                    cursor: pointer;
                    transition: color 0.2s;
                    padding: 1.2rem 0;
                }
                .dropbtn:hover {
                    color: var(--text-hover);
                }
                .dropdown-content {
                    display: none;
                    position: absolute;
                    background-color: var(--dropdown-bg);
                    min-width: 13.75rem;
                    box-shadow: 0 0.5rem 1rem 0 rgba(0,0,0,0.15);
                    z-index: 1;
                    border: 1px solid var(--border-color);
                    border-radius: 0.25rem;
                    top: 100%;
                    left: 0;
                }
                .dropdown-content a {
                    color: var(--text-color);
                    padding: 0.75rem 1rem;
                    text-decoration: none;
                    display: block;
                    font-size: 0.9rem;
                    border-bottom: 1px solid var(--border-color);
                    transition: background-color 0.2s;
                }
                .dropdown-content a:last-child {
                    border-bottom: none;
                }
                .dropdown-content a:hover {
                    background-color: var(--dropdown-hover);
                    color: var(--text-hover);
                }
                .dropdown:hover .dropdown-content {
                    display: block;
                }

                /* Action buttons styling */
                .actions {
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                    margin-left: 2.5rem;
                    flex-shrink: 0;
                    white-space: nowrap;
                }
                .btn {
                    padding: 0.4rem 1rem;
                    border-radius: 0.25rem;
                    text-decoration: none;
                    font-size: 0.9rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: background 0.2s, color 0.2s, border-color 0.2s;
                }
                .btn-outline {
                    border: 1px solid var(--btn-outline-border);
                    color: var(--text-color);
                    background: transparent;
                }
                .btn-outline:hover {
                    background: var(--btn-outline-hover);
                }
                .btn-filled {
                    background: var(--btn-filled-bg);
                    color: var(--btn-filled-text);
                    border: 1px solid var(--btn-filled-bg);
                }
                .btn-filled:hover {
                    opacity: 0.9;
                }
                #theme-btn-toggle {
                    width: 9.375rem;
                    text-align: center;
                }
                .actions .dropdown-content {
                    min-width: 9.375rem;
                    left: auto;
                    right: 0;
                }

                /* Hamburger three-line styling (low width screen) */
                .hamburger {
                    display: none;
                    flex-direction: column;
                    cursor: pointer;
                    gap: 0.25rem;
                    padding: 0.3125rem;
                }
                .hamburger span {
                    display: block;
                    width: 1.25rem;
                    height: 0.125rem;
                    background-color: var(--hamburger-line);
                }
                
                /* Shading */
                .menu-backdrop {
                    position: fixed;
                    top: 3.75rem;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0, 0, 0, 0.4);
                    opacity: 0;
                    visibility: hidden;
                    transition: opacity 0.3s, visibility 0.3s;
                    z-index: 90;
                }
                .menu-backdrop.open {
                    opacity: 1;
                    visibility: visible;
                }

                /* Hamburger menu styling (low width screen) */
                .mobile-menu {
                    display: none;
                    flex-direction: column;
                    background-color: var(--dropdown-bg);
                    position: absolute;
                    top: 3.75rem;
                    right: 0;
                    width: 18.75rem;
                    padding: 1rem;
                    border-left: 1px solid var(--border-color);
                    border-bottom: 1px solid var(--border-color);
                    z-index: 100;
                    max-height: calc(100vh - 3.75rem);
                    overflow-y: auto;
                }
                .mobile-menu.open {
                    display: flex;
                }
                .mobile-menu .group-title {
                    color: var(--menu-group-title);
                    font-size: 0.8rem;
                    text-transform: uppercase;
                    padding: 1rem 0 0.2rem 0;
                    font-weight: 700;
                    text-decoration: none;
                    display: block;
                }
                .mobile-menu .group-title:hover {
                    color: var(--text-hover);
                }
                .mobile-menu a, .mobile-menu button {
                    color: var(--text-color);
                    text-decoration: none;
                    padding: 0.6rem 0;
                    font-size: 1rem;
                    background: none;
                    border: none;
                    border-bottom: 1px solid var(--border-color);
                    text-align: left;
                    font-family: inherit;
                    cursor: pointer;
                }
                .mobile-menu .sub-link {
                    padding-left: 1.5rem;
                    font-size: 0.95rem;
                }
                @media (max-width: 1100px) {
                    .nav-links, .search-bar, .actions {
                        display: none;
                    }
                    .hamburger {
                        display: flex;
                    }
                }
            </style>
            
            <header>
                <a href="${rootUrl}index.html" class="logo-container" id="brand-link">
                    <div class="logo"></div>
                    Web Projects
                </a>
                
                <div class="search-bar">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    <input type="text" placeholder="Search...">
                </div>

                <nav class="nav-links">
                    <div class="dropdown">
                        <a href="${rootUrl}major-projects/index.html" class="dropbtn">Major Projects</a>
                        <div class="dropdown-content">
                            <a href="${rootUrl}major-projects/aes-encryption/index.html">AES Encryption</a>
                            <a href="${rootUrl}major-projects/chess/index.html">Chess</a>
                            <a href="${rootUrl}major-projects/image-manipulation/index.html">Image Manipulation</a>
                            <a href="${rootUrl}major-projects/pathfinding-visualizer/index.html">Pathfinding Visualizer</a>
                            <a href="${rootUrl}major-projects/web-browser/index.html">Web Browser</a>
                        </div>
                    </div>
                    
                    <div class="dropdown">
                        <a href="${rootUrl}medium-projects/index.html" class="dropbtn">Medium Projects</a>
                        <div class="dropdown-content">
                            <a href="${rootUrl}medium-projects/markdown-to-html/index.html">Markdown to HTML</a>
                            <a href="${rootUrl}medium-projects/pixel-art-editor/index.html">Pixel Art Editor</a>
                            <a href="${rootUrl}medium-projects/typing-test/index.html">Typing Test</a>
                        </div>
                    </div>

                    <div class="dropdown">
                        <a href="${rootUrl}mini-projects/index.html" class="dropbtn">Mini Projects</a>
                        <div class="dropdown-content">
                            <a href="${rootUrl}mini-projects/bill-calculator.html">Bill Calculator</a>
                            <a href="${rootUrl}mini-projects/clock.html">Clock</a>
                            <a href="${rootUrl}mini-projects/palindrome-checker.html">Palindrome Checker</a>
                            <a href="${rootUrl}mini-projects/random-background.html">Random Background</a>
                            <a href="${rootUrl}mini-projects/task-manager.html">Task Manager</a>
                        </div>
                    </div>

                    <div class="dropdown">
                        <a href="${rootUrl}tech-demo/index.html" class="dropbtn">Tech Demos</a>
                        <div class="dropdown-content">
                            <a href="${rootUrl}tech-demo/informal-report/index.html">Informal Report</a>
                            <a href="${rootUrl}tech-demo/image-extractor/index.html">Image Extractor</a>
                            <a href="${rootUrl}tech-demo/sample-bfs/index.html">Sample BFS</a>
                        </div>
                    </div>
                </nav>

                <div class="actions">
                    <div class="dropdown">
                        <button class="btn btn-outline" id="theme-btn-toggle">Theme: System</button>
                        <div class="dropdown-content">
                            <a href="#" class="theme-option" data-theme="system">OS Default</a>
                            <a href="#" class="theme-option" data-theme="light">Light Mode</a>
                            <a href="#" class="theme-option" data-theme="dark">Dark Mode</a>
                        </div>
                    </div>
                    <a href="https://github.com/wenbo222/website-projects" target="_blank" class="btn btn-filled">GitHub</a>
                </div>

                <div class="hamburger" id="menu-toggle">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </header>

            <div class="menu-backdrop" id="menu-backdrop"></div>

            <div class="mobile-menu" id="mobile-menu">
                <a href="${rootUrl}major-projects/index.html" class="group-title">Major Projects</a>
                <a class="sub-link" href="${rootUrl}major-projects/aes-encryption/index.html">AES Encryption</a>
                <a class="sub-link" href="${rootUrl}major-projects/chess/index.html">Chess</a>
                <a class="sub-link" href="${rootUrl}major-projects/image-manipulation/index.html">Image Manipulation</a>
                <a class="sub-link" href="${rootUrl}major-projects/pathfinding-visualizer/index.html">Pathfinding Visualizer</a>
                <a class="sub-link" href="${rootUrl}major-projects/web-browser/index.html">Web Browser</a>

                <a href="${rootUrl}medium-projects/index.html" class="group-title">Medium Projects</a>
                <a class="sub-link" href="${rootUrl}medium-projects/markdown-to-html/index.html">Markdown to HTML</a>
                <a class="sub-link" href="${rootUrl}medium-projects/pixel-art-editor/index.html">Pixel Art Editor</a>
                <a class="sub-link" href="${rootUrl}medium-projects/typing-test/index.html">Typing Test</a>

                <a href="${rootUrl}mini-projects/index.html" class="group-title">Mini Projects</a>
                <a class="sub-link" href="${rootUrl}mini-projects/bill-calculator.html">Bill Calculator</a>
                <a class="sub-link" href="${rootUrl}mini-projects/clock.html">Clock</a>
                <a class="sub-link" href="${rootUrl}mini-projects/palindrome-checker.html">Palindrome Checker</a>
                <a class="sub-link" href="${rootUrl}mini-projects/random-background.html">Random Background</a>
                <a class="sub-link" href="${rootUrl}mini-projects/task-manager.html">Task Manager</a>
                
                <a href="${rootUrl}tech-demo/index.html" class="group-title">Tech Demos</a>
                <a class="sub-link" href="${rootUrl}tech-demo/informal-report/index.html">Informal Report</a>
                <a class="sub-link" href="${rootUrl}tech-demo/image-extractor/index.html">Image Extractor</a>
                <a class="sub-link" href="${rootUrl}tech-demo/sample-bfs/index.html">Sample BFS</a>

                <div class="group-title">Site Settings</div>
                <button class="sub-link mobile-theme-btn" data-theme="system">Theme: System</button>
                <button class="sub-link mobile-theme-btn" data-theme="light">Theme: Light</button>
                <button class="sub-link mobile-theme-btn" data-theme="dark">Theme: Dark</button>
                <a class="sub-link" href="https://github.com/wenbo222/website-projects" target="_blank">GitHub</a>
            </div>
        `;

        /** Toggles the mobile menu and backdrop */
        const toggleMenu = () => {
            menu.classList.toggle('open');
            backdrop.classList.toggle('open');
        }

        /** Applies the selected theme 
         * @param {string} mode - The theme mode to apply ('light', 'dark', or 'system')
        */
        const applyTheme = (mode) => {
            let isDark = true;
            if (mode==='light') {
                isDark = false;
            } else if (mode==='system') {
                isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            }

            document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
            this.setAttribute('data-theme', isDark ? 'dark' : 'light'); 
            const labelMap = {light: 'Light', dark: 'Dark', system: 'System'};
            themeBtnToggle.textContent = 'Theme: '+labelMap[mode];
        }

        /** Switches the theme 
         * @param {string} mode - The theme mode to switch to ('light', 'dark', or 'system')
         * @param {Event} e - The event that caused the theme switch
        */
        const switchTheme = (mode, e) => {
            if (e) e.preventDefault();
            currentMode = mode;
            localStorage.setItem('global-theme', mode);
            applyTheme(mode);
        };

        const toggle = this.shadowRoot.getElementById('menu-toggle');
        const menu = this.shadowRoot.getElementById('mobile-menu');
        const backdrop = this.shadowRoot.getElementById('menu-backdrop');
        const themeBtnToggle = this.shadowRoot.getElementById('theme-btn-toggle');
        const desktopOptions = this.shadowRoot.querySelectorAll('.theme-option');
        const mobileOptions = this.shadowRoot.querySelectorAll('.mobile-theme-btn');
        let currentMode = localStorage.getItem('global-theme') || 'system';

        // Hamburger Menu Logic
        toggle.addEventListener('click', toggleMenu);
        backdrop.addEventListener('click', toggleMenu);

        // Theme Switcher Logic
        desktopOptions.forEach(opt => {
            opt.addEventListener('click', (e) => switchTheme(opt.dataset.theme, e));
        });
        mobileOptions.forEach(opt => {
            opt.addEventListener('click', (e) => {
                switchTheme(opt.dataset.theme, e);
                menu.classList.remove('open');
                backdrop.classList.remove('open');
            });
        });

        // Initial application and OS listener
        applyTheme(currentMode);
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
            if (currentMode==='system') {
                applyTheme('system');
            }
        });

        // Close mobile menu if window is resized beyond the mobile breakpoint
        window.matchMedia('(max-width: 1100px)').addEventListener('change', (e) => {
            if (!e.matches) {
                menu.classList.remove('open');
                backdrop.classList.remove('open');
            }
        });

        // Sync theme across multiple tabs instantly
        window.addEventListener('storage', (e) => {
            if (e.key==='global-theme') {
                currentMode = e.newValue || 'system';
                applyTheme(currentMode);
            }
        });
    }
}

customElements.define('global-header', GlobalHeader);
