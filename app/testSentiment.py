import sentiment
# from loaders import techcrunch

text = "AS fresh revelations come in waves at Hollywood’s alleged serial sexual harasser Harvey Weinstein, there are reports the New York Police Department and the FBI also have him in their sights."
# text = techcrunch.ArticleLoader.load('https://techcrunch.com/2017/07/09/trump-discussed-forming-impenetrable-cyber-security-unit-with-russia/')

content = sentiment.SentimentAnalysis.analyise(text=text)

probability = content['probability']
print(probability)
temp = sorted(probability, key=probability.get ,reverse=1)
print(temp)
