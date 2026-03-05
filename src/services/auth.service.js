
import { appState, findUserByEmail, getCurrentUser } from '../store/state.js';
import { API_URL } from '../api/config.js';

export const AuthService = {
    /**
     * Autentica al usuario usando el backend JWT real.
     */
    async login(email, password) {
        try {
            const response = await fetch(`${API_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
                credentials: 'include'
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Credenciales inválidas');
            }

            const data = await response.json();

            // Guardar el token JWT
            localStorage.setItem('jwt_token', data.access_token);

            // Obtener información del usuario
            const userResponse = await fetch(`${API_URL}/api/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${data.access_token}`
                },
                credentials: 'include'
            });

            if (!userResponse.ok) {
                throw new Error('Error al obtener información del usuario');
            }

            const userData = await userResponse.json();

            // Guardar en el estado local
            appState.currentUserId = userData.id;

            // Actualizar el usuario en el estado local si existe
            const existingUser = appState.users.find(u => u.email === email);
            if (existingUser) {
                existingUser.id = userData.id;
            } else {
                appState.users.push(userData);
            }
            appState.saveState();

            return userData;
        } catch (error) {
            console.error('Error en login:', error);
            throw error;
        }
    },

    /**
     * Registra un nuevo usuario en el sistema.
     */
    async signup(userData) {
        try {
            const response = await fetch(`${API_URL}/api/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
                credentials: 'include'
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al registrar usuario');
            }

            const data = await response.json();

            // Guardar el token JWT
            localStorage.setItem('jwt_token', data.access_token);

            // Obtener información del usuario
            const userResponse = await fetch(`${API_URL}/api/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${data.access_token}`
                },
                credentials: 'include'
            });

            const newUserData = await userResponse.json();

            // Agregar al estado local
            appState.users.push(newUserData);
            appState.currentUserId = newUserData.id;
            appState.saveState();

            return newUserData;
        } catch (error) {
            console.error('Error en signup:', error);
            throw error;
        }
    },

    /**
     * Cierra la sesión del usuario.
     */
    logout() {
        appState.currentUserId = null;
        localStorage.removeItem('jwt_token');
    },

    /**
     * Obtiene el token JWT actual.
     */
    getToken() {
        return localStorage.getItem('jwt_token');
    },

    /**
     * Verifica si el usuario está autenticado.
     */
    async isAuthenticated() {
        const token = this.getToken();
        if (!token) return false;

        try {
            const response = await fetch(`${API_URL}/api/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                credentials: 'include'
            });
            return response.ok;
        } catch {
            return false;
        }
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
