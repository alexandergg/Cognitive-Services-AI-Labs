import logging, requests, json, os
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO
from matplotlib.patches import Rectangle
from ...shared_code.storage.storage import BlobStorageService
from ...shared_code.config.setting import Settings

class CognitiveServices():
    def __init__(self):
        self._settings = Settings()
        self._storage = BlobStorageService(self._settings.get_storage_account(), self._settings.get_storage_key())
        self._subscription_key = self._settings.get_cognitive_key()
        self._vision_base_url = self._settings.get_computer_vision_url()
        self._text_analytics_url = self._settings.get_text_analytics_url()

    def checkDatetime(self, utc_now, last_modified, doc):
        blob_date = last_modified.strftime('%Y-%m-%d')
        enrichdata = {}
        if utc_now == blob_date:
            blob_url = self._storage.make_blob_url(self._settings.get_storage_documents(), doc.name)
            vision = self.computer_vision_api(blob_url)
            text, word_infos = self.ocr(blob_url, doc.name)
            text_clean = ' '.join(text)
            language = self.detectLanguage(text_clean)
            document, sentiments = self.detectSentiment(language, text_clean)
            keyphrases = self.getKeyphrases(document)

            enrichdata["Vision"] = vision
            enrichdata["OCR"] = word_infos
            enrichdata["OCRText"] = text_clean
            enrichdata["Language"] = {"language":language}
            enrichdata["Sentiment"] = sentiments
            enrichdata["Keyphrases"] = keyphrases
            
            logging.info(f'{json.dumps(enrichdata, indent=4, sort_keys=True)}')
            enrichdata = json.dumps(enrichdata).encode('utf-8')
            filename, _ = os.path.splitext(doc.name)
            self._storage.upload_file_from_bytes(container_name=self._settings.get_storage_enrichment(), filename=filename+'.json', blob=enrichdata)
        else:
            return "False"
    
    def computer_vision_api(self, blob_url):
        vision_analyze_url = self._vision_base_url + "analyze"
        headers  = {'Ocp-Apim-Subscription-Key': self._subscription_key }
        params   = {'visualFeatures': 'Faces,Tags,Categories,Description,Color'}
        data     = {'url': blob_url}
        response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
        response.raise_for_status()
        analysis = response.json()
        return analysis
    
    def ocr(self, blob_url, filename):
        ocr_url = self._vision_base_url + "ocr"
        headers  = {'Ocp-Apim-Subscription-Key': self._subscription_key}
        params   = {'language': 'unk', 'detectOrientation ': 'true'}
        data     = {'url': blob_url}
        response = requests.post(ocr_url, headers=headers, params=params, json=data)
        response.raise_for_status()
        analysis = response.json()
        line_infos = [region["lines"] for region in analysis["regions"]]
        word_infos = self.extractWordsBoudings(line_infos)
        self.showResultOnImage(word_infos, blob_url, filename)

        text = self.extractTextFromOCR(line_infos)
        return text, word_infos
    
    def extractWordsBoudings(self, line_infos):
        word_infos = []
        for line in line_infos:
            for word_metadata in line:
                for word_info in word_metadata["words"]:
                    word_infos.append(word_info)
        return word_infos
    
    def extractTextFromOCR(self, line_infos):
        text = []
        for line in line_infos:
            for word_metadata in line:
                for i in range(len(word_metadata["words"])):
                    text.append(word_metadata["words"][i]['text'])
        return text
    
    def showResultOnImage(self, word_infos, blob_url, filename):
        name = os.path.basename(filename)
        plt.figure(figsize=(50,50))
        b = self._storage.download_blob_bytes(self._settings.get_storage_documents(), filename)
        image = Image.open(BytesIO(b.content))
        ax = plt.imshow(image, alpha=0.5)
        for word in word_infos:
            bbox = [int(num) for num in word["boundingBox"].split(",")]
            text = word["text"]
            origin = (bbox[0], bbox[1])
            patch  = Rectangle(origin, bbox[2], bbox[3], fill=False, linewidth=2, color='y')
            ax.axes.add_patch(patch)
            plt.text(origin[0], origin[1], text, fontsize=20, weight="bold", va="top")
        _ = plt.axis("off")
        plt.savefig('{}'.format(name))
        self._storage.upload_file(container_name=self._settings.get_storage_ocr(),
                                filename=name,
                                local_file='./{}'.format(name),
                                delete_local_file=True)
    
    def truncateCharacters(self, text):
        _, text = os.path.split(text)
        text = (text[:5100] + '..') if len(text) > 5100 else text
        return text
                            
    def detectLanguage(self, text):
        language_api_url = self._text_analytics_url + "languages"
        text = self.truncateCharacters(text)
        document = { 'documents': [
            { 'id': '1', 'text': text }
        ]}
        headers   = {"Ocp-Apim-Subscription-Key": self._subscription_key}
        response  = requests.post(language_api_url, headers=headers, json=document)
        languages = response.json()
        language = languages['documents'][0]['detectedLanguages'][0]["iso6391Name"]
        return language

    def detectSentiment(self, language, text):
        sentiment_api_url = self._text_analytics_url + "sentiment"
        document = {'documents' : [{'id': '1', 'language': language, 'text': text}]}
        headers   = {"Ocp-Apim-Subscription-Key": self._subscription_key}
        response  = requests.post(sentiment_api_url, headers=headers, json=document)
        sentiments = response.json()
        return document, sentiments
    
    def getKeyphrases(self, document):
        key_phrase_api_url =  self._text_analytics_url + "keyPhrases"
        headers   = {"Ocp-Apim-Subscription-Key": self._subscription_key}
        response  = requests.post(key_phrase_api_url, headers=headers, json=document)
        key_phrases = response.json()
        return key_phrases