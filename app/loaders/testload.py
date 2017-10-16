# import techcrunch
# import cricketau
# import venturebeat
import hackernoon
# import newsau

#article = techcrunch.ArticleLoader.load(
#    'https://techcrunch.com/2017/09/30/where-human-intelligence-outperforms-ai')

# article2 = cricketau.ArticleLoader.load('http://www.cricket.com.au/news/brad-hogg-kfc-big-bash-league-bbl07-targets-50-year-melbourne-renegades-scorchers/2017-10-03')
# print(article2['date'])
#
#
# article3 = venturebeat.ArticleLoader.load('https://venturebeat.com/2017/10/07/how-trivia-crack-put-argentina-on-the-worlds-game-industry-map/')
# print(article3['date'])
#
#
article4 = hackernoon.ArticleLoader.load('https://hackernoon.com/how-it-feels-to-learn-javascript-in-2016-d3a717dd577f')
print (article4['date'])
#
#
# article5 = newsau.ArticleLoader.load('http://www.news.com.au/entertainment/celebrity-life/celebrities-gone-bad/as-movie-mogul-heads-to-sex-rehab-police-and-fbi-tipped-to-investigate/news-story/3443e313c1e08e90658689d728d01b56')
#
# print(article5['date'])
