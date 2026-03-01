// ===============================
// Calendario (UI) - Refactored
// ===============================

import { appState, getCurrentUser } from '../store/state.js';
import { escapeHtml } from '../utils/helpers.js';
import { SessionService } from '../services/session.service.js';
import { RequestService } from '../services/request.service.js';
import { API_BASE_URL } from '../api/config.js';

let calendar;

export function initCalendar() {
    const calendarEl = document.getElementById('calendar');
    if (!calendarEl) return;

    try {
        if (typeof FullCalendar === 'undefined') {
            console.warn('FullCalendar not loaded');
            return;
        }

        calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            locale: 'es',
            height: '100%',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth',
            },
            eventClick: (info) => {
                const sesId = info.event.extendedProps.sessionId;
                const ses = appState.sessions.find(s => s.id === sesId);
                if (!ses) return;

                const student = appState.users.find(u => u.id === ses.studentId);
                const advisor = appState.users.find(u => u.id === ses.advisorId);

                if (window.Swal) {
                    window.Swal.fire({
                        title: 'Sesión agendada',
                        html: `
                            <p><b>Fecha:</b> ${new Date(ses.datetimeISO).toLocaleString()}</p>
                            <p><b>Estudiante:</b> ${student ? escapeHtml(student.name) : '...'}</p>
                            <p><b>Asesor:</b> ${advisor ? escapeHtml(advisor.name) : '...'}</p>
                            <p><a href="${ses.teamsLink}" target="_blank">Canal de Teams</a></p>
                        `,
                        icon: 'info',
                    });
                }
            },
        });

        calendar.render();
        renderCalendarEvents();
    } catch (error) {
        console.error('Error initializing calendar:', error);
    }
}

export function renderCalendarEvents() {
    if (!calendar) return;

    const user = getCurrentUser();
    if (!user) return;

    try {
        // Primero renderizar sesiones locales
        const visibleSessions = SessionService.getVisibleSessionsForUser(user);

        calendar.removeAllEvents();

        // Renderizar sesiones locales
        visibleSessions.forEach(ses => {
            const req = appState.requests.find(r => r.id === ses.requestId);
            calendar.addEvent({
                title: escapeHtml(req ? req.subject : 'Sesión'),
                start: ses.datetimeISO,
                end: new Date(new Date(ses.datetimeISO).getTime() + 60 * 60 * 1000),
                sessionId: ses.id,
                backgroundColor: '#4CAF50',
                borderColor: '#388E3C'
            });
        });

        // Cargar eventos desde Microsoft Graph API
        loadGraphCalendarEvents();

        renderSessionList(visibleSessions);
    } catch (e) {
        console.error(e);
    }
}

// Cargar eventos desde Microsoft Graph
async function loadGraphCalendarEvents() {
    try {
        // Usar la fecha actual visible del calendario, no initialDate que puede ser null
        const startDate = calendar.view ? new Date(calendar.view.currentStart) : new Date();
        startDate.setDate(startDate.getDate() - 30); // 30 días antes
        const endDate = calendar.view ? new Date(calendar.view.currentStart) : new Date();
        endDate.setDate(endDate.getDate() + 60); // 60 días después

        const events = await RequestService.getCalendarEvents(
            startDate.toISOString(),
            endDate.toISOString()
        );

        // Renderizar eventos de Outlook
        events.forEach(event => {
            calendar.addEvent({
                title: escapeHtml(event.subject || 'Evento de Outlook'),
                start: event.start,
                end: event.end,
                backgroundColor: '#2196F3',
                borderColor: '#1976D2',
                extendedProps: {
                    isOutlookEvent: true,
                    onlineMeetingUrl: event.onlineMeetingUrl
                }
            });
        });
    } catch (error) {
        console.error('Error loading Graph calendar events:', error);
    }
}

function renderSessionList(visibleSessions) {
    const listSessionsEl = document.getElementById('list-sessions');
    if (listSessionsEl) {
        listSessionsEl.innerHTML = '';
        if (!visibleSessions.length) {
            listSessionsEl.innerHTML = '<div class="muted small">No hay sesiones agendadas.</div>';
        } else {
            visibleSessions
                .sort((a, b) => new Date(a.datetimeISO) - new Date(b.datetimeISO))
                .forEach(ses => {
                    const req = appState.requests.find(r => r.id === ses.requestId);
                    const student = appState.users.find(u => u.id === ses.studentId);
                    const advisor = appState.users.find(u => u.id === ses.advisorId);

                    const div = document.createElement('div');
                    div.className = 'list-item';
                    div.innerHTML = `
                      <div class="list-header">
                        <span><b>${req ? escapeHtml(req.subject) : 'Sesión'}</b></span>
                        <span class="badge status-${ses.status}">${ses.status}</span>
                      </div>
                      <div class="mt-8 small">${new Date(ses.datetimeISO).toLocaleString()}</div>
                      <div class="mt-8 small muted">Estudiante: ${student ? escapeHtml(student.name) : '...'}</div>
                      <div class="mt-8 small muted">Asesor: ${advisor ? escapeHtml(advisor.name) : '...'}</div>
                    `;
                    listSessionsEl.appendChild(div);
                });
        }
    }
}
