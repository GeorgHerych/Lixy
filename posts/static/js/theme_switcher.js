const themeToggle = document.getElementById('theme-toggle');
const themeLink = document.getElementById('theme-link');

const themeKey = 'theme';

let currentTheme = localStorage.getItem(themeKey) || 'light';

function toggleTheme() {
    if (currentTheme === 'light') {
        currentTheme = 'dark';
        themeLink.href = '/static/css/styles_dark.css';
    } else {
        currentTheme = 'light';
        themeLink.href = '/static/css/styles_light.css';
    }

    localStorage.setItem(themeKey, currentTheme);
}

function initializeTheme() {
    if (currentTheme === 'dark') {
        themeLink.href = '/static/css/styles_dark.css';
    } else {
        themeLink.href = '/static/css/styles_light.css';
    }
}

// Ініціалізація теми
initializeTheme();

// Вішаємо обробник на кнопку
themeToggle.addEventListener('click', toggleTheme);