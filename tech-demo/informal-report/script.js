const toggleBtn = document.getElementById('toggle-version');
const detailedVersion = document.getElementById('detailed-version');
const simpleVersion = document.getElementById('simple-version');

toggleBtn.addEventListener('click', () => {
    if (detailedVersion.style.display==='none') {
        detailedVersion.style.display = 'block';
        simpleVersion.style.display = 'none';
        toggleBtn.textContent = 'Switch to Less Detailed Version';
    } else {
        detailedVersion.style.display = 'none';
        simpleVersion.style.display = 'block';
        toggleBtn.textContent = 'Switch to More Detailed Version';
    }
});