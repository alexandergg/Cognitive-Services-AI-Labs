import json
from singleton_decorator import singleton
import os

@singleton
class Settings:
    def __init__(self):
        self.__config = self.__load_configuration('./shared_code/config/settings.json')
    
    def __load_configuration(self, path):    
        if os.path.exists(path):
            with open(path) as file:
                return json.load(file)
        return dict()

    def get_storage_account(self):
        return os.environ.get("STORAGE_ACCOUNTNAME", self.__from_config("STORAGE_ACCOUNTNAME"))

    def get_storage_key(self):
        return os.environ.get("STORAGE_KEY", self.__from_config("STORAGE_KEY"))
    
    def get_storage_documents(self):
        return os.environ.get("STORAGE_DOCUMENTS", self.__from_config("STORAGE_DOCUMENTS"))
    
    def get_storage_ocr(self):
        return os.environ.get("STORAGE_OCR", self.__from_config("STORAGE_OCR"))
    
    def get_storage_enrichment(self):
        return os.environ.get("STORAGE_ENRICHMENT", self.__from_config("STORAGE_ENRICHMENT"))
    
    def get_cognitive_key(self):
        return os.environ.get("COGNITIVE_KEY", self.__from_config("COGNITIVE_KEY"))
    
    def get_computer_vision_url(self):
        return os.environ.get("COMPUTER_VISION_URL", self.__from_config("COMPUTER_VISION_URL"))
    
    def get_text_analytics_url(self):
        return os.environ.get("TEXT_ANALYTICS_URL", self.__from_config("TEXT_ANALYTICS_URL"))

    def __from_config(self, key):
        return self.__config[key]