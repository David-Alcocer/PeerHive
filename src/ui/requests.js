// ===============================
// Solicitudes (UI) - Refactored
// ===============================

import { appState, getCurrentUser } from '../store/state.js';
import {
    escapeHtml,
    showToast,
    setButtonLoading
} from '../utils/helpers.js';

// Import de Servicio
import { RequestService } from '../services/request.service.js';

import { renderDashboard } from './dashboard.js';
import { renderAdvisorPanel } from './advisor.js';
import { renderCalendarEvents } from './calendar.js';
import { renderChatList, renderChatMessages } from './chat.js';
import { switchView } from './router.js';

export function initRequests() {
    const formRequest = document.getElementById('form-request');
    const requestSubmitBtn = document.getElementById('request-submit-btn');

    formRequest?.addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = requestSubmitBtn;
        setButtonLoading(submitBtn, true);

        try {
            const user = getCurrentUser();
            if (!user || (user.role !== 'student' && user.role !== 'admin')) {
                showToast('Solo estudiantes o administrador pueden crear solicitudes', 'error');
                return;
            }

            const subject = document.getElementById('req-subject').value.trim();
            const topic = document.getElementById('req-topic').value.trim();
            const datetimeISO = document.getElementById('req-datetime').value;
            const notes = document.getElementById('req-notes').value.trim();

            if (!subject || !topic || !datetimeISO) {
                showToast('Completa los campos requeridos', 'warning');
                return;
            }

            const selectedDate = new Date(datetimeISO);
            if (selectedDate < new Date()) {
                showToast('La fecha y hora deben ser futuras', 'error');
                return;
            }

            // Delegar creación al servicio
            await RequestService.create({
                studentId: user.id,
                subject,
                topic,
                datetimeISO,
                notes
            });

            if (formRequest) formRequest.reset();
            showToast('Solicitud creada exitosamente', 'success');

            renderRequests();
            renderDashboard();

        } catch (error) {
            console.error('Error creating request:', error);
            showToast('Error al crear la solicitud', 'error');
        } finally {
            setButtonLoading(submitBtn, false);
        }
    });
}

export function renderRequests() {
    const listMyRequests = document.getElementById('list-my-requests');
    const user = getCurrentUser();
    if (!user) return;

    try {
        const myRequests = RequestService.getAllForUser(user);

        // Mis solicitudes (Student view)
        if (listMyRequests) {
            listMyRequests.innerHTML = '';

            // Filter locally for "My Created Requests" if user is student
            const studentReqs = user.role === 'student' || user.role === 'admin'
                ? appState.requests.filter(r => r.studentId === user.id)
                : [];

            if (!studentReqs.length) {
                listMyRequests.innerHTML = '<div class="muted small">Aún no tienes solicitudes.</div>';
            } else {
                studentReqs
                    .sort((a, b) => new Date(a.datetimeISO) - new Date(b.datetimeISO))
                    .forEach(req => {
                        const li = document.createElement('div');
                        li.className = 'list-item';
                        li.innerHTML = `
                          <div class="list-header">
                            <span><b>${escapeHtml(req.subject)}</b> · ${escapeHtml(req.topic)}</span>
                            <span class="badge status-${req.status}">
                              ${req.status.charAt(0).toUpperCase() + req.status.slice(1)}
                            </span>
                          </div>
                          <div class="mt-8 small">
                            ${new Date(req.datetimeISO).toLocaleString()}
                          </div>
                          ${req.notes ? `<div class="mt-8 small muted">${escapeHtml(req.notes)}</div>` : ''}
                        `;
                        listMyRequests.appendChild(li);
                    });
            }
        }

        // Todas las solicitudes (Advisor/Admin Global View)
        const cardGlobalRequests = document.getElementById('card-global-requests');
        const listAllRequests = document.getElementById('list-all-requests');

        if (cardGlobalRequests) {
            if (user.role !== 'advisor' && user.role !== 'admin') {
                cardGlobalRequests.style.display = 'none';
            } else {
                cardGlobalRequests.style.display = 'block';

                if (listAllRequests) {
                    listAllRequests.innerHTML = '';

                    // Logic for "Available Requests Pool" or "My Assigned Requests"
                    // Ideally Service should provide this specific list
                    const poolRequests = appState.requests; // Admin/Advisor can see all to pick from or manage

                    if (!poolRequests.length) {
                        listAllRequests.innerHTML = '<div class="muted small">Aún no hay solicitudes.</div>';
                    } else {
                        poolRequests
                            .slice()
                            .sort((a, b) => new Date(a.datetimeISO) - new Date(b.datetimeISO))
                            .forEach(req => {
                                const student = appState.users.find(u => u.id === req.studentId);
                                const advisor = req.advisorId && appState.users.find(u => u.id === req.advisorId);

                                const li = document.createElement('div');
                                li.className = 'list-item';

                                li.innerHTML = `
                                    <div class="list-header">
                                      <span><b>${escapeHtml(req.subject)}</b> · ${escapeHtml(req.topic)}</span>
                                      <span class="badge status-${req.status}">
                                        ${req.status.charAt(0).toUpperCase() + req.status.slice(1)}
                                      </span>
                                    </div>
                                    <div class="mt-8 small">
                                      ${new Date(req.datetimeISO).toLocaleString()}
                                    </div>
                                    <div class="mt-8 small muted">
                                      Estudiante: ${student ? escapeHtml(student.name) : 'Desconocido'}
                                    </div>
                                    <div class="mt-8 small muted">
                                      Asesor: ${advisor ? escapeHtml(advisor.name) : 'Sin asignar'}
                                    </div>
                                `;

                                if (req.status === 'pendiente' && (user.role === 'advisor' || user.role === 'admin')) {
                                    const btn = document.createElement('button');
                                    btn.textContent = 'Aceptar y agendar';
                                    btn.className = 'btn primary mt-8';
                                    btn.addEventListener('click', () => {
                                        assignRequestToAdvisor(req.id, user.id);
                                    });
                                    li.appendChild(btn);
                                }

                                listAllRequests.appendChild(li);
                            });
                    }
                }
            }
        }

        renderAdvisorPanel();
    } catch (error) {
        console.error('Error rendering requests:', error);
    }
}

export async function assignRequestToAdvisor(requestId, advisorId) {
    try {
        await RequestService.assignAdvisor(requestId, advisorId);

        showToast('Solicitud asignada, sesión agendada y chat creado', 'success');

        renderRequests();
        renderAdvisorPanel();
        renderCalendarEvents();
        renderChatList();
        renderChatMessages();

        switchView('view-chat');
    } catch (error) {
        console.error('Error assigning request:', error);
        showToast(error.message || 'Error al procesar la solicitud', 'error');
    }
}
