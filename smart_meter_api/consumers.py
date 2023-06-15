import logging
import django
import os
import json
from datetime import datetime
from asgiref.sync import sync_to_async
from mqttasgi.consumers import MqttConsumer

from channels.generic.websocket import AsyncWebsocketConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.contrib.auth.models import User
from smart_meter_api.models import Device
from smart_meter_api.models import Measurement

logger = logging.getLogger(__name__)
MQTT_TOPIC = "iot/smart_meters/data"


async def process_mqtt_message(mqtt_message):
    try:
        payload = json.loads(mqtt_message["payload"].decode("UTF-8"))

        if all(key in payload for key in ("EUI", "RSSI", "SNR", "Payload")):
            user_id, volume, battery_level = payload["Payload"].split(";")

            if user_id and volume and battery_level:
                try:
                    # Fetch user
                    user = await sync_to_async(User.objects.get)(id=user_id)

                    # Create or update device
                    device, created = await sync_to_async(Device.objects.get_or_create)(
                        eui=payload["EUI"], user=user
                    )

                    device.updated_at = datetime.now()
                    await sync_to_async(device.save)()

                    # Create measurement
                    measurement = Measurement(
                        device=device,
                        rssi=payload["RSSI"],
                        snr=payload["SNR"],
                        modinfo=payload["Modinf"],
                        codrate=payload["CodRate"],
                        freq=payload["Freq"],
                        size=payload["Size"],
                        payload=payload["Payload"],
                        volume=float(volume),
                        battery_level=float(battery_level),
                    )

                    await sync_to_async(measurement.save)()

                    return {
                        "id": device.id,
                        "eui": device.eui,
                        "rssi": measurement.rssi,
                        "snr": measurement.snr,
                        "volume": measurement.volume,
                        "battery_level": measurement.battery_level,
                        "updated_at": device.updated_at.isoformat() + "Z",
                    }
                except Exception as e:
                    logger.error("Failed to create device and measurement: %s", e)

            else:
                logger.error(
                    "Payload %s is not in the correct format.", payload["Payload"]
                )

        else:
            logger.error(
                "Invalid payload received: %s", mqtt_message["payload"].decode("UTF-8")
            )
    except User.DoesNotExist:
        logger.error("User with id %s does not exist.", user_id)
    except ValueError:
        logger.error("Payload %s is not in the correct format.", payload["Payload"])
    except Exception as e:
        logger.error("Error processing message: %s", e)

    return None


class MyMqttConsumer(MqttConsumer):
    async def connect(self):
        await self.subscribe(MQTT_TOPIC, 0)

    async def receive(self, mqtt_message):
        logger.info("Received a message at topic: %s", mqtt_message["topic"])
        logger.info("Payload: %s", mqtt_message["payload"])
        logger.info("QOS: %s", mqtt_message["qos"])

        message = await process_mqtt_message(mqtt_message)
        if message:
            # Send message to websocket
            await self.channel_layer.group_send(
                "dashboard", {"type": "ws_dashboard_data", "value": message}
            )

    async def disconnect(self):
        await self.unsubscribe(MQTT_TOPIC)


class MyWsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.groupname = "dashboard"
        await self.channel_layer.group_add(self.groupname, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        logger.info(">>>> %s", text_data)
        # datapoint = json.loads(text_data)
        # val = datapoint["value"]
        # await self.channel_layer.group_send(
        #     self.groupname, {"type": "deprocessing", "value": val}
        # )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.groupname, self.channel_name)

    async def ws_dashboard_data(self, event):
        logger.info("Send channel layer message to websocket")
        logger.info("event -> %s", event)
        e_value = event["value"]
        await self.send(text_data=json.dumps({"value": e_value}))
