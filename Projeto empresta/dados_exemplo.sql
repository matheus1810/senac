-- EMPRESTA EQUIPAMENTOS: dados ficticios para demonstracao.
-- Importe depois do SQL do DrawSQL e do cadastro do primeiro administrador.
-- Adiciona 5 equipamentos, 2 almoxarifados e os status que ainda nao existirem.
-- Nao cria usuarios/senhas nem altera equipamentos ou usuarios existentes.
-- Pode ser executado novamente: identifica equipamentos pelo numero de serie.
-- Execute sem --force e interrompa a importacao se houver erro.

SET NAMES utf8mb4;
USE projeto_senac_empresta;
SET SESSION time_zone = '-03:00';

START TRANSACTION;

INSERT INTO status_equipamentos (status)
SELECT 'Disponível'
WHERE NOT EXISTS (SELECT 1 FROM status_equipamentos WHERE status = 'Disponível');

INSERT INTO status_equipamentos (status)
SELECT 'Emprestado'
WHERE NOT EXISTS (SELECT 1 FROM status_equipamentos WHERE status = 'Emprestado');

INSERT INTO status_equipamentos (status)
SELECT 'Manutenção'
WHERE NOT EXISTS (SELECT 1 FROM status_equipamentos WHERE status = 'Manutenção');

INSERT INTO status_equipamentos (status)
SELECT 'Indisponível'
WHERE NOT EXISTS (SELECT 1 FROM status_equipamentos WHERE status = 'Indisponível');

INSERT INTO almoxarifado (descricao)
SELECT 'Laboratório de Informática - Exemplo'
WHERE NOT EXISTS (
    SELECT 1 FROM almoxarifado WHERE descricao = 'Laboratório de Informática - Exemplo'
);

INSERT INTO almoxarifado (descricao)
SELECT 'Sala de Audiovisual - Exemplo'
WHERE NOT EXISTS (
    SELECT 1 FROM almoxarifado WHERE descricao = 'Sala de Audiovisual - Exemplo'
);

-- Resolve os IDs existentes, sem presumir que comecem em 1.
SET @disponivel = (SELECT MIN(id) FROM status_equipamentos WHERE status = 'Disponível');
SET @manutencao = (SELECT MIN(id) FROM status_equipamentos WHERE status = 'Manutenção');
SET @indisponivel = (SELECT MIN(id) FROM status_equipamentos WHERE status = 'Indisponível');
SET @informatica = (SELECT MIN(id) FROM almoxarifado WHERE descricao = 'Laboratório de Informática - Exemplo');
SET @audiovisual = (SELECT MIN(id) FROM almoxarifado WHERE descricao = 'Sala de Audiovisual - Exemplo');
SET @agora = CURRENT_TIMESTAMP;

INSERT INTO equipamentos (nome, valor, numero_serie, data_cad, status_id, id_almoxarifado)
SELECT 'Notebook Dell Inspiron', 4200.00, 'EX-NOTE-001', @agora, @disponivel, @informatica
WHERE NOT EXISTS (SELECT 1 FROM equipamentos WHERE numero_serie = 'EX-NOTE-001');

INSERT INTO equipamentos (nome, valor, numero_serie, data_cad, status_id, id_almoxarifado)
SELECT 'Projetor Epson PowerLite', 3500.00, 'EX-PROJ-001', @agora, @disponivel, @audiovisual
WHERE NOT EXISTS (SELECT 1 FROM equipamentos WHERE numero_serie = 'EX-PROJ-001');

INSERT INTO equipamentos (nome, valor, numero_serie, data_cad, status_id, id_almoxarifado)
SELECT 'Câmera Canon EOS', 2800.00, 'EX-CAM-001', @agora, @disponivel, @audiovisual
WHERE NOT EXISTS (SELECT 1 FROM equipamentos WHERE numero_serie = 'EX-CAM-001');

INSERT INTO equipamentos (nome, valor, numero_serie, data_cad, status_id, id_almoxarifado)
SELECT 'Microfone Shure', 650.00, 'EX-MIC-001', @agora, @manutencao, @audiovisual
WHERE NOT EXISTS (SELECT 1 FROM equipamentos WHERE numero_serie = 'EX-MIC-001');

INSERT INTO equipamentos (nome, valor, numero_serie, data_cad, status_id, id_almoxarifado)
SELECT 'Tablet Samsung Galaxy Tab', 1800.00, 'EX-TAB-001', @agora, @indisponivel, @informatica
WHERE NOT EXISTS (SELECT 1 FROM equipamentos WHERE numero_serie = 'EX-TAB-001');

COMMIT;

-- Confira os exemplos: 3 disponiveis, 1 em manutencao e 1 indisponivel.
-- Nenhum emprestimo e criado artificialmente; os disponiveis podem ser
-- solicitados pelo Aluno e aprovados pelo Gestor no fluxo normal do sistema.
SELECT e.nome, e.numero_serie, e.valor, s.status, a.descricao AS almoxarifado
FROM equipamentos AS e
JOIN status_equipamentos AS s ON s.id = e.status_id
JOIN almoxarifado AS a ON a.id = e.id_almoxarifado
WHERE e.numero_serie IN ('EX-NOTE-001', 'EX-PROJ-001', 'EX-CAM-001', 'EX-MIC-001', 'EX-TAB-001')
ORDER BY e.numero_serie;
