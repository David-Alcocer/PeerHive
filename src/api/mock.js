// ===============================
// Datos Mock (Simulación Backend)
// ===============================

// Función de hash básica para seguridad en demo (Requerida aquí o en helpers, 
// pero como se usa para definir los usuarios, la importaremos de helpers si es posible,
// o la duplicamos para evitar ciclos si helpers depende de esto.
// Mejor opción: Mover hashPassword a helpers y usarla aquí.

import { hashPassword } from '../utils/helpers.js';

export const DEMO_USERS = [
    {
        id: "u-admin",
        name: "Admin Demo",
        email: "admin@demo.com",
        password: hashPassword("admin"),
        role: "admin",
        subjects: [],
        isAdvisorApproved: true,
        createdAt: new Date().toISOString()
    },
    {
        id: "u-asesor",
        name: "Asesor Demo",
        email: "asesor@demo.com",
        password: hashPassword("asesor"),
        role: "advisor",
        subjects: ["Algoritmia", "Programación Orientada a Objetos"],
        isAdvisorApproved: true,
        createdAt: new Date().toISOString()
    },
    {
        id: "u-estudiante",
        name: "Estudiante Demo",
        email: "estudiante@demo.com",
        password: hashPassword("estudiante"),
        role: "student",
        subjects: [],
        isAdvisorApproved: false,
        createdAt: new Date().toISOString()
    },
];
