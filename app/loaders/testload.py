#import techcrunch
#import cricketau
import venturebeat

#article = techcrunch.ArticleLoader.load(
#    'https://techcrunch.com/2017/09/30/where-human-intelligence-outperforms-ai')

#article2 = cricketau.ArticleLoader.load(
#'http://www.cricket.com.au/news/brad-hogg-kfc-big-bash-league-bbl07-targets-50-year-melbourne-renegades-scorchers/2017-10-03')
#print(article['content'])
#print(article2['title'],article2['date'])

article3 = venturebeat.ArticleLoader.load(
'https://venturebeat.com/2017/10/07/how-trivia-crack-put-argentina-on-the-worlds-game-industry-map/')

print(article3['date'])
