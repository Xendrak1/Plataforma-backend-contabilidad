-- TRUNCATE actualizado según tus tablas actuales
TRUNCATE TABLE 
    lecturas_comunicado,
    comunicados,
    pagos,
    multas,
    tipos_infraccion,
    reservas,
    areas_comunes,
    visitas,
    visitantes,
    parqueos_usuario,
    parqueos,
    vehiculos,
    tipos_vehiculo,
    residente_vivienda,
    usuario_roles,
    usuarios,
    roles,
    mascotas,
    personas,
    viviendas,
    categorias_vivienda,
    expensas,
    condominios
RESTART IDENTITY CASCADE;

-- CONDOMINIO
INSERT INTO condominios (nombre, ciudad)
VALUES ('Condominio KE', 'Santa Cruz');

-- CATEGORIAS DE VIVIENDA
INSERT INTO categorias_vivienda 
(nombre, habitaciones, banos, churrasquera, pisos, cochera, jardin, balcon, descripcion) VALUES 
('Casa Familiar',	 3, 2, TRUE,	 1, 1, TRUE,	 TRUE,	'Casa unifamiliar con 3 habitaciones y churrasquera'),
('Casa Pequeña',	 2, 1, FALSE,	 1, 1, TRUE,	 TRUE,	'Casa pequeña de 2 habitaciones con mini balcon'),
('Casa Grande',	 4, 3, TRUE,	 2, 2, TRUE,	 TRUE,	'Casa grande de 4 habitaciones, ideal para familias'),
('Casa Suit',		 6, 4, TRUE,	 2, 2, TRUE,	 TRUE, 	'Casa tipo suit con 6 habitaciones'),
('Casa Mansion',	 8, 6, TRUE,	 3, 3, TRUE,	 TRUE, 	'Mansión con 8 habitaciones, amplio jardín y lujo total');

--VIVIENDAS POR SECTOR
INSERT INTO viviendas (categoria_id, codigo, metros2, ubicacion, activo)
VALUES
(1, 'CN-001', 150, 'Sector Norte', TRUE),	/*1 CF-3 -*/
(2, 'CN-002', 100, 'Sector Norte', TRUE),	/*2 CP-2 -*/
(3, 'CN-003', 200, 'Sector Norte', TRUE),	/*3 CG-4 -*/
(4, 'CN-004', 250, 'Sector Norte', FALSE),	/*4 CS-6*/
(5, 'CN-005', 300, 'Sector Norte', FALSE), 	/*5 CM-8*/

(1, 'CS-001', 150, 'Sector Sur', TRUE),		/*6 CF-3 -*/
(2, 'CS-002', 100, 'Sector Sur', TRUE),		/*7 CP-2 -*/
(3, 'CS-003', 200, 'Sector Sur', TRUE),		/*8 CG-4 -*/
(4, 'CS-004', 250, 'Sector Sur', FALSE),		/*9 CM-6*/
(5, 'CS-005', 300, 'Sector Sur', FALSE),		/*10 CS-8*/

(1, 'CE-001', 150, 'Sector Este', TRUE),		/*11 CF-3 -*/
(2, 'CE-002', 100, 'Sector Este', TRUE),		/*12 CP-2 -*/
(3, 'CE-003', 200, 'Sector Este', FALSE),	/*13 CG-4*/
(4, 'CE-004', 250, 'Sector Este', FALSE),	/*14 CS-6*/
(5, 'CE-005', 300, 'Sector Este', FALSE),	/*15 CM-8*/

(1, 'CO-001', 150, 'Sector Oeste', TRUE),	/*16 CF-3 -*/
(2, 'CO-002', 100, 'Sector Oeste', TRUE),	/*17 CP-2 -*/
(3, 'CO-003', 200, 'Sector Oeste', FALSE),	/*18 CG-4*/
(4, 'CO-004', 250, 'Sector Oeste', FALSE),	/*19 CS-6*/
(5, 'CO-005', 300, 'Sector Oeste', FALSE);	/*20 CM-8*/

-- PERSONAS (propietarios y familias)
INSERT INTO personas (nombres, apellidos, num_doc, telefono, email) VALUES
/*1*/('Juan', 'Pérez','10001','76543210','juan@email.com'),
/*2*/('Ana', 'Pérez','10002','76543211','ana@email.com'),
/*3*/('Luis', 'Pérez','10003','76543212','luis@email.com'),

/*4*/('Carlos', 'Gutiérrez','10004','76543213','carlos@email.com'),
/*5*/('María', 'Gutiérrez','10005','76543214','maria@email.com'),
/*6*/('Sofía', 'Gutiérrez','10006','76543215','sofia@email.com'),

/*7*/('Pedro', 'Quispe','10007','76543216','pedro@email.com'),
/*8*/('Lucía', 'Quispe','10008','76543217','lucia@email.com'),

/*9*/('Mario', 'Lopez','10009','76543218','mario@email.com'),
/*10*/('Elena', 'Lopez','10010','76543219','elena@email.com'),

/*11*/('Diego', 'Torres','10011','76543220','diego@email.com'),
/*12*/('Valeria', 'Torres','10012','76543221','valeria@email.com'),

/*13*/('Raúl', 'Sánchez','10013','76543222','raul@email.com'),
/*14*/('Paula', 'Sánchez','10014','76543223','paula@email.com'),

/*15*/('Andrés', 'Vargas','10015','76543224','andres@email.com'),
/*16*/('Carla', 'Vargas','10016','76543225','carla@email.com'),

/*17*/('Fernando', 'Rojas','10017','76543226','fernando@email.com'),
/*18*/('Natalia', 'Rojas','10018','76543227','natalia@email.com'),

/*19*/('Javier', 'Flores','10019','76543228','javier@email.com'),
/*20*/('Gabriela', 'Flores','10020','76543229','gabriela@email.com');

-- USUARIOS Y ROLES
INSERT INTO roles (nombre) VALUES ('ADMIN'),('GUARDIA'),('RESIDENTE');

INSERT INTO usuarios (persona_id, email_login, hash_password, estado) VALUES
(1,'juanperez','adminJUAN',TRUE),
(2,'anaperez','adminANA',TRUE),
(4,'carlosguardia','guardia123',TRUE),
(7,'pedroquispe','adminPEDRO',TRUE),
(9,'mariolopez','adminMARIO',TRUE),
(11,'diegotorrez','adminIDIEGO',TRUE),
(13,'raulsanchez','adminRAUL',TRUE),
(15,'andresvargas','adminANDRES',TRUE),
(17,'fernandorojas','adminFERNANDO',TRUE),
(19,'javierflores','adminJAVIER',TRUE);

INSERT INTO usuario_roles (usuario_id, rol_id) VALUES
(1,1),(2,2),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1);

-- RESIDENTE CLASIFICACION PROPIETARIO(S)
INSERT INTO residente_vivienda (persona_id, vivienda_id, es_propietario, inicio, estado) VALUES
(1,1,TRUE,'2025-09-01',TRUE),	/*1 CF-3 -*/
(2,1,TRUE,'2025-09-01',TRUE),	/*1 CF-3 -*/
(3,1,FALSE,'2025-09-01',TRUE),	/*1 CF-3 -*/

(4,6,TRUE,'2025-09-05',TRUE),	/*6 CF-3 -*/
(5,6,FALSE,'2025-09-05',TRUE),	/*6 CF-3 -*/
(6,6,FALSE,'2025-09-05',TRUE),	/*6 CF-3 -*/

(7,2,TRUE,'2025-09-10',TRUE),	/*2 CP-2 -*/
(8,2,FALSE,'2025-09-10',TRUE),	/*2 CP-2 -*/

(9,7,TRUE,'2025-09-12',TRUE),	/*7 CP-2 -*/
(10,7,FALSE,'2025-09-12',TRUE),	/*7 CP-2 -*/

(11,12,TRUE,'2025-09-12',TRUE),	/*12 CP-2 -*/
(12,12,FALSE,'2025-09-12',TRUE),/*12 CP-2 -*/

(13,17,TRUE,'2025-09-12',TRUE),	/*17 CP-2 -*/
(14,17,FALSE,'2025-09-12',TRUE),/*17 CP-2 -*/

(15,11,TRUE,'2025-09-12',TRUE),	/*11 CF-3 -*/
(16,11,FALSE,'2025-09-12',TRUE),/*11 CF-3 -*/

(17,16,TRUE,'2025-09-12',TRUE),	/*16 CF-3 -*/
(18,16,FALSE,'2025-09-12',TRUE),/*16 CF-3 -*/

(19,3,TRUE,'2025-09-12',TRUE),	/*3 CG-4 -*/
(20,3,FALSE,'2025-09-12',TRUE);	/*3 CG-4 -*/

INSERT INTO tipos_vehiculo (nombre) VALUES
('AUTO'),
('MOTO'),
('CAMIONETA'),
('CAMION');

-- VEHICULOS
INSERT INTO vehiculos (persona_id, vivienda_id, tipo_id, placa, modelo, color) VALUES
(1, 1, 1, 'ABC-123', 'Toyota Corolla', 'Blanco'), /*g*/
(2, 1, 1, 'DEF-456', 'Honda Civic', 'Negro'),	/*g*/
(3, 1, 1, 'GHI-789', 'Suzuki Swift', 'Rojo'),		/*g*/

(4, 6, 1, 'JKL-012', 'Nissan Versa', 'Azul'),	/*g*/
(5, 6, 1, 'MNO-345', 'Chevrolet Spark', 'Gris'),	/*g*/

(7, 2, 1, 'PQR-678', 'Ford Fiesta', 'Negro'),	/*g*/

(9, 7, 1, 'STU-901', 'Kia Rio', 'Blanco'),		/*g*/

(11, 12, 1, 'VWX-234', 'Hyundai i20', 'Rojo'),	/*g*/
(12, 12, 1, 'YZA-567', 'Volkswagen Polo', 'Azul'),/*p*/

(13, 17, 1, 'BCD-890', 'Honda Fit', 'Blanco'),	/*g*/

(15, 11, 3, 'EFG-123', 'Ford Ranger', 'Gris'),	/*g*/

(17, 16, 3, 'HIJ-456', 'Chevrolet S10', 'Negro'), /*g*/

(19, 3, 2, 'KLM-789', 'Yamaha R3', 'Rojo');	/*g*/

-- Inserción de parqueos físicos
INSERT INTO parqueos (codigo, ocupado) VALUES
('P-001',TRUE),
('P-002',TRUE),
('P-003',TRUE),
('P-004',TRUE),
('P-005',TRUE),
('P-006',TRUE),
('P-007',TRUE),
('P-008',TRUE),
('P-009',TRUE),
('P-010',TRUE),
('P-011',FALSE),
('P-012',FALSE),
('P-013',FALSE),
('P-014',FALSE),
('P-015',FALSE),
('P-016',FALSE),
('P-017',FALSE),
('P-018',FALSE),
('P-019',FALSE),
('P-020',FALSE),
('P-021',FALSE),
('P-022',FALSE),
('P-023',FALSE),
('P-024',FALSE),
('P-025',FALSE),
('P-026',FALSE),
('P-027',FALSE),
('P-028',FALSE),
('P-029',FALSE),
('P-030',FALSE),
('P-031',FALSE),
('P-032',FALSE),
('P-033',FALSE),
('P-034',FALSE),
('P-035',FALSE),
('P-036',FALSE),
('P-037',FALSE),
('P-038',FALSE),
('P-039',FALSE),
('P-040',FALSE);

--USO DE PARQUEO
INSERT INTO parqueos_usuario (parqueo_id, vivienda_id, tipo, fecha_reserva) VALUES
(1,1,'COMPRA','2025-09-20'),
(2,1,'MENSUAL','2025-09-20'),
(3,2,'COMPRA','2025-09-20'),
(4,3,'COMPRA','2025-09-20'),
(5,6,'COMPRA','2025-09-20'),
(6,7,'COMPRA','2025-09-20'),
(7,11,'COMPRA','2025-09-20'),
(8,12,'COMPRA','2025-09-20'),
(9,16,'COMPRA','2025-09-20'),
(10,17,'COMPRA','2025-09-20');

-- MASCOTAS
INSERT INTO mascotas (nombre,tipo,raza,edad,vivienda_id) VALUES
('Rex','Perro','Labrador',3,1),
('Michi','Gato','Siames',2,1),
('Bolt','Perro','Husky',1,2),
('Luna','Gato','Persa',4,2),
('Rocky','Perro','Bulldog',2,3);

-- AREAS COMUNES
INSERT INTO areas_comunes (nombre, requiere_pago, tarifa, reglas) VALUES
('Piscina', TRUE, 50, 'Uso máximo 3 horas, solo residentes y acompañantes'),
('Gimnasio', FALSE, NULL, 'Horario: 6:00 - 22:00, uso responsable de máquinas'),
('Parque Infantil', FALSE, NULL, 'Solo niños menores de 12 años, acompañados de un adulto'),
('Salón de Juegos', TRUE, 100, 'Reservar con 24h de anticipación, máximo 4 horas'),
('Terraza/Deck', TRUE, 150, 'Eventos privados, limpieza obligatoria'),
('Área de BBQ', TRUE, 80, 'Reservar con 24h de anticipación, máximo 3 horas'),
('Cancha de Tenis', TRUE, 50, 'Reservar 24h antes, uso por turnos de 1 hora'),
('Sala de Reuniones', TRUE, 120, 'Reservar con 48h de anticipación, máximo 4 horas'),
('Cine/Media Room', TRUE, 150, 'Reservar con 24h de anticipación, máximo 3 horas'),
('Zona de Mascotas', FALSE, NULL, 'Mascotas bajo supervisión, limpieza obligatoria');

-- RESERVAS
INSERT INTO reservas (codigo,area_id,vivienda_id,persona_id,fecha,hora_inicio,hora_fin,estado) VALUES
('R-001',1,1,1,'2025-09-15','2025-09-15 18:00','2025-09-15 23:00','CONFIRMADA'),
('R-002',2,2,4,'2025-09-18','2025-09-18 09:00','2025-09-18 11:00','PENDIENTE');

-- VISITANTES
INSERT INTO visitantes (nombres,apellidos,num_doc) VALUES
('María','López','20001'),
('Pedro','Quispe','20002');

--VISITAS
INSERT INTO visitas (visitante_id,vivienda_destino_id,medio) VALUES
(1,1,'QR'),
(2,2,'MANUAL');

-- EXPENSAS
INSERT INTO expensas (codigo,vivienda_id,periodo,monto,vencimiento,estado) VALUES
('EXP-001',1,'2025-09',500.00,'2025-09-30','PENDIENTE'),
('EXP-002',2,'2025-09',450.00,'2025-09-30','PAGADA');

-- PAGOS
INSERT INTO pagos (vivienda_id,persona_id,concepto,monto,metodo,estado) VALUES
(1,1,'EXPENSA',500.00,'QR','PENDIENTE'),
(2,4,'EXPENSA',450.00,'TRANSFERENCIA','CONFIRMADO');
