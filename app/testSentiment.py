import sentiment


text = "AS fresh revelations come in waves at Hollywood’s alleged serial sexual harasser Harvey Weinstein, there are reports the New York Police Department and the FBI also have him in their sights."

content = sentiment.SentimentAnalysis.analyise(text=text)

probability = content['probability']
temp = sorted(probability, key=probability.get ,reverse=1)

print(temp[1])
