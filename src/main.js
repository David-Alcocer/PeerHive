
// ===============================
// Main Entry Point
// ===============================

import { appState } from './store/state.js';
import { initTheme } from './ui/theme.js';
import { initNavigation, showMainApp } from './ui/router.js';
import { initAuthScreen } from './ui/auth.js';
import { initRequests } from './ui/requests.js';
import { initCalendar } from './ui/calendar.js';
import { initChat } from './ui/chat.js';
import { initSettings } from './ui/settings.js';
import { initContactsSearch as initAdmin } from './ui/admin.js';
import { initAdvisor } from './ui/advisor.js';

document.addEventListener('DOMContentLoaded', () => {
  console.log('PeerHive Modules Initializing...');

  // 1. Core Services & UI
  initTheme();
  initNavigation();

  // 2. Module Initializations
  initRequests();
  initCalendar();
  initChat();
  initSettings();
  initAdmin();
  initAdvisor();

  // 3. Auth State Check
  if (appState.currentUserId) {
    console.log('User logged in, showing app...');
    showMainApp();
  } else {
    console.log('No user, showing auth...');
    initAuthScreen();
  }
});