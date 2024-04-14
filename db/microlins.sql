CREATE DATABASE microlins;
USE microlins;

CREATE TABLE IF NOT EXISTS `cliente` (
	`id_cliente` int AUTO_INCREMENT NOT NULL UNIQUE,
	`bairro` varchar(255) NOT NULL,
	`estado_civil` varchar(255) NOT NULL,
	`genero` varchar(255) NOT NULL,
	PRIMARY KEY (`id_cliente`)
);

CREATE TABLE IF NOT EXISTS `produto` (
	`id_produto` int AUTO_INCREMENT NOT NULL UNIQUE,
	`categoria` varchar(255) NOT NULL,
	`professor` varchar(255) NOT NULL,
	`valor` int NOT NULL,
	`nome_produto` varchar(255) NOT NULL,
	PRIMARY KEY (`id_produto`)
);

CREATE TABLE IF NOT EXISTS `venda` (
	`id_venda` int AUTO_INCREMENT NOT NULL UNIQUE,
	`faturamento` float NOT NULL,
	`quantidade` int NOT NULL,
	`id_cliente` int NOT NULL,
	`id_produto` int NOT NULL,
	PRIMARY KEY (`id_venda`)
);

ALTER TABLE `venda` ADD CONSTRAINT `venda_fk3` FOREIGN KEY (`id_cliente`) REFERENCES `cliente`(`id_cliente`);

ALTER TABLE `venda` ADD CONSTRAINT `venda_fk4` FOREIGN KEY (`id_produto`) REFERENCES `produto`(`id_produto`);