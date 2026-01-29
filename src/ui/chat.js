// ===============================
// Chat (UI) - Refactored
// ===============================

import { appState, getCurrentUser, globalState, setChatId } from '../store/state.js';
import { escapeHtml, showToast, setButtonLoading } from '../utils/helpers.js';
import { ChatService } from '../services/chat.service.js';

export function renderChatList() {
    const chatListEl = document.getElementById('chat-list');
    const user = getCurrentUser();
    if (!chatListEl) return;

    try {
        chatListEl.innerHTML = '';

        if (!user) {
            chatListEl.innerHTML = '<div class="muted small">Inicia sesión para ver tus chats.</div>';
            return;
        }

        const chats = ChatService.getMyChats(user);
        if (!chats.length) {
            chatListEl.innerHTML = '<div class="muted small">Aún no tienes chats. Se crearán cuando se acepte una solicitud.</div>';
            return;
        }

        chats
            .slice()
            .reverse()
            .forEach(chat => {
                const session = appState.sessions.find(s => s.id === chat.sessionId);
                const req = session ? appState.requests.find(r => r.id === session.requestId) : null;
                const student = appState.users.find(u => u.id === chat.studentId);
                const advisor = appState.users.find(u => u.id === chat.advisorId);

                const isStudent = user.id === chat.studentId;
                const otherUser = isStudent ? advisor : student;

                const lastMsg = chat.messages?.[chat.messages.length - 1];
                const lastSnippet = lastMsg
                    ? (lastMsg.text || '[Archivo]').slice(0, 40) + ((lastMsg.text || '[Archivo]').length > 40 ? '...' : '')
                    : 'Sin mensajes aún';

                const item = document.createElement('div');
                item.className = `list-item chat-list-item ${chat.id === globalState.currentChatId ? 'active' : ''}`;
                item.innerHTML = `
                  <div class="list-header">
                    <span>${otherUser ? escapeHtml(otherUser.name) : 'Chat'}</span>
                    <span class="badge small">${req ? escapeHtml(req.subject) : 'Sesión'}</span>
                  </div>
                  <p class="small muted">${escapeHtml(lastSnippet)}</p>
                `;

                item.addEventListener('click', () => {
                    setChatId(chat.id);
                    document.querySelectorAll('.chat-list-item').forEach(el => el.classList.remove('active'));
                    item.classList.add('active');
                    renderChatMessages();
                });

                chatListEl.appendChild(item);
            });
    } catch (error) {
        console.error('Error rendering chat list:', error);
    }
}

export function renderChatMessages() {
    const chatMessagesEl = document.getElementById('chat-messages');
    const chatTitleEl = document.getElementById('chat-title');
    const chatSubtitleEl = document.getElementById('chat-subtitle');
    const user = getCurrentUser();

    if (!chatMessagesEl || !chatTitleEl || !chatSubtitleEl) return;

    try {
        if (!user) return;

        const chats = ChatService.getMyChats(user);
        if (!globalState.currentChatId && chats.length) {
            setChatId(chats[0].id);
        }

        const chat = chats.find(c => c.id === globalState.currentChatId);
        if (!chat) {
            chatTitleEl.textContent = 'Selecciona un chat';
            chatSubtitleEl.textContent = 'Cuando se acepte una solicitud se creará un chat privado.';
            chatMessagesEl.innerHTML = '';
            return;
        }

        const session = appState.sessions.find(s => s.id === chat.sessionId);
        const req = session ? appState.requests.find(r => r.id === session.requestId) : null;
        const student = appState.users.find(u => u.id === chat.studentId);
        const advisor = appState.users.find(u => u.id === chat.advisorId);
        const otherUser = (user.id === chat.studentId) ? advisor : student;

        chatTitleEl.textContent = `Chat con ${otherUser ? escapeHtml(otherUser.name) : 'usuario'}`;
        chatSubtitleEl.textContent = req ? `${escapeHtml(req.subject)} · ${escapeHtml(req.topic)}` : 'Sesión';

        chatMessagesEl.innerHTML = '';

        (chat.messages || []).forEach(m => {
            const row = document.createElement('div');
            row.className = `chat-message-row ${m.fromUserId === user.id ? 'own' : ''}`;

            const fromUser = appState.users.find(u => u.id === m.fromUserId);
            const timeLabel = m.timestampISO ? new Date(m.timestampISO).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }) : '';

            row.innerHTML = `
                <div class="chat-bubble">
                  ${m.text ? `<div>${escapeHtml(m.text)}</div>` : ''}
                  ${m.attachment ? `
                    <div class="chat-attachment">
                      <a href="${m.attachment.dataUrl || '#'}" download="${m.attachment.fileName}">
                        <i class="fa-solid fa-paperclip"></i> ${escapeHtml(m.attachment.fileName)}
                      </a>
                    </div>` : ''}
                  <div class="chat-meta">
                    ${fromUser ? escapeHtml(fromUser.name) : 'Usuario'} · ${timeLabel}
                  </div>
                </div>
            `;
            chatMessagesEl.appendChild(row);
        });

        chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
    } catch (error) {
        console.error('Error rendering messages:', error);
    }
}

export function initChat() {
    const chatForm = document.getElementById('chat-form');

    chatForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const user = getCurrentUser();
        const submitBtn = document.getElementById('chat-submit-btn');

        if (!user) return;

        try {
            const chatInput = document.getElementById('chat-input');
            const chatFileInput = document.getElementById('chat-file');
            const text = chatInput.value.trim();
            const file = chatFileInput.files[0];

            if (!text && !file) return;

            setButtonLoading(submitBtn, true);

            const chats = ChatService.getMyChats(user);
            const chat = chats.find(c => c.id === globalState.currentChatId);
            if (!chat) return;

            let attachment = null;
            if (file) {
                attachment = await ChatService.processAttachment(file);
            }

            await ChatService.sendMessage(chat.id, user.id, text, attachment);

            chatInput.value = '';
            chatFileInput.value = '';
            renderChatMessages();
            renderChatList();

        } catch (error) {
            showToast(error.message, 'error');
        } finally {
            setButtonLoading(submitBtn, false);
        }
    });
}
