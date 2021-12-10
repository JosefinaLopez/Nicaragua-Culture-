CREATE table usuario (
    iduser serial not null PRIMARY KEY,
    username varchar not null,
    password varchar not null , 
    isadmin BOOLEAN not null,
); 
   SELECT *from usuario

CREATE table publication (
    idpublication serial not null PRIMARY KEY,
    iduser INTEGER REFERENCES usuario,
    contenido  varchar not null,
    timedate  time no null,
);  
   SELECT *from publication 

CREATE table comentarios (
    idcometarios serial not null PRIMARY KEY,
    idpublicacion INTEGER REFERENCES publication,
    comentarios varchar not null,
    iduser INTEGER REFERENCES usuario
);
ALTER TABLE  comentarios
RENAME COLUMN idpublicacion
TO idpublication;

SELECT *from comentarios