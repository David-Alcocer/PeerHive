// ===============================
// Panel Asesor (UI) - Refactored
// ===============================

import { appState, getCurrentUser } from '../store/state.js';
import { escapeHtml, showToast, setButtonLoading } from '../utils/helpers.js';
import { UserService } from '../services/user.service.js';
import { RequestService } from '../services/request.service.js';
import { SessionService } from '../services/session.service.js';
import { assignRequestToAdvisor } from './requests.js';

export function initAdvisor() {
    const formSubjects = document.getElementById('form-subjects');
    const subjectsSubmitBtn = document.getElementById('subjects-submit-btn');

    formSubjects?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const user = getCurrentUser();
        if (!user) return;

        setButtonLoading(subjectsSubmitBtn, true);

        try {
            const checks = formSubjects.querySelectorAll('input[type=checkbox]');
            const subjects = Array.from(checks)
                .filter(c => c.checked)
                .map(c => c.value);

            await UserService.updateAdvisorSubjects(user.id, subjects);
            showToast('Materias guardadas exitosamente', 'success');
            renderAdvisorPanel();
        } catch (error) {
            showToast(error.message, 'error');
        } finally {
            setButtonLoading(subjectsSubmitBtn, false);
        }
    });
}

export function renderAdvisorPanel() {
    const formSubjects = document.getElementById('form-subjects');
    const listAdvisorRequests = document.getElementById('list-advisor-requests');
    const listAdvisorSessions = document.getElementById('list-advisor-sessions');
    const user = getCurrentUser();

    if (!user || (user.role !== 'advisor' && user.role !== 'admin')) {
        [listAdvisorRequests, listAdvisorSessions].forEach(el => {
            if (el) el.innerHTML = '<div class="muted small">Disponible solo para asesores y admin.</div>';
        });
        return;
    }

    try {
        // Hydrate checkboxes
        const checks = formSubjects?.querySelectorAll('input[type=checkbox]');
        checks?.forEach(c => {
            c.checked = (user.subjects || []).includes(c.value);
        });

        // Relevant Requests (Pool)
        if (listAdvisorRequests) {
            listAdvisorRequests.innerHTML = '';

            // Should probably amove this specific filter to RequestService but keeping it simple for now
            const mySubjects = user.subjects || [];
            const relevantRequests = user.role === 'admin'
                ? appState.requests
                : appState.requests.filter(r => {
                    const subjectMatch = mySubjects.length ? mySubjects.includes(r.subject) : true;
                    return subjectMatch && (!r.advisorId || r.advisorId === user.id);
                });

            if (!relevantRequests.length) {
                listAdvisorRequests.innerHTML = '<div class="muted small">No hay solicitudes pendientes relevantes.</div>';
            } else {
                relevantRequests
                    .sort((a, b) => new Date(a.datetimeISO) - new Date(b.datetimeISO))
                    .forEach(req => {
                        const student = appState.users.find(u => u.id === req.studentId);
                        const li = document.createElement('div');
                        li.className = 'list-item';
                        li.innerHTML = `
                          <div class="list-header">
                            <span><b>${escapeHtml(req.subject)}</b> · ${escapeHtml(req.topic)}</span>
                            <span class="badge status-${req.status}">${req.status}</span>
                          </div>
                          <div class="mt-8 small">${new Date(req.datetimeISO).toLocaleString()}</div>
                          <div class="mt-8 small muted">Estudiante: ${student ? escapeHtml(student.name) : '...'}</div>
                        `;

                        if (req.status === 'pendiente') {
                            const btn = document.createElement('button');
                            btn.textContent = 'Aceptar y agendar';
                            btn.className = 'btn primary mt-8';
                            btn.addEventListener('click', () => assignRequestToAdvisor(req.id, user.id));
                            li.appendChild(btn);
                        }
                        listAdvisorRequests.appendChild(li);
                    });
            }
        }

        // Sessions
        if (listAdvisorSessions) {
            listAdvisorSessions.innerHTML = '';
            const mySessions = SessionService.getVisibleSessionsForUser(user).filter(s => s.advisorId === user.id || user.role === 'admin');

            if (!mySessions.length) {
                listAdvisorSessions.innerHTML = '<div class="muted small">Aún no tienes sesiones.</div>';
            } else {
                mySessions
                    .sort((a, b) => new Date(a.datetimeISO) - new Date(b.datetimeISO))
                    .forEach(ses => {
                        const student = appState.users.find(u => u.id === ses.studentId);
                        const li = document.createElement('div');
                        li.className = 'list-item';
                        li.innerHTML = `
                          <div class="list-header">
                            <span><b>${new Date(ses.datetimeISO).toLocaleString()}</b></span>
                            <span class="badge status-${ses.status}">${ses.status}</span>
                          </div>
                          <div class="mt-8 small muted">Estudiante: ${student ? escapeHtml(student.name) : '...'}</div>
                          <div class="mt-8 small"><a href="${ses.teamsLink}" target="_blank">Canal Teams</a></div>
                        `;
                        listAdvisorSessions.appendChild(li);
                    });
            }
        }
    } catch (error) {
        console.error('Error rendering advisor panel:', error);
    }
}
