
import { appState } from '../store/state.js';

export const SessionService = {
    getVisibleSessionsForUser(user) {
        if (!user) return [];
        if (user.role === 'admin') return appState.sessions;

        return appState.sessions.filter(
            s => s.studentId === user.id || s.advisorId === user.id
        );
    },

    getUpcomingSessions(user, limit = 5) {
        const sessions = this.getVisibleSessionsForUser(user);
        const now = new Date();

        return sessions
            .filter(s => new Date(s.datetimeISO) >= now)
            .sort((a, b) => new Date(a.datetimeISO) - new Date(b.datetimeISO))
            .slice(0, limit);
    }
};
