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