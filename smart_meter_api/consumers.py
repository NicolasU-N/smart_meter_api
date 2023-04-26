import django
import os
import json
from datetime import datetime
from asgiref.sync import sync_to_async
from mqttasgi.consumers import MqttConsumer

from channels.generic.websocket import AsyncWebsocketConsumer


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

django.setup()

from .models import Device


class MyMqttConsumer(MqttConsumer):
    async def connect(self):
        await self.subscribe("my/testing/topic", 0)

    async def receive(self, mqtt_message):
        print(
            f"{datetime.now()} -- Received a message at topic: { mqtt_message['topic'] }"
        )
        print(f"With payload: { mqtt_message['payload'] }")
        print(f"And QOS: { mqtt_message['qos']}\n")

        # ? update
        # device = await sync_to_async(Device.objects.get)(eui='70-b3-d5-49-98-9c-58-a4')
        # device.rssi = -200
        # await sync_to_async(device.save)()
        # ? create new device
        try:
            payload = json.loads(mqtt_message["payload"].decode("UTF-8"))
            # validate payload contains required keys
            if all(key in payload for key in ("EUI", "RSSI", "SNR", "Payload")):
                device = await sync_to_async(Device.objects.create)(
                    eui=payload["EUI"],
                    rssi=payload["RSSI"],
                    snr=payload["SNR"],
                    payload=payload["Payload"],
                )
                await sync_to_async(device.save)()
                print(f"Device {device.eui} created")
                # ? channel layer: send message to websocket
                await self.channel_layer.group_send(
                    "dashboard",
                    {"type": "ws_dashboard_data", "value": payload["Payload"]},
                )
            else:
                # print(f"Invalid payload received: {mqtt_message['payload']}")
                print(
                    "Invalid payload received: ",
                    mqtt_message["payload"].decode("UTF-8"),
                )
        except json.JSONDecodeError as e:
            print(
                "Invalid JSON payload received: ",
                mqtt_message["payload"].decode("UTF-8"),
            )
        except Exception as e:
            print(f"Error processing message: {e}")

    async def disconnect(self):
        await self.unsubscribe("my/testing/topic")


class MyWsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.groupname = "dashboard"
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.groupname, self.channel_name)

    async def receive(self, text_data):
        print(">>>>", text_data)
        # datapoint = json.loads(text_data)
        # val = datapoint["value"]
        # await self.channel_layer.group_send(
        #     self.groupname, {"type": "deprocessing", "value": val}
        # )

    async def ws_dashboard_data(self, event):
        print("Send channel layer message to websocket \n")
        print("event -> ", event)
        e_value = event["value"]
        await self.send(text_data=json.dumps({"value": e_value}))
