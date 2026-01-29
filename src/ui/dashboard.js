// ===============================
// Dashboard (UI) - Refactored
// ===============================

import { appState, getCurrentUser } from '../store/state.js';
import { SessionService } from '../services/session.service.js';
import { UserService } from '../services/user.service.js';
import { escapeHtml } from '../utils/helpers.js';

export function renderDashboard() {
  const user = getCurrentUser();
  if (!user) return;

  const cardRequests = document.getElementById('card-requests');
  const cardSessions = document.getElementById('card-sessions');
  const cardRole = document.getElementById('card-role');
  const upcomingSessions = document.getElementById('upcoming-sessions');

  try {
    if (cardRole) {
      cardRole.innerHTML = `
                <h3>Rol actual</h3>
                <p class="mt-8 small"><b>${user.role.toUpperCase()}</b></p>
                ${user.role === 'advisor' && !user.isAdvisorApproved ? '<p class="mt-8 small badge status-pendiente">En revisión</p>' : ''}
            `;
    }

    if (cardRequests) {
      const myRequests = user.role === 'student' ? appState.requests.filter(r => r.studentId === user.id) : appState.requests;
      cardRequests.innerHTML = `
                <h3>Solicitudes</h3>
                <p class="mt-8 small">Total: <b>${myRequests.length}</b></p>
            `;
    }

    if (cardSessions) {
      const mySessions = SessionService.getVisibleSessionsForUser(user);
      cardSessions.innerHTML = `
                <h3>Sesiones</h3>
                <p class="mt-8 small">Total: <b>${mySessions.length}</b></p>
            `;
    }

    if (upcomingSessions) {
      upcomingSessions.innerHTML = '';
      const future = SessionService.getUpcomingSessions(user);

      if (!future.length) {
        upcomingSessions.innerHTML = '<div class="muted small">No hay sesiones próximas.</div>';
      } else {
        future.forEach(ses => {
          const req = appState.requests.find(r => r.id === ses.requestId);
          const div = document.createElement('div');
          div.className = 'list-item';
          div.innerHTML = `
                        <div class="list-header">
                          <span><b>${req ? escapeHtml(req.subject) : 'Sesión'}</b></span>
                          <span class="badge status-${ses.status}">${ses.status}</span>
                        </div>
                        <div class="mt-8 small">${new Date(ses.datetimeISO).toLocaleString()}</div>
                    `;
          upcomingSessions.appendChild(div);
        });
      }
    }
  } catch (e) { console.error('Error rendering dashboard:', e); }
}

export function updateSystemStats() {
  const systemStats = document.getElementById('system-stats');
  if (!systemStats) return;

  try {
    const stats = UserService.getSystemStats();
    systemStats.innerHTML = `
            <li>Total usuarios: <b>${stats.totalUsers}</b></li>
            <li>Solicitudes registradas: <b>${stats.totalRequests}</b></li>
            <li>Sesiones agendadas: <b>${stats.totalSessions}</b></li>
            ${stats.pendingAdvisors > 0 ? `<li>Asesores pendientes: <b>${stats.pendingAdvisors}</b></li>` : ''}
        `;
  } catch (e) { console.error(e); }
}
