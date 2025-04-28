-- Inserindo fundos fictícios
INSERT INTO fundos (nome_fundo, cnpj_fundo, tipo_fundo) VALUES
('FIAGRO Terra Brasil', '01.234.567/0001-00', 'FIAGRO'),
('FIAGRO AgroVale', '02.345.678/0001-11', 'FIAGRO'),
('FII Urbe Real', '03.456.789/0001-22', 'FII'),
('FIAGRO Campo Forte', '04.567.890/0001-33', 'FIAGRO'),
('FIAGRO VerdeCampo', '05.678.901/0001-44', 'FIAGRO');

-- Inserindo classes de cotas para os fundos
INSERT INTO fundos_cotas (fundo_id, nome_classe, numero_cotistas, percentual_minimo_representacao, taxa_administracao, publico_alvo, data_registro) VALUES
(1, 'Classe A', 120, 3.00, 1.50, 'Investidores em geral', '2024-04-10'), -- correto: mais de 100 cotistas, 3%
(1, 'Classe B', 90, 5.00, 1.80, 'Investidores qualificados', '2024-04-10'), -- correto: até 100 cotistas, 5%
(2, 'Classe Única', 75, 4.00, 2.00, 'Investidores em geral', '2024-04-11'), -- divergente: deveria ser 5% para até 100 cotistas
(3, 'Classe Alpha', 200, 2.50, 1.30, 'Investidores em geral', '2024-04-12'), -- divergente: deveria ser 3% para >100 cotistas
(4, 'Classe Ouro', 150, 3.00, 1.60, 'Investidores em geral', '2024-04-13'), -- correto
(5, 'Classe Verde', 60, 5.00, 1.90, 'Investidores profissionais', '2024-04-14'), -- correto
(5, 'Classe Agro', 95, 6.00, 2.10, 'Investidores qualificados', '2024-04-14'); -- divergente: deveria ser 5% para <=100 cotistas
