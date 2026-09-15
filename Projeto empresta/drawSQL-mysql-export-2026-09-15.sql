CREATE TABLE `usuario`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `role_id` INT UNSIGNED NOT NULL,
    `nome` VARCHAR(255) NOT NULL,
    `data_nascimento` DATE NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `senha` VARCHAR(255) NOT NULL,
    `cpf` VARCHAR(255) NOT NULL,
    `data_cad` DATETIME NOT NULL
);
ALTER TABLE
    `usuario` ADD INDEX `usuario_role_id_index`(`role_id`);
ALTER TABLE
    `usuario` ADD UNIQUE `usuario_email_unique`(`email`);
ALTER TABLE
    `usuario` ADD UNIQUE `usuario_cpf_unique`(`cpf`);
CREATE TABLE `emprestimos`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `item_solicitacao_id` INT UNSIGNED NOT NULL UNIQUE,
    `data_emprestimo` DATETIME NOT NULL,
    `data_devolucao` DATETIME NULL,
    `observacoes` VARCHAR(255) NOT NULL,
    `estado_na_devolucao` VARCHAR(255) NULL
);
CREATE TABLE `solicitacao`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_aluno` INT NOT NULL,
    `data_solicitacao` DATETIME NOT NULL
);
CREATE TABLE `papeis`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `responsabilidade` VARCHAR(255) NOT NULL
);
CREATE TABLE `almoxarifado`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `descricao` VARCHAR(255) NOT NULL
);
CREATE TABLE `equipamentos`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `nome` VARCHAR(255) NOT NULL,
    `valor` DECIMAL(8, 2) NOT NULL,
    `numero_serie` VARCHAR(255) NOT NULL,
    `data_cad` DATETIME NOT NULL,
    `status_id` INT NOT NULL,
    `id_almoxarifado` INT NOT NULL
);
CREATE TABLE `status_equipamentos`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `status` VARCHAR(255) NOT NULL
) COMMENT 'Disponível, emprestado, manutanção, indisponível';
CREATE TABLE `item_solicitacao`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_solicitacao` INT NOT NULL,
    `id_equipamento` INT NOT NULL,
    `status` ENUM('aprovado', 'negado', 'analise') NOT NULL DEFAULT 'analise'
);
ALTER TABLE
    `emprestimos` ADD CONSTRAINT `emprestimos_item_solicitacao_id_foreign` FOREIGN KEY(`item_solicitacao_id`) REFERENCES `item_solicitacao`(`id`);
ALTER TABLE
    `usuario` ADD CONSTRAINT `usuario_role_id_foreign` FOREIGN KEY(`role_id`) REFERENCES `papeis`(`id`);
ALTER TABLE
    `item_solicitacao` ADD CONSTRAINT `item_solicitacao_id_solicitacao_foreign` FOREIGN KEY(`id_solicitacao`) REFERENCES `solicitacao`(`id`);
ALTER TABLE
    `equipamentos` ADD CONSTRAINT `equipamentos_id_almoxarifado_foreign` FOREIGN KEY(`id_almoxarifado`) REFERENCES `almoxarifado`(`id`);
ALTER TABLE
    `item_solicitacao` ADD CONSTRAINT `item_solicitacao_id_equipamento_foreign` FOREIGN KEY(`id_equipamento`) REFERENCES `equipamentos`(`id`);
ALTER TABLE
    `equipamentos` ADD CONSTRAINT `equipamentos_status_id_foreign` FOREIGN KEY(`status_id`) REFERENCES `status_equipamentos`(`id`);
ALTER TABLE
    `solicitacao` ADD CONSTRAINT `solicitacao_id_aluno_foreign` FOREIGN KEY(`id_aluno`) REFERENCES `usuario`(`id`);