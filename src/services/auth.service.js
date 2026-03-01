
import { appState, findUserByEmail, getCurrentUser } from '../store/state.js';
import { hashPassword, verifyPassword, uid } from '../utils/helpers.js';
import { API_URL } from '../api/config.js';

export const AuthService = {
    async login(email, password) {
        // Simular latencia de red
        await new Promise(resolve => setTimeout(resolve, 800));

        const user = findUserByEmail(email);
        if (!user || !verifyPassword(password, user.password)) {
            throw new Error('Credenciales inválidas');
        }

        if (user.role === 'advisor' && user.isAdvisorApproved === false) {
            throw new Error('Tu cuenta de asesor está en revisión. Te notificaremos cuando sea aprobada.');
        }

        appState.currentUserId = user.id;
        return user;
    },

    async signup(userData) {
        // Simular latencia
        await new Promise(resolve => setTimeout(resolve, 1000));

        if (findUserByEmail(userData.email)) {
            throw new Error('Ya existe un usuario con ese correo');
        }

        const newUser = {
            id: uid('u'),
            name: userData.name,
            email: userData.email,
            password: hashPassword(userData.password),
            role: userData.role,
            subjects: [],
            advisorSubject: userData.advisorSubject || null,
            advisorKardex: userData.advisorKardex || null,
            isAdvisorApproved: userData.role === 'advisor' ? userData.isAdvisorApproved : false,
            createdAt: new Date().toISOString()
        };

        appState.users.push(newUser);
        appState.saveState();

        return newUser;
    },

    logout() {
        appState.currentUserId = null;
    },

    async processKardexFile(file) {
        return new Promise((resolve, reject) => {
            if (file.size > 500000) {
                resolve({
                    fileName: file.name,
                    uploadedAt: new Date().toISOString(),
                    size: file.size,
                    status: 'uploaded'
                });
            } else {
                const reader = new FileReader();
                reader.onload = () => {
                    resolve({
                        fileName: file.name,
                        uploadedAt: new Date().toISOString(),
                        dataUrl: reader.result,
                        size: file.size,
                        status: 'processed'
                    });
                };
                reader.onerror = () => reject(new Error('No se pudo leer el archivo'));
                reader.readAsDataURL(file);
            }
        });
    }
};

// ===============================
// Funciones auxiliares para Microsoft Graph
// ===============================

/**
 * Verifica si el usuario tiene una sesión activa con Microsoft Graph en el backend.
 * El token NUNCA sale del backend — el frontend solo verifica el estado de autenticación.
 */
export async function checkGraphAuthStatus() {
    try {
        const response = await fetch(`${API_URL}/auth/me`, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) return false;
        const data = await response.json();
        return data.has_graph_token === true;
    } catch (error) {
        console.warn('Error verificando estado de autenticación Graph:', error.message);
        return false;
    }
}
