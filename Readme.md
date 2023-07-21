# Prueba DjangoRestFramework

[![.NET Core 6.0](https://img.shields.io/badge/Django_Rest_Framework-blue)]() [![PostgreSQL 14](https://img.shields.io/badge/PostgreSQL_14-purple)]()

## Autora
- [Ericka Ramos León](https://github.com/eramos1002)

## Notas
Para abrir el proyecto es necesario ir al fichero `settings.py` y establecer los valores de la conexión con la base de datos PostgreSQL en la variable DATABASES.

## Prerequisitos
Antes de comenzar, asegúrate de cumplir con los siguientes requisitos:

* Tener instalado Docker y Docker Compose en tu sistema. (opcional si no esta instalado postgres)
* Contar con Python
* Disponer de pip, el administrador de paquetes de Python.

## Instalación y configuración
### Paso 1: Clonar el repositorio
````
git clone https://github.com/eramos1002/django-rest-eshop.git
cd django-rest-eshop
````
### Paso 2: Crear y activar un entorno virtual
````
python -m venv venv
venv\Scripts\activate.bat
````
### Paso 3: Iniciar servicios de Docker (Postgres)
Si no tiene instalado postgres, ejecutar el siguiente comando:
````
docker-compose up -d
````
### Paso 4: Instalar las dependencias
````
pip install -r requirements.txt
````
### Paso 5: Aplicar las migraciones de Django
Para crear las tablas en la base de datos 
````
python manage.py migrate
````

## Uso
### Iniciar el servidor
En una terminal, ejecutar el siguiente comando:
````
python manage.py runserver
````
### Documentación Swagger
Para ver la docuemntación de las apis
````
Abrir un navegador poner en la dirección: http://127.0.0.1:8000/docs/
````
### Ejecutar test
````
python manage.py test --verbosity=2

````
Si desea ver el estado de cada caso
````
python manage.py test --verbosity=2

````