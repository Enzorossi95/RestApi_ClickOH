# RestApi_ClickOH
Rest API Click OH Challenge

Para poner en funcionamiento el codigo:

1) docker compose build
2) docker compse up

Se va a crear un volumen para la base de datos y un volumen para el contenedor WEB.

Se creara un super user con user: admin y pass: admin.

ingresando a http://localhost:8000 se podra visualizar el API ROOT.

para realizar los test se debe ingresar por docker exec a la cli del contenedor WEB y ejecutar python manage.py test .

