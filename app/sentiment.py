import requests
import json


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
