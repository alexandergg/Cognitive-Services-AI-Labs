import logging, shutil
import os, datetime, requests
import azure.functions as func

from .preprocessing.preprocess import CognitiveServices

try:
    from shared_code.storage import storage
    from shared_code.config.setting import Settings

except:
    from __app__.shared_code.storage import storage
    from __app__.shared_code.config.setting import Settings


def main(mytimer: func.TimerRequest):
    settings = Settings()
    cs = CognitiveServices()

    st = storage.BlobStorageService(settings.get_key_value("STORAGE_ACCOUNTNAME"), settings.get_key_value("STORAGE_KEY"))
    utc_timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    try:
        docs = st.download_blobs(settings.get_key_value("STORAGE_DOCUMENTS"))
        list(map(lambda doc: cs.checkDatetime(utc_timestamp, doc.properties.last_modified, doc), docs))
    except Exception as e:
        error = str(e)
        print(error)
    logging.info(f'Process finish succesfully')