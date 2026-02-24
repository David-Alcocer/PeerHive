
import { appState, setChatId } from '../store/state.js';
import { uid, generateTeamsChannelLink } from '../utils/helpers.js';

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
    }
};
