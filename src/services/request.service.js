
import { appState, setChatId } from '../store/state.js';
import { uid, generateTeamsChannelLink } from '../utils/helpers.js';
import { API_BASE_URL } from '../api/config.js';

export const RequestService = {
    async create(requestData) {
        // Simular latencia
        await new Promise(resolve => setTimeout(resolve, 800));

        const request = {
            id: uid('req'),
            studentId: requestData.studentId,
            subject: requestData.subject,
            topic: requestData.topic,
            datetimeISO: requestData.datetimeISO,
            notes: requestData.notes,
            status: 'pendiente',
            advisorId: null, // Always null initially
            createdAt: new Date().toISOString()
        };

        appState.requests.push(request);
        appState.saveState();
        return request;
    },

    async assignAdvisor(requestId, advisorId) {
        const req = appState.requests.find(r => r.id === requestId);
        if (!req) {
            throw new Error('Solicitud no encontrada');
        }

        if (req.status !== 'pendiente') {
            throw new Error('Esta solicitud ya fue procesada');
        }

        // Simular latencia
        await new Promise(resolve => setTimeout(resolve, 1000));

        const session = {
            id: uid('ses'),
            requestId: req.id,
            studentId: req.studentId,
            advisorId,
            datetimeISO: req.datetimeISO,
            status: 'agendada',
            teamsLink: generateTeamsChannelLink(),
            createdAt: new Date().toISOString()
        };

        appState.sessions.push(session);

        // Actualizar solicitud
        req.status = 'agendada';
        req.advisorId = advisorId;

        // Crear chat asociado
        if (!appState.chats) appState.chats = [];

        const chat = {
            id: uid('chat'),
            sessionId: session.id,
            studentId: req.studentId,
            advisorId: advisorId,
            messages: [],
            createdAt: new Date().toISOString()
        };

        appState.chats.push(chat);
        setChatId(chat.id);

        appState.saveState();

        return { session, chat };
    },

    getAllForUser(user) {
        if (!user) return [];
        if (user.role === 'student') {
            return appState.requests.filter(r => r.studentId === user.id);
        }
        if (user.role === 'advisor') {
            // Advisors see requests assigned to them OR unassigned (pending) if they want to pick them
            // The original logic was: advisorId === user.id || !r.advisorId
            return appState.requests.filter(r => r.advisorId === user.id || !r.advisorId);
        }
        return appState.requests; // Admin sees all
    },

    // ==============================
    // Métodos de API - Calendario
    // ==============================

    async getCalendarEvents(startDate, endDate) {
        try {
            const response = await fetch(
                `${API_BASE_URL}/calendar/events?start_date=${startDate}&end_date=${endDate}`,
                {
                    credentials: 'include',
                    headers: { 'Content-Type': 'application/json' }
                }
            );

            if (!response.ok) {
                if (response.status === 401) {
                    console.log('No autenticado con Microsoft Graph - mostrando solo sesiones locales');
                    return [];
                }
                throw new Error(`Error fetching calendar events: ${response.status}`);
            }

            const data = await response.json();
            return data.events || [];
        } catch (error) {
            console.error('Error getting calendar events:', error);
            return [];
        }
    },

    async createCalendarEvent(eventData) {
        try {
            const response = await fetch(`${API_BASE_URL}/calendar/events`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(eventData)
            });

            if (!response.ok) {
                throw new Error(`Error creating calendar event: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error creating calendar event:', error);
            throw error;
        }
    },

    // ==============================
    // Métodos de API - Teams
    // ==============================

    async createTeamsMeeting(subject, startTime, endTime) {
        try {
            const response = await fetch(`${API_BASE_URL}/teams/meetings`, {
                method: 'POST',
                credentials: 'include', // Usar sesión del backend para autenticación
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    subject,
                    start_time: startTime,
                    end_time: endTime
                })
            });

            if (!response.ok) {
                if (response.status === 401) {
                    console.warn('No autenticado con Microsoft Graph para crear reunión de Teams');
                    return { joinUrl: generateTeamsChannelLink(), error: 'No autenticado' };
                }
                throw new Error(`Error creating Teams meeting: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error creating Teams meeting:', error);
            return {
                joinUrl: generateTeamsChannelLink(),
                error: error.message
            };
        }
    },

    async getMeetingAttendance(meetingId) {
        try {
            const response = await fetch(`${API_BASE_URL}/teams/meetings/${meetingId}/attendance`, {
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error(`Error getting meeting attendance: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting meeting attendance:', error);
            return { attendees: [], error: error.message };
        }
    }
};
