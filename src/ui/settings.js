// ===============================
// Ajustes (UI) - Refactored
// ===============================

import { getCurrentUser } from '../store/state.js';
import { showToast, setButtonLoading, hashPassword } from '../utils/helpers.js';
import { UserService } from '../services/user.service.js';
import { updateTopbarUser } from './router.js';

export function hydrateSettings() {
    const user = getCurrentUser();
    if (!user) return;

    const nameInput = document.getElementById('settings-name');
    const emailInput = document.getElementById('settings-email');
    const avatar = document.getElementById('settings-avatar');
    const roleLabel = document.getElementById('settings-role-label');

    if (nameInput) nameInput.value = user.name || '';
    if (emailInput) emailInput.value = user.email || '';
    if (roleLabel) roleLabel.textContent = user.role.charAt(0).toUpperCase() + user.role.slice(1);

    if (avatar) {
        avatar.textContent = (user.name || user.email || 'PH')
            .split(' ')
            .map(p => p[0])
            .join('')
            .slice(0, 2)
            .toUpperCase();
    }
}

export function initSettings() {
    const formSettings = document.getElementById('form-settings');
    const settingsSubmitBtn = document.getElementById('settings-submit-btn');

    formSettings?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const user = getCurrentUser();
        if (!user) return;

        setButtonLoading(settingsSubmitBtn, true);

        try {
            const name = document.getElementById('settings-name').value.trim();
            const email = document.getElementById('settings-email').value.trim();
            const password = document.getElementById('settings-password').value.trim();

            const updates = { name, email };
            if (password) {
                updates.password = hashPassword(password);
            }

            await UserService.updateProfile(user.id, updates);

            showToast('Perfil actualizado exitosamente', 'success');
            updateTopbarUser();
            hydrateSettings();

            if (password) document.getElementById('settings-password').value = '';

        } catch (error) {
            showToast(error.message, 'error');
        } finally {
            setButtonLoading(settingsSubmitBtn, false);
        }
    });
}
