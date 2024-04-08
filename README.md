## Descripcion del Problema

Se requiere la construcción de dos microservicios, uno de ellos para que los usuarios externos puedan consultar los inmuebles en la BD de acuerdo a los filtros que deseen y el otro para que los usuarios puedan dar un "Me Gusta" a un inmueble en específico

## Tecnologias a Usar
- Python
- Virtualenv
- mysql-connector-python

## Dudas
- Realizar microservicios sin hacer uso de un framework (Por lo general uso django)
- Manejo de Solicitudes HTTP, como dirigir las solicitudes a los manejadores correspondientes (el Ruteo)

## Resolucion de Problemas
- Hacemos uso de mysql-connector-python para evitar el uso de ORMs y directamente tratar con las consultas SQL directamente.
- Hacemos uso de http.server que permite implementar un servidor web básico. Con esta podemos construir los manejadores de las solicitudes HTTP y por ende podemos manejar las distintas rutas que tengamos, con esto podemos manejar los microservicios que tengamos, aunque para estos casos es mejor hacer uso de un framework tipo Flask o FastAPI


## Segundo Requerimiento
 Para este requerimiento se propone adicionar dos nuevas tablas, que serían la tabla Usuarios y la tabla Likes, entre las cuales habría una relación dado que un usuario puede dar "Me Gusta" a muchos inmuebles pero un "Me Gusta" específico está asociado a un solo usuario. Ahora bien, entre la tabla Property y la tabla Likes habría una relación dado que un inmueble puede recibir "Me Gusta" de muchos usuarios, pero un "Me Gusta" específico, perfenece a un solo inmueble, a nivel visual sería algo así:

+--------------+
|    Usuarios  |
| user_id (PK) |
| username     |
| email        |
+--------------+
       |
       | 1
       |
       | M
+---------------+        +------------------------+
|     Likes     |------>|        Property        |
|               |       | property_id (PK)       |
| like_id (PK)  |       | address                |
| user_id (FK)  |       | city                   |
| property_id (FK) |    | price                  |
| timestamp     |       | description            |
+--------------+        | year                   |
                        +-----------------------+



## Extra Points
Para mejorar la velocidad de las consultas en la base de datos se puede considerar tener en la tabla property un atributo current_status_id, lo cual evitaría realizar joins complejos para obtener el estado más reciente de una propiedad. Adicionalmente añadir un campo desnormalizado like_count el cual permita tener un conteo rápido de los "Me Gusta" que tiene una propiedad, para descartar la necesidad de hacer un count de todos los likes cada que se quiera saber cuantos likes tiene una propiedad.