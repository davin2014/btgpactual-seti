SELECT DISTINCT Cliente.nombre
FROM Cliente
JOIN Inscripción ON Cliente.id = Inscripción.idCliente
JOIN Disponibilidad ON Inscripción.idProducto = Disponibilidad.idProducto
JOIN Visitan ON Cliente.id = Visitan.idCliente AND Disponibilidad.idSucursal = Visitan.idSucursal;