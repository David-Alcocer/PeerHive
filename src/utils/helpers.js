// ===============================
// Utilidades Generales
// ===============================

import { TEAMS_CHANNEL_URL } from '../api/config.js';

export function hashPassword(password) {
    return btoa(password + '_peerhive_salt_demo_v2');
}

export function uid(prefix = "id") {
    return prefix + "_" + Math.random().toString(36).slice(2, 9) + "_" + Date.now().toString(36);
}

export function verifyPassword(input, stored) {
    return hashPassword(input) === stored;
}

export function generateTeamsChannelLink() {
    return TEAMS_CHANNEL_URL;
}

// UI Helpers
export function showToast(message, type = 'info') {
    try {
        // Asumimos que Swal está en el objeto global windows (CDN)
        if (window.Swal) {
            window.Swal.fire({
                toast: true,
                position: 'top-end',
                icon: type,
                title: message,
                showConfirmButton: false,
                timer: 1800,
                timerProgressBar: true,
            });
        } else {
            console.warn('SweetAlert2 not loaded');
            alert(message);
        }
    } catch (error) {
        console.error('Error showing toast:', error);
        alert(message);
    }
}

export function setButtonLoading(button, isLoading) {
    if (!button) return;

    if (isLoading) {
        button.disabled = true;
        button.classList.add('loading');
    } else {
        button.disabled = false;
        button.classList.remove('loading');
    }
}

export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

export function escapeHtml(unsafe) {
    if (typeof unsafe !== 'string') return unsafe;
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
