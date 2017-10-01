import techcrunch


article = techcrunch.ArticleLoader.load(
    'https://techcrunch.com/2017/09/30/where-human-intelligence-outperforms-ai')


print(article['content'])
