# README #

## Management Commands
Use `python manage.py generate-pedidos <int>` to generate X amount of random `Pedido`'s 

Use `python manage.py generate-repairman <int>` to generate X amount of random `Repairman`'s

## Endpoint's expected responses
### ```GET api/repairman/```
```json
[
    {
        "full_name": "Manuel Gutierrez",
        "hours_worked": 6,
        "total_pay": 1020.0,
        "orders": 1
    },
    {
        "full_name": "Simon Correa",
        "hours_worked": 3,
        "total_pay": 510.0,
        "orders": 1
    }
]
```

### ```GET api/repairman/summary/```
```json
{
    "average_pay": 765.0,
    "below_average": [
        {
            "full_name": "Simon Correa",
            "hours_worked": 3,
            "total_pay": 510.0,
            "orders": 1
        }
    ],
    "min_pay": "Simon Correa",
    "max_pay": "Manuel Gutierrez"
}
```

## Instalar Docker

* Mac y Windows: [Docker Desktop](https://www.docker.com/products/docker-desktop)
* Ubuntu: [ Docker ](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-es) & [Docker Compose](https://docs.docker.com/compose/install/)


## Run
* Clonar repository
* Verificar puertos
* Docker run
* Inicializar la base de datos 
* How to run tests

### Revisar si el puerto 80 esta ocupado. 

Debian:
```bash
netstat -tulpn | grep 80
```
Mac:
```bash
sudo lsof -i :80
```
```bash
docker-compose build
docker-compose up
docker-compose ps

    Name                  Command               State                    Ports                  
------------------------------------------------------------------------------------------------
test_nginx_1   /docker-entrypoint.sh ngin ...   Up      0.0.0.0:80->80/tcp,:::80->80/tcp        
test_web_1     python manage.py runserver ...   Up      0.0.0.0:8000->8000/tcp,:::8000->8000/tcp
```

```bash
docker exec test_web_1  python manage.py  makemigrations rapihogar
docker exec test_web_1  python manage.py  migrate
```
### Datos de prubas 
```bash
python manage.py loaddata rapihogar/fixtures/user.json --app rapihogar.user
python manage.py loaddata rapihogar/fixtures/company.json --app rapihogar.company
python manage.py loaddata rapihogar/fixtures/user.scheme --app rapihogar.scheme
python manage.py loaddata rapihogar/fixtures/pedido.json --app rapihogar.pedido
```
or 
```bash
docker exec -it test_web_1 python manage.py createsuperuser
```
### Run test ###

```bash
docker exec -it test_web_1 python manage.py test
```
# Tarea a realizar #
Rapihogar, necesita cargar las horas trabajadas por los técnicos  para poder realizar la liquidación. Se pide:

### 1. ###
Crear el modelo para cargar técnicos y crear al menos 5 técnicos

### 2. ###
Realizar un Comando que genere N pedidos  (N, será el número de pedidos a cargar, que se deberá ingresar)

* N sólo puede contener valores entre 1 (inclusive) y 100 (inclusive).
* Seleccionar un Técnico aleatoriamente
* Seleccionar un Cliente  aleatoriamente
* Asigne horas trabajadas entre 1 y 10

### 3. ###
Luego de cargar todos los datos crear un servicio web que liste todos los técnicos y calcule el pago según las horas trabajadas 

Cálculo de Pago según la siguiente tabla:

| Cantidad De Horas | Valor Hora  | Porcentaje de descuento  |
| --------   | -------- | -------- |
|  0-14 | 200 | 15% |
| 15-28 | 250 | 16% |
| 29-47 | 300 | 17% |
|  >48 | 350 | 18% |

	
	Por ejemplo: Trabajador “Larusso Daniel”, Horas trabajadas = 20
		total = (20 * 250) – (20 * 250 * 0.16)
		total = (5.000) – (800)
		total = 4.200
		
Luego realizar un servicio que muestre un listado completo de técnicos, que debería ser algo así:

* Nombre completo 
* Horas Trabajadas  
* Total a Cobrar
* Cantidad de pedidos en los que trabajo

```
 El listado se debe poder filtrar por parte del nombre 
```
### 4. ###
Luego realizar un servicio que muestre un informe que contenga:

* mostrar el monto promedio cobrado por todos los técnicos.
* mostrar los datos de todos los técnicos que cobraron menos que el promedio.
* El último trabajador ingresado que cobró el monto más bajo.
* El último trabajador ingresado que cobró el monto más alto.

### Nota. ### 

Para la implementación de las API's utilizar solo las clases necesarias, no exponer metodos publicos que no se necesitan.
