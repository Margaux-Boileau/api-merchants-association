# Forum API for a Merchants Association

¡Bienvenido/a a la API REST de Foros para la Asociación de Comerciantes! Esta API proporciona un conjunto de endpoints para la gestión de un sistema de foros destinado a la comunicación entre los miembros de la asociación.

## Features

- Utiliza Django REST Framework para proporcionar una API RESTful.
- Usa SQLite como base de datos.
- Implementa autenticación mediante tokens para proteger los endpoints.
- Utiliza Firebase Cloud Messaging para enviar notificaciones cuando se publica un nuevo post en el foro.

## Instalación

1. Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/Margaux-Boileau/api-merchants-association.git
```

2. Instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

3. Ejecuta las migraciones de la base de datos:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

La API estará disponible en `http://localhost:8000/`.  

El panel de administrador se puede acceder a  `http://localhost:8000/admin/`.

## Autores

Desarrollado por [Margaux Boileau](https://github.com/Margaux-Boileau), [Óscar Perona Gómez](https://github.com/peronaOscar), [Lorenzo Poderoso Dalmau](https://github.com/LorenzoDalmaau)
