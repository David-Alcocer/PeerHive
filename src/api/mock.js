// ===============================
// Datos Mock - Información Pública de Usuarios
// ==============================================================
// NOTA: Este archivo SOLO contiene información pública de usuarios.
// Las contraseñas NUNCA deben estar en el cliente.
// La autenticación real se realiza mediante JWT con el backend.

// Usuarios de demostración (sin contraseñas - solo datos públicos)
export const DEMO_USERS_PUBLIC = [
    {
        id: "u-admin",
        name: "Admin Demo",
        email: "admin@demo.com",
        role: "admin", //La contrasela admin se ha removido para mayor seguridad
        subjects: [],
        isAdvisorApproved: true,
        createdAt: new Date().toISOString()
    },
    {
        id: "u-asesor",
        name: "Asesor Demo",
        email: "asesor@demo.com",
        role: "advisor",
        subjects: ["Algoritmia", "Programación Orientada a Objetos"],
        isAdvisorApproved: true,
        createdAt: new Date().toISOString()
    },
    {
        id: "u-estudiante",
        name: "Estudiante Demo",
        email: "estudiante@demo.com",
        role: "student",
        subjects: [],
        isAdvisorApproved: false,
        createdAt: new Date().toISOString()
    },
];

// =============================================================================
// ADVERTENCIA DE SEGURIDAD
// =============================================================================
// Las contraseñas NUNCA deben estar en el código del cliente.
// Este archivo es solo para información pública de usuarios.
// La autenticación debe realizarse mediante el endpoint /api/auth/login del backend.
