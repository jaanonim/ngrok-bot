import subprocess
import time

import requests


class Ngrok:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def init(self, port):
        self.port = port
        self.start()

    def start(self):
        subprocess.Popen(["ngrok", "tcp", "-region=eu", self.port])
        time.sleep(3)
        print(self.getAddres())
        print("ngrok is running")

    def getAddres(self):
        return (
            requests.get("http://127.0.0.1:4040/api/tunnels")
            .json()["tunnels"][0]["public_url"]
            .split("//")[1]
        )
