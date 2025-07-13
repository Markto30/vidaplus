-- Criar o banco de dados
USE vidaplus;

-- Criar a tabela 'usuarios' com a hierarquia atualizada
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_completo VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    endereco VARCHAR(150),
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    hierarquia ENUM('Administrador', 'Medico', 'Paciente') NOT NULL
);

SELECT * FROM usuarios;

CREATE TABLE agendamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_usuario VARCHAR(50),
    medico_usuario VARCHAR(50),
    data_consulta DATE,
    hora_consulta TIME,
    observacoes TEXT,
    FOREIGN KEY (paciente_usuario) REFERENCES usuarios(usuario),
    FOREIGN KEY (medico_usuario) REFERENCES usuarios(usuario)
);

SELECT * FROM agendamentos



