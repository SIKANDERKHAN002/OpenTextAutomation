import os
import configparser


base_dir = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))

config_path = os.path.join(base_dir,"configurations","config.ini")

config = configparser.ConfigParser()
config.read(config_path)

class ReadConfig:
    @staticmethod
    def get(key):
        return  config["commonInfo"][key]
