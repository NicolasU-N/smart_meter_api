# smart_meter_api

El proyecto smart_meter_api es un API desarrollado en Django que tiene como objetivo recolectar la información de nodos LoRaWAN que están monitoreando variables de consumo hídrico. Esta API permitirá gestionar el estado y configuración de cada nodo conectado a la red, así como también visualizar los datos de consumo hídrico.

# Uso

```
$ python manage.py makemigrations && python manage.py migrate && python manage.py runserver

$ mqttasgi -H localhost -p 1883 project.asgi:application

$ mosquitto_pub -h localhost -t iot/smart_meters/data -m "{\"EUI\":\"70-b3-d5-49-90-0d-17-d6\",\"SNR\":3.5,\"RSSI\":-203,\"Modinf\":\"SF9BW125\",\"CodRate\":\"4/5\",\"Freq\":915.8,\"Size\":24,\"Payload\":\"1;10.1;80\"}"
```
## Instalación

```
$ pip install -r requirements.txt

$ docker run --hostname=c3b14f773242 --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=GOSU_VERSION=1.14 --env=REDIS_VERSION=5.0.14 --env=REDIS_DOWNLOAD_URL=http://download.redis.io/releases/redis-5.0.14.tar.gz --env=REDIS_DOWNLOAD_SHA=3ea5024766d983249e80d4aa9457c897a9f079957d0fb1f35682df233f997f32 --volume=/data --workdir=/data -p 6379:6379 --restart=no --runtime=runc -d redis:5
```





<!-- ## Instalación

Instrucciones para instalar el proyecto y sus dependencias.

## Configuración

Instrucciones para configurar el proyecto y sus variables de entorno.

## Uso

Instrucciones para utilizar el proyecto. Incluye ejemplos de uso si es posible.

## Créditos

Información sobre los autores del proyecto y las fuentes de inspiración. -->

