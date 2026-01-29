// ===============================
// Autenticación (UI) - Refactored
// ===============================

import { getCurrentUser, findUserByEmail } from '../store/state.js';
import {
    showToast,
    setButtonLoading,
    escapeHtml
} from '../utils/helpers.js';
import { AuthService } from '../services/auth.service.js';

import { showMainApp } from './router.js';
import { updateSystemStats } from './dashboard.js';
import { renderContacts } from './admin.js';

let currentAuthTab = 'login';

export function initAuthScreen() {
    const authScreen = document.getElementById('auth-screen');
    const app = document.querySelector('.app');

    if (authScreen) authScreen.style.display = 'flex';
    if (app) app.style.display = 'none';

    setupAuthTabs();
    setupDemoAccounts();
    setupRoleSelection();
    setupFileUpload();
    setupPasswordStrength();
    setupForms();
}

function setupAuthTabs() {
    document.querySelectorAll('.auth-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');
            switchAuthTab(targetTab);
        });
    });
}

function switchAuthTab(tabName) {
    document.querySelectorAll('.auth-tab').forEach(tab => {
        tab.classList.toggle('active', tab.getAttribute('data-tab') === tabName);
    });

    document.querySelectorAll('.auth-content').forEach(content => {
        content.classList.toggle('active', content.id === `${tabName}-tab`);
    });

    currentAuthTab = tabName;
}

function setupDemoAccounts() {
    document.querySelectorAll('.demo-account-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const email = btn.getAttribute('data-email');
            const password = btn.getAttribute('data-password');

            const emailInput = document.getElementById('login-email');
            const passInput = document.getElementById('login-password');

            if (emailInput && passInput) {
                emailInput.value = email;
                passInput.value = password;
            }

            switchAuthTab('login');
            showToast(`Cuenta demo cargada: ${email.split('@')[0]}`, 'info');
        });
    });
}

function setupRoleSelection() {
    document.querySelectorAll('input[name="signup-type"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            const isAdvisor = e.target.value === 'advisor';
            const extra = document.getElementById('signup-advisor-extra');
            if (extra) extra.style.display = isAdvisor ? 'block' : 'none';
        });
    });
}

function setupFileUpload() {
    const uploadArea = document.getElementById('kardex-upload-area');
    const fileInput = document.getElementById('signup-kardex');

    if (!uploadArea || !fileInput) return;

    uploadArea.addEventListener('click', () => fileInput.click());

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');

        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileSelection(e.target.files[0]);
        }
    });
}

function handleFileSelection(file) {
    if (file.type !== 'application/pdf') {
        showToast('Solo se permiten archivos PDF', 'error');
        return;
    }

    if (file.size > 2 * 1024 * 1024) {
        showToast('El archivo debe ser menor a 2MB', 'error');
        return;
    }

    const preview = document.getElementById('kardex-preview');
    if (preview) {
        preview.innerHTML = `
        <i class="fa-solid fa-file-pdf"></i>
        <div>
        <strong>${escapeHtml(file.name)}</strong>
        <div>${(file.size / 1024 / 1024).toFixed(2)} MB</div>
        </div>
        <button type="button" class="remove-file" id="btn-remove-kardex">
        <i class="fa-solid fa-times"></i>
        </button>
    `;
        preview.style.display = 'flex';
        document.getElementById('btn-remove-kardex').addEventListener('click', removeKardexFile);
    }
}

export function removeKardexFile() {
    const fileInput = document.getElementById('signup-kardex');
    const preview = document.getElementById('kardex-preview');

    if (fileInput) fileInput.value = '';
    if (preview) preview.style.display = 'none';
}

function setupPasswordStrength() {
    const passwordInput = document.getElementById('signup-password');
    const strengthBar = document.querySelector('.strength-bar');
    const strengthText = document.querySelector('.strength-text');

    if (!passwordInput || !strengthBar) return;

    passwordInput.addEventListener('input', (e) => {
        const password = e.target.value;
        const strength = calculatePasswordStrength(password);

        strengthBar.style.setProperty('--strength-width', `${strength.score * 25}%`);
        strengthBar.style.setProperty('--strength-color', strength.color);
        if (strengthText) {
            strengthText.textContent = strength.text;
            strengthText.style.color = strength.color;
        }
    });
}

function calculatePasswordStrength(password) {
    let score = 0;
    if (password.length >= 8) score++;
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) score++;
    if (password.match(/\d/)) score++;
    if (password.match(/[^a-zA-Z\d]/)) score++;

    const strengths = [
        { score: 0, color: '#ef4444', text: 'Muy débil' },
        { score: 1, color: '#f59e0b', text: 'Débil' },
        { score: 2, color: '#eab308', text: 'Regular' },
        { score: 3, color: '#84cc16', text: 'Fuerte' },
        { score: 4, color: '#22c55e', text: 'Muy fuerte' }
    ];

    return strengths[Math.min(score, 4)];
}

function setupForms() {
    const formLogin = document.getElementById('form-login');
    const loginSubmitBtn = document.getElementById('login-submit-btn');

    formLogin?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = loginSubmitBtn;
        setButtonLoading(submitBtn, true);

        try {
            const email = document.getElementById('login-email').value.trim();
            const password = document.getElementById('login-password').value.trim();

            if (!email || !password) {
                showToast('Completa todos los campos', 'warning');
                return;
            }

            // Delegar lógica a AuthService
            const user = await AuthService.login(email, password);

            showMainApp();
            showToast(`¡Bienvenido de vuelta, ${user.name}!`, 'success');

        } catch (error) {
            console.error('Login error:', error);
            showToast(error.message || 'Error al iniciar sesión', 'error');
        } finally {
            setButtonLoading(submitBtn, false);
        }
    });

    const formSignup = document.getElementById('form-signup');
    const signupSubmitBtn = document.getElementById('signup-submit-btn');

    formSignup?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = signupSubmitBtn;
        setButtonLoading(submitBtn, true);

        try {
            const name = document.getElementById('signup-name').value.trim();
            const email = document.getElementById('signup-email').value.trim();
            const password = document.getElementById('signup-password').value.trim();
            const typeRadio = document.querySelector('input[name="signup-type"]:checked');
            const type = typeRadio ? typeRadio.value : 'student';

            if (!name || !email || !password) {
                showToast('Completa todos los campos de registro', 'warning');
                return;
            }

            const uadyPattern = /^a\d{8}@alumnos\.uady\.mx$/i;
            if (!uadyPattern.test(email)) {
                showToast('El correo debe ser institucional UADY (a########@alumnos.uady.mx)', 'error');
                return;
            }

            let advisorSubject = null;
            let advisorKardex = null;
            let role = 'student';
            let isAdvisorApproved = false;

            if (type === 'advisor') {
                advisorSubject = document.getElementById('signup-subject').value.trim();
                const kardexFile = document.getElementById('signup-kardex').files[0];

                if (!advisorSubject) {
                    showToast('Indica la materia que deseas asesorar', 'warning');
                    return;
                }

                if (!kardexFile) {
                    showToast('Debes adjuntar tu kardex en PDF para registrarte como asesor', 'warning');
                    return;
                }

                if (kardexFile.type !== 'application/pdf') {
                    showToast('El kardex debe ser un archivo PDF', 'error');
                    return;
                }

                if (kardexFile.size > 2 * 1024 * 1024) {
                    showToast('El kardex debe pesar máximo 2 MB', 'error');
                    return;
                }

                role = 'advisor';
                isAdvisorApproved = false;

                // Usar servicio para procesar archivo
                advisorKardex = await AuthService.processKardexFile(kardexFile);
            }

            // Delegar creación a AuthService
            await AuthService.signup({
                name, email, password, role, advisorSubject, advisorKardex, isAdvisorApproved
            });

            const formSignup = document.getElementById('form-signup');
            if (formSignup) formSignup.reset();

            const extra = document.getElementById('signup-advisor-extra');
            if (extra) extra.style.display = 'none';

            removeKardexFile();

            try {
                updateSystemStats();
                renderContacts();
            } catch (e) { console.error(e); }

            if (role === 'advisor') {
                showToast('Registro enviado. Tu solicitud para ser asesor está en revisión.', 'success');
                switchAuthTab('login');
            } else {
                showToast('Estudiante registrado exitosamente. Ahora puedes iniciar sesión.', 'success');
                switchAuthTab('login');
            }

        } catch (error) {
            console.error('Signup error:', error);
            showToast(error.message || 'Error en el registro', 'error');
        } finally {
            setButtonLoading(submitBtn, false);
        }
    });
}
