// ===============================
// Gestión del Estado (Store)
// ===============================

import { STORAGE_KEY } from '../api/config.js';
import { DEMO_USERS } from '../api/mock.js';
import { showToast } from '../utils/helpers.js';

class AppState {
    constructor() {
        this._state = this.loadState();
    }

    loadState() {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) {
            return {
                users: [...DEMO_USERS], // Clone to avoid mutation of constant
                currentUserId: null,
                requests: [],
                sessions: [],
                reports: [],
                chats: [],
                lastUpdate: new Date().toISOString()
            };
        }

        try {
            const parsed = JSON.parse(raw);

            // Validar y normalizar estructura
            if (!parsed.users || !Array.isArray(parsed.users)) {
                parsed.users = [...DEMO_USERS];
            }

            if (!parsed.requests || !Array.isArray(parsed.requests)) {
                parsed.requests = [];
            }

            if (!parsed.sessions || !Array.isArray(parsed.sessions)) {
                parsed.sessions = [];
            }

            if (!parsed.chats || !Array.isArray(parsed.chats)) {
                parsed.chats = [];
            }

            // Normalizar campos nuevos en usuarios existentes
            parsed.users.forEach(u => {
                if (u.role === 'advisor' && typeof u.isAdvisorApproved !== 'boolean') {
                    u.isAdvisorApproved = true;
                }
                // Asegurar que todos los usuarios tengan array de subjects
                if (!u.subjects) u.subjects = [];
                // Asegurar fecha de creación
                if (!u.createdAt) u.createdAt = new Date().toISOString();
            });

            parsed.lastUpdate = parsed.lastUpdate || new Date().toISOString();

            return parsed;
        } catch (error) {
            console.error('Error loading state:', error);
            return {
                users: [...DEMO_USERS],
                currentUserId: null,
                requests: [],
                sessions: [],
                reports: [],
                chats: [],
                lastUpdate: new Date().toISOString()
            };
        }
    }

    saveState() {
        try {
            this._state.lastUpdate = new Date().toISOString();
            localStorage.setItem(STORAGE_KEY, JSON.stringify(this._state));
        } catch (error) {
            console.error('Error saving state:', error);
            showToast('Error al guardar los datos', 'error');
        }
    }

    get state() {
        return this._state;
    }

    setState(updates) {
        this._state = { ...this._state, ...updates };
        this.saveState();
    }

    // Getters específicos
    get users() { return this._state.users; }
    get currentUserId() { return this._state.currentUserId; }
    get requests() { return this._state.requests; }
    get sessions() { return this._state.sessions; }
    get chats() { return this._state.chats; }

    set currentUserId(id) {
        this._state.currentUserId = id;
        this.saveState();
    }
}

// Instancia global del estado
export const appState = new AppState();

// Variables globales adicionales (que antes estaban en script.js)
// currentChatId lo moveremos a un modulo de UI o al state si es compartido.
// Para simplificar, lo añadimos al AppState o lo exportamos como variable reactiva (mutable export).
// Usaremos una variable mutable exportada aquí para simplificar.

export let globalState = {
    currentChatId: null
};

export function setChatId(id) {
    globalState.currentChatId = id;
}

export function getCurrentUser() {
    return appState.users.find(u => u.id === appState.currentUserId) || null;
}

export function findUserByEmail(email) {
    return appState.users.find(u => u.email.toLowerCase() === email.toLowerCase());
}
