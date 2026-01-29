// ===============================
// Router y UI General
// ===============================

import { appState, getCurrentUser, setChatId, globalState } from '../store/state.js';
import { showToast } from '../utils/helpers.js';

// Imports de renderers
import { renderDashboard, updateSystemStats } from './dashboard.js';
import { renderRequests } from './requests.js';
import { renderCalendarEvents, initCalendar } from './calendar.js';
import { renderAdvisorPanel } from './advisor.js';
import { renderChatList, renderChatMessages } from './chat.js';
import { hydrateSettings } from './settings.js';
import { renderReports } from './admin.js';

export function switchView(viewId) {
    try {
        document.querySelectorAll('.view').forEach(v => {
            v.hidden = v.id !== viewId;
        });

        document.querySelectorAll('.nav-btn').forEach(btn => {
            const target = btn.getAttribute('data-view');
            if (!target) return;
            btn.classList.toggle('active', target === viewId);
        });

        // Renderizado específico por vista
        const viewRenderers = {
            'view-dashboard': renderDashboard,
            'view-requests': renderRequests,
            'view-calendar': renderCalendarEvents,
            'view-advisor': renderAdvisorPanel,
            'view-chat': () => {
                renderChatList();
                // Si hay chat activo, renderizar mensajes?
                if (globalState.currentChatId) {
                    renderChatMessages();
                }
            },
            'view-settings': hydrateSettings,
            'view-reports': renderReports
        };

        if (viewRenderers[viewId]) {
            viewRenderers[viewId]();
        }
    } catch (error) {
        console.error('Error switching view:', error);
        showToast('Error al cambiar de vista', 'error');
    }
}

export function updateTopbarUser() {
    const topbarUser = document.getElementById('topbar-user');
    const avatarInitials = document.getElementById('avatar-initials');
    const userNameEl = document.getElementById('user-name');
    const userEmailEl = document.getElementById('user-email');
    const userRoleEl = document.getElementById('user-role');

    try {
        const user = getCurrentUser();

        // Control de visibilidad de botones Admin
        document.querySelectorAll('.nav-admin-only').forEach(btn => {
            btn.style.display = (user && user.role === 'admin') ? 'grid' : 'none';
        });

        if (!user) {
            if (topbarUser) topbarUser.hidden = true;
            return;
        }

        if (topbarUser) topbarUser.hidden = false;
        if (userNameEl) userNameEl.textContent = user.name;
        if (userEmailEl) userEmailEl.textContent = user.email;
        if (userRoleEl) {
            userRoleEl.textContent = user.role === 'admin' ? 'Administrador' :
                user.role === 'advisor' ? 'Asesor' : 'Estudiante';
        }

        if (avatarInitials) {
            const initials = (user.name || user.email)
                .split(' ')
                .map(p => p[0] || '')
                .join('')
                .slice(0, 2)
                .toUpperCase();
            avatarInitials.textContent = initials;
        }
    } catch (error) {
        console.error('Error updating topbar:', error);
    }
}

export function showMainApp() {
    const authScreen = document.getElementById('auth-screen');
    const app = document.querySelector('.app');

    if (authScreen) authScreen.style.display = 'none';
    if (app) app.style.display = 'grid';

    const user = getCurrentUser();
    if (user) {
        updateTopbarUser();
        switchView('view-dashboard');
        renderDashboard();
        renderRequests();
        renderAdvisorPanel();
        renderCalendarEvents();
        // No hace falta renderizar chat hasta que entre
    }
}

export function logout() {
    appState.currentUserId = null;
    setChatId(null);

    const authScreen = document.getElementById('auth-screen');
    const app = document.querySelector('.app');

    if (app) app.style.display = 'none';
    if (authScreen) authScreen.style.display = 'flex';

    updateSystemStats();
    showToast('Sesión cerrada', 'info');
}

export function initNavigation() {
    document.querySelectorAll('.nav-btn').forEach(btn => {
        const view = btn.getAttribute('data-view');
        if (!view) return;

        btn.addEventListener('click', () => {
            const user = getCurrentUser();
            if (!user && view !== 'view-login') {
                showToast('Inicia sesión para acceder a esta sección', 'warning');
                logout(); // Force logout/login screen
                return;
            }

            if (view === 'view-advisor' && (!user || (user.role !== 'advisor' && user.role !== 'admin'))) {
                showToast('Solo asesores o administrador pueden ver el panel asesor', 'warning');
                return;
            }

            if (view === 'view-reports' && (!user || user.role !== 'admin')) {
                showToast('Solo el administrador puede ver los reportes', 'warning');
                return;
            }

            switchView(view);
        });
    });

    document.getElementById('btn-logout')?.addEventListener('click', logout);
}
