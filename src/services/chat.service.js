
import { appState } from '../store/state.js';
import { uid } from '../utils/helpers.js';

export const ChatService = {
    getMyChats(user) {
        if (!user) return [];
        if (!appState.chats) appState.chats = [];

        if (user.role === 'admin') return appState.chats;

        return appState.chats.filter(
            c => c.studentId === user.id || c.advisorId === user.id
        );
    },

    async sendMessage(chatId, fromUserId, text, attachment = null) {
        const chat = appState.chats.find(c => c.id === chatId);
        if (!chat) throw new Error('Chat no encontrado');

        if (!chat.messages) chat.messages = [];

        const newMessage = {
            id: uid('msg'),
            fromUserId,
            text: text || '',
            timestampISO: new Date().toISOString(),
            attachment: attachment || null,
        };

        chat.messages.push(newMessage);
        appState.saveState();
        return newMessage;
    },

    async processAttachment(file) {
        return new Promise((resolve, reject) => {
            if (file.size > 500000) {
                resolve({
                    fileName: file.name,
                    mimeType: file.type,
                    size: file.size,
                    status: 'uploaded'
                });
            } else {
                const reader = new FileReader();
                reader.onload = () => {
                    resolve({
                        fileName: file.name,
                        mimeType: file.type,
                        dataUrl: reader.result,
                    });
                };
                reader.onerror = () => reject(new Error('No se pudo leer el archivo'));
                reader.readAsDataURL(file);
            }
        });
    }
};
