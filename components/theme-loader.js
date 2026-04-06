const savedTheme = localStorage.getItem('global-theme') || 'system';
if (savedTheme==='dark' || (savedTheme==='system' && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.setAttribute('data-theme', 'dark');
} else {
    document.documentElement.setAttribute('data-theme', 'light');
}
