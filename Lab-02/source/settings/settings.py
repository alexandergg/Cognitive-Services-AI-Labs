import json
import os

from singleton_decorator import singleton

@singleton
class Settings:
    def __init__(self):
        self.__config = self.__load_configuration('./settings/settings.json')
    
    def __load_configuration(self, path):    
        if os.path.exists(path):
            with open(path) as file:
                return json.load(file)
        return dict()

    def get_subscription_training_key(self):
        return os.environ.get("SUBSCRIPTION_TRAINING_KEY", self.__from_config("SUBSCRIPTION_TRAINING_KEY"))
    
    def get_subscription_prediction_key(self):
        return os.environ.get("SUBSCRIPTION_PREDICTION_KEY", self.__from_config("SUBSCRIPTION_PREDICTION_KEY"))

    def get_prediction_resource_id(self):
        return os.environ.get("PREDICTION_RESOURCE_ID", self.__from_config("PREDICTION_RESOURCE_ID"))

    def get_endpoint(self):
        return os.environ.get("ENDPOINT", self.__from_config("ENDPOINT"))
    
    def get_project_name(self):
        return os.environ.get("PROJECT_NAME", self.__from_config("PROJECT_NAME"))

    def __from_config(self, key):
        return self.__config[key]