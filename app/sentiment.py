import requests
import json


url = "http://text-processing.com/api/sentiment/"


class SentimentAnalysis(object):
    """REST call to NLP sentiment analysis"""
    @staticmethod
    def analyise(text):
        respone = requests.post(url, data={'text':text})
        content = json.loads(respone.content)
        if 'neutral' in content['label']:
            probability = content['probability']
            #if neutral analysis it returns the next best guess either pos or neg
            content['label'] = sorted(probability, key=probability.get ,reverse=1)[1]
        return content
