CREATE DATABASE IF NOT EXISTS vidaplus;
USE vidaplus;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_completo VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    endereco VARCHAR(150),
    usuario_id VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    hierarquia ENUM('Administrador', 'Enfermeiro', 'Paciente') NOT NULL
);
