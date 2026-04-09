-- Script SQL para criar o banco de dados do Sistema de Gestão de Riscos em Projetos de TI

CREATE DATABASE IF NOT EXISTS risk_management_db;
USE risk_management_db;

-- Tabela PROJETOS
CREATE TABLE IF NOT EXISTS projetos (
    id_projeto INT AUTO_INCREMENT PRIMARY KEY,
    nome_projeto VARCHAR(255) NOT NULL,
    responsavel VARCHAR(255) NOT NULL,
    prazo_final DATE NOT NULL,
    orcamento DECIMAL(10, 2) NOT NULL,
    status ENUM('Ativo', 'Concluído', 'Cancelado') NOT NULL DEFAULT 'Ativo'
);

-- Tabela RISCOS
CREATE TABLE IF NOT EXISTS riscos (
    id_risco INT AUTO_INCREMENT PRIMARY KEY,
    id_projeto INT NOT NULL,
    descricao TEXT NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    probabilidade ENUM('Baixa', 'Média', 'Alta') NOT NULL,
    impacto ENUM('Baixo', 'Médio', 'Alto') NOT NULL,
    nivel_criticidade ENUM('Baixo', 'Médio', 'Alto') NOT NULL,
    status_risco ENUM('Ativo', 'Mitigado', 'Resolvido') NOT NULL DEFAULT 'Ativo',
    FOREIGN KEY (id_projeto) REFERENCES projetos(id_projeto) ON DELETE CASCADE
);

-- Tabela MITIGACAO
CREATE TABLE IF NOT EXISTS mitigacao (
    id_acao INT AUTO_INCREMENT PRIMARY KEY,
    id_risco INT NOT NULL,
    descricao_acao TEXT NOT NULL,
    responsavel VARCHAR(255) NOT NULL,
    prazo DATE NOT NULL,
    status_acao ENUM('Pendente', 'Em Andamento', 'Concluída') NOT NULL DEFAULT 'Pendente',
    FOREIGN KEY (id_risco) REFERENCES riscos(id_risco) ON DELETE CASCADE
);