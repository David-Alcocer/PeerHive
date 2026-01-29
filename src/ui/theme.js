// ===============================
// Gestión de Tema
// ===============================

import { THEME_KEY } from '../api/config.js';

export function loadTheme() {
    try {
        const stored = localStorage.getItem(THEME_KEY);
        if (stored === 'dark' || stored === 'light') return stored;

        // Detección de preferencia del sistema
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
            return 'light';
        }
        return 'dark';
    } catch (error) {
        return 'dark';
    }
}

export function applyTheme(theme) {
    try {
        document.documentElement.dataset.theme = theme;
        localStorage.setItem(THEME_KEY, theme);

        const toggle = document.getElementById('theme-toggle');
        if (!toggle) return;

        const icon = toggle.querySelector('i');
        const label = toggle.querySelector('span');

        // Verificación defensiva por si el DOM no está listo o los elementos cambiaron
        if (icon) {
            if (theme === 'dark') {
                icon.className = 'fa-regular fa-sun';
            } else {
                icon.className = 'fa-regular fa-moon';
            }
        }

        if (label) {
            label.textContent = theme === 'dark' ? 'Claro' : 'Oscuro';
        }

    } catch (error) {
        console.error('Error applying theme:', error);
    }
}

export function initTheme() {
    const current = loadTheme();
    applyTheme(current);

    const toggle = document.getElementById('theme-toggle');
    if (toggle) {
        // Remover listeners previos para evitar duplicados si se llama initTheme varias veces
        // (Aunque con módulos esto es menos probable, es buena práctica)
        const newToggle = toggle.cloneNode(true);
        toggle.parentNode.replaceChild(newToggle, toggle);

        newToggle.addEventListener('click', () => {
            const current = loadTheme();
            const next = current === 'light' ? 'dark' : 'light';
            applyTheme(next);
        });
    }
}
