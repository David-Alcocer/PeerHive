// ===============================
// Administración (UI) - Refactored
// ===============================

import { appState, getCurrentUser } from '../store/state.js';
import { escapeHtml, showToast, debounce } from '../utils/helpers.js';
import { UserService } from '../services/user.service.js';

export function renderReports() {
    const reportsList = document.getElementById('reports-list');
    const user = getCurrentUser();

    if (!user || user.role !== 'admin') {
        if (reportsList) reportsList.innerHTML = '<div class="muted small">Solo el administrador puede ver esta sección.</div>';
        return;
    }

    try {
        if (reportsList) {
            const stats = UserService.getSystemStats();
            reportsList.innerHTML = `
                <div class="list-item"><b>Usuarios registrados:</b> ${stats.totalUsers}</div>
                <div class="list-item"><b>Solicitudes totales:</b> ${stats.totalRequests}</div>
                <div class="list-item"><b>Sesiones agendadas:</b> ${stats.totalSessions}</div>
                ${stats.pendingAdvisors > 0 ? `<div class="list-item"><b>Asesores pendientes:</b> ${stats.pendingAdvisors}</div>` : ''}
            `;
        }

        renderAdvisorRequestsAdmin();
        renderContacts();
    } catch (error) {
        console.error('Error rendering reports:', error);
    }
}

export function renderAdvisorRequestsAdmin() {
    const advisorRequestsListAdmin = document.getElementById('advisor-requests-list');
    if (!advisorRequestsListAdmin) return;

    const user = getCurrentUser();
    if (!user || user.role !== 'admin') { advisorRequestsListAdmin.innerHTML = ''; return; }

    try {
        const pendingAdvisors = appState.users.filter(u => u.role === 'advisor' && !u.isAdvisorApproved);
        advisorRequestsListAdmin.innerHTML = '';

        if (!pendingAdvisors.length) {
            advisorRequestsListAdmin.innerHTML = '<div class="muted small">No hay solicitudes de asesor pendientes.</div>';
            return;
        }

        pendingAdvisors.forEach(u => {
            const div = document.createElement('div');
            div.className = 'list-item';
            div.innerHTML = `
                <div class="list-header">
                  <span><b>${escapeHtml(u.name)}</b></span>
                  <span class="badge">Asesor (pendiente)</span>
                </div>
                <div class="mt-8 small">${u.email}</div>
                <div class="mt-8 small muted">Materia: ${escapeHtml(u.advisorSubject || 'N/A')}</div>
                <div class="row-right mt-8">
                  <button class="btn secondary btn-compact" data-action="reject">Rechazar</button>
                  <button class="btn primary btn-compact" data-action="approve">Aprobar</button>
                </div>
            `;

            div.querySelector('[data-action="approve"]').addEventListener('click', () => {
                UserService.approveAdvisor(u.id);
                showToast('Asesor aprobado exitosamente', 'success');
                renderReports();
            });

            div.querySelector('[data-action="reject"]').addEventListener('click', async () => {
                const result = await window.Swal.fire({
                    title: '¿Rechazar solicitud?',
                    text: 'El usuario será convertido en estudiante.',
                    icon: 'warning',
                    showCancelButton: true
                });
                if (result.isConfirmed) {
                    UserService.rejectAdvisor(u.id);
                    showToast('Solicitud rechazada', 'info');
                    renderReports();
                }
            });

            advisorRequestsListAdmin.appendChild(div);
        });
    } catch (error) { console.error(error); }
}

const debouncedRenderContacts = debounce((query) => renderContacts(query), 300);

export function initContactsSearch() {
    document.getElementById('contact-search')?.addEventListener('input', (e) => debouncedRenderContacts(e.target.value));
}

export function renderContacts(filterText = '') {
    const contactList = document.getElementById('contact-list');
    const user = getCurrentUser();
    if (!user || user.role !== 'admin' || !contactList) return;

    try {
        contactList.innerHTML = '';
        const query = filterText.trim().toLowerCase() || (document.getElementById('contact-search')?.value || '').trim().toLowerCase();

        const filtered = appState.users.filter(u =>
            !query || u.name.toLowerCase().includes(query) || u.email.toLowerCase().includes(query) || u.role.toLowerCase().includes(query)
        );

        if (!filtered.length) {
            contactList.innerHTML = '<div class="muted small">No se encontraron usuarios.</div>';
            return;
        }

        filtered.forEach(u => {
            const isCurrentUser = u.id === user.id;
            const div = document.createElement('div');
            div.className = 'list-item contact-item';
            div.innerHTML = `
                <div class="list-header">
                    <div><strong>${escapeHtml(u.name)}</strong> <span class="badge">${u.role}</span></div>
                    ${!isCurrentUser ? `
                        <div class="contact-actions">
                            <select class="role-select" data-id="${u.id}">
                                <option value="student" ${u.role === 'student' ? 'selected' : ''}>Estudiante</option>
                                <option value="advisor" ${u.role === 'advisor' ? 'selected' : ''}>Asesor</option>
                                <option value="admin" ${u.role === 'admin' ? 'selected' : ''}>Administrador</option>
                            </select>
                            <button class="btn-compact delete" data-id="${u.id}"><i class="fa-solid fa-trash"></i></button>
                        </div>
                    ` : '<span class="muted small">Tú</span>'}
                </div>
                <div class="small muted">${u.email}</div>
            `;

            if (!isCurrentUser) {
                div.querySelector('.role-select').addEventListener('change', (e) => {
                    UserService.changeUserRole(u.id, e.target.value);
                    showToast('Rol actualizado', 'success');
                    renderContacts();
                });
                div.querySelector('.delete').addEventListener('click', async () => {
                    const res = await window.Swal.fire({ title: '¿Eliminar?', icon: 'warning', showCancelButton: true });
                    if (res.isConfirmed) {
                        UserService.deleteUser(u.id);
                        showToast('Usuario eliminado', 'info');
                        renderContacts();
                        renderReports();
                    }
                });
            }
            contactList.appendChild(div);
        });
    } catch (e) { console.error(e); }
}
