-- Cria o banco de dados se necessário (opcional, depende da configuração)
-- CREATE DATABASE cvm_assistente;

-- 1. Tabela de Fundos 
-- Guarda o cadastro básico dos fundos.
CREATE TABLE fundos (
    id SERIAL PRIMARY KEY,
    nome_fundo TEXT NOT NULL,
    cnpj_fundo VARCHAR(20) UNIQUE,
    tipo_fundo TEXT -- ex.: FIAGRO, FII, etc
);

-- 2. Tabela de Classes de Cotas: 
-- Guarda os dados de cada classe de cotas (incluindo número de cotistas e taxas).
CREATE TABLE fundos_cotas (
    id SERIAL PRIMARY KEY,
    fundo_id INTEGER REFERENCES fundos(id) ON DELETE CASCADE,
    nome_classe TEXT NOT NULL,
    numero_cotistas INTEGER,
    percentual_minimo_representacao DECIMAL(5,2), -- exemplo: 3.00 (%)
    taxa_administracao DECIMAL(5,2), -- em % ao ano
    taxa_gestao DECIMAL(5,2),        -- em % ao ano
    taxa_custodia DECIMAL(5,2),      -- em % ao ano
    publico_alvo TEXT, -- 'Investidores em geral', 'Qualificado', etc
    data_registro DATE
);

-- 3. Tabela de Validações Realizadas (logs)
-- Guarda o log das comparações feitas pelo agente (resultado de validações).
CREATE TABLE validacoes (
    id SERIAL PRIMARY KEY,
    fundo_cota_id INTEGER REFERENCES fundos_cotas(id) ON DELETE CASCADE,
    tipo_validacao TEXT NOT NULL, -- ex.: 'percentual_representacao', 'taxa_administracao'
    valor_esperado DECIMAL(10,4),
    valor_encontrado DECIMAL(10,4),
    status_validacao TEXT, -- 'Conforme', 'Divergente', 'Não encontrado'
    detalhe_validacao TEXT,
    data_validacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
