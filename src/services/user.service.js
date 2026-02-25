
import { appState } from '../store/state.js';

export const UserService = {
    updateProfile(userId, updates) {
        const user = appState.users.find(u => u.id === userId);
        if (!user) throw new Error('Usuario no encontrado');

        Object.assign(user, updates);
        appState.saveState();
        return user;
    },

    updateAdvisorSubjects(userId, subjects) {
        const user = appState.users.find(u => u.id === userId);
        if (!user || (user.role !== 'advisor' && user.role !== 'admin')) {
            throw new Error('Solo los asesores pueden configurar materias');
        }

        user.subjects = subjects;
        appState.saveState();
        return user;
    },

    approveAdvisor(userId) {
        const user = appState.users.find(u => u.id === userId);
        if (!user) throw new Error('Usuario no encontrado');

        user.isAdvisorApproved = true;
        appState.saveState();
    },

    rejectAdvisor(userId) {
        const user = appState.users.find(u => u.id === userId);
        if (!user) throw new Error('Usuario no encontrado');

        user.role = 'student';
        user.isAdvisorApproved = false;
        user.advisorSubject = null;
        user.advisorKardex = null;
        appState.saveState();
    },

    deleteUser(userId) {
        const user = appState.users.find(u => u.id === userId);
        if (!user) throw new Error('Usuario no encontrado');

        const newUsers = appState.users.filter(u => u.id !== userId);
        const newRequests = appState.requests.filter(r => r.studentId !== userId && r.advisorId !== userId);
        const newSessions = appState.sessions.filter(s => s.studentId !== userId && s.advisorId !== userId);
        const newChats = appState.chats.filter(c => c.studentId !== userId && c.advisorId !== userId);

        appState.setState({
            users: newUsers,
            requests: newRequests,
            sessions: newSessions,
            chats: newChats
        });
    },

    changeUserRole(userId, newRole) {
        const user = appState.users.find(u => u.id === userId);
        if (!user) throw new Error('Usuario no encontrado');

        user.role = newRole;

        if (newRole !== 'advisor') {
            user.isAdvisorApproved = false;
            user.advisorSubject = null;
            user.advisorKardex = null;
        } else {
            // Si es asesor asignado por admin, lo aprobamos por defecto
            user.isAdvisorApproved = true;
        }

        appState.saveState();
        return user;
    },

    getSystemStats() {
        return {
            totalUsers: appState.users.length,
            totalRequests: appState.requests.length,
            totalSessions: appState.sessions.length,
            pendingAdvisors: appState.users.filter(u => u.role === 'advisor' && !u.isAdvisorApproved).length
        };
    }
};
