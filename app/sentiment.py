import requests
import json

# sentiment analysis algorithm is based on an api from http://text-processing.com/
# it takes in text and return an object with a probability distribution between positive neutral and negative sentiment
url = "http://text-processing.com/api/sentiment/"


class SentimentAnalysis(object):
    """REST call to NLP sentiment analysis"""
    @staticmethod
    def analyise(text):
        response = requests.post(url, data={'text':text})
        json_content = response.content
        if (type(json_content) == bytes):
            json_content = json_content.decode('utf-8')
        content = json.loads(json_content)
        if 'neutral' in content['label']:
            probability = content['probability']
            #if neutral analysis it returns the next best guess either pos or neg
            content['label'] = sorted(probability, key=probability.get ,reverse=1)[1]
        return content
