-- Criando as tabelas
CREATE TABLE clientes (
id_cliente SERIAL PRIMARY KEY,
nome VARCHAR(100),
data_cadastro DATE
);
CREATE TABLE produtos (
id_produto SERIAL PRIMARY KEY,
nome VARCHAR(100),
categoria VARCHAR(50),
preco NUMERIC
);
CREATE TABLE pedidos (
id_pedido SERIAL PRIMARY KEY,
data_pedido DATE,
valor_total NUMERIC,
id_cliente INT REFERENCES clientes(id_cliente)
);
CREATE TABLE itens_pedido (
id_item SERIAL PRIMARY KEY,
id_pedido INT REFERENCES pedidos(id_pedido),
id_produto INT REFERENCES produtos(id_produto),
quantidade INT,
preco_unitario NUMERIC
);

SELECT * FROM clientes;

INSERT INTO clientes (nome, data_cadastro) VALUES
('Agropecuária São Jorge', '2024-01-10'),
('Cooperativa do Vale', '2024-02-05'),
('Fazenda Boa Esperança', '2024-03-12'),
('Cerealista Nacional', '2024-04-01'),
('Comercial Agrícola Sul', '2024-04-08'),
('Fazendinha da Silva','2023-08-12');

INSERT INTO produtos (nome, categoria, preco) VALUES
('Soja', 'Grãos', 150.00),        -- preço por saca de 60kg
('Milho', 'Grãos', 90.00),
('Trigo', 'Grãos', 110.00),
('Arroz', 'Grãos', 95.00),
('Feijão', 'Grãos', 180.00),
('Sorgo', 'Grãos', 70.00),
('Cevada', 'Grãos', 100.00);

INSERT INTO pedidos (data_pedido, valor_total, id_cliente) VALUES
('2024-04-10', 7500.00, 1),
('2024-04-12', 4500.00, 2),
('2024-04-13', 9900.00, 3),
('2024-04-14', 2850.00, 4),
('2024-04-15', 3600.00, 5),
('2024-12-20', 8500.00, 1),
('2024-11-12', 2500.00, 2),
('2024-08-13', 19900.00, 3),
('2024-09-14', 21850.00, 4),
('2024-10-15', 10600.00, 5);

INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(1, 1, 50, 150.00), -- 50 sacas de soja
(1, 2, 20, 90.00),  -- 20 sacas de milho

(2, 3, 30, 110.00), -- trigo
(2, 4, 10, 95.00),  -- arroz

(3, 1, 60, 150.00), -- soja
(3, 5, 20, 180.00), -- feijão
(3, 6, 30, 70.00),  -- sorgo

(4, 7, 15, 100.00), -- cevada
(4, 2, 10, 90.00),  -- milho

(5, 4, 20, 95.00),  -- arroz
(5, 5, 10, 180.00), -- feijão

(1, 1, 60, 150.00), -- 60 sacas de soja
(1, 2, 30, 90.00),  -- 30 sacas de milho

(2, 3, 100, 110.00), -- trigo
(2, 4, 120, 95.00),  -- arroz

(3, 1, 90, 150.00), -- soja
(3, 5, 50, 180.00), -- feijão
(3, 6, 60, 70.00),  -- sorgo

(4, 7, 25, 100.00), -- cevada
(4, 2, 100, 90.00),  -- milho

(5, 4, 110, 95.00),  -- arroz
(5, 5, 100, 180.00); -- feijão