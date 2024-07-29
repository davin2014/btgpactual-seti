-- Insertar datos en la tabla Cliente
INSERT INTO Cliente (id, nombre, apellidos, ciudad)
VALUES 
(1, 'Juan', 'Perez', 'Bogotá'),
(2, 'Maria', 'Gomez', 'Medellín'),
(3, 'Luis', 'Rodriguez', 'Cali');

-- Insertar datos en la tabla Sucursal
INSERT INTO Sucursal (id, nombre, ciudad)
VALUES 
(1, 'Sucursal Norte', 'Bogotá'),
(2, 'Sucursal Sur', 'Medellín'),
(3, 'Sucursal Este', 'Cali');

-- Insertar datos en la tabla Producto
INSERT INTO Producto (id, nombre, tipoProducto)
VALUES 
(1, 'Producto A', 'Tipo 1'),
(2, 'Producto B', 'Tipo 2'),
(3, 'Producto C', 'Tipo 3');

-- Insertar datos en la tabla Inscripción
INSERT INTO Inscripción (idProducto, idCliente)
VALUES 
(1, 1),
(2, 2),
(3, 3);

-- Insertar datos en la tabla Disponibilidad
INSERT INTO Disponibilidad (idSucursal, idProducto)
VALUES 
(1, 1),
(2, 2),
(3, 3);

-- Insertar datos en la tabla Visitan
INSERT INTO Visitan (idSucursal, idCliente, fechaVisita)
VALUES 
(1, 1, '2024-01-01'),
(2, 2, '2024-01-02'),
(3, 3, '2024-01-03');