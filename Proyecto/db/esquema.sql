CREATE TABLE IF NOT EXISTS EstadoSolicitud (
    id_estado_solicitud INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(9) NOT NULL, -- "En espera", "Aceptada", "Rechazada"
    descripcion VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(20) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    rol VARCHAR(15) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS TipoUbicacion (
    id_tipo_ubicacion INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(25) NOT NULL UNIQUE,
    descripcion VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS EstadoUbicacion (
    id_estado_ubicacion INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(25) NOT NULL,
    descripcion VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Ubicacion (
    id_ubicacion INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    codigo VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    coordenadas VARCHAR(100) NOT NULL,
    fk_tipo INT NOT NULL,
    fk_estado INT NOT NULL,
    FOREIGN KEY (fk_tipo) REFERENCES TipoUbicacion(id_tipo_ubicacion),
    FOREIGN KEY (fk_estado) REFERENCES EstadoUbicacion(id_estado_ubicacion)
);

CREATE TABLE IF NOT EXISTS Solicitud (
    id_solicitud INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    facultad VARCHAR(100),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    respuesta TEXT,
    fk_estado INT NOT NULL DEFAULT 1,
    creado_por INT NOT NULL,
    gestionado_por INT,
    fk_ubicacion INT NOT NULL,
    FOREIGN KEY (fk_ubicacion) REFERENCES Ubicacion(id_ubicacion),
    FOREIGN KEY (fk_estado) REFERENCES EstadoSolicitud(id_estado_solicitud),
    FOREIGN KEY (creado_por) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (gestionado_por) REFERENCES Usuario(id_usuario),
    CONSTRAINT Chequeo_respuesta CHECK (
        (gestionado_por IS NULL) OR (respuesta IS NOT NULL)
    )
);

CREATE TABLE IF NOT EXISTS Favorito (
    id_favorito INT PRIMARY KEY AUTO_INCREMENT,
    fk_usuario INT NOT NULL,
    fk_ubicacion INT NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (fk_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (fk_ubicacion) REFERENCES Ubicacion(id_ubicacion)
);

CREATE TABLE IF NOT EXISTS Evento (
    id_evento INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    inicio DATETIME NOT NULL,
    fin DATETIME NOT NULL,
    fk_ubicacion INT NOT NULL,
    fk_solicitud_asociada INT,
    FOREIGN KEY (fk_ubicacion) REFERENCES Ubicacion(id_ubicacion),
    FOREIGN KEY (fk_solicitud_asociada) REFERENCES Solicitud(id_solicitud)
);

