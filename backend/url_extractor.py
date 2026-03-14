from newspaper import Article


def extract_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()

        text = article.text
        title = article.title

        return title + " " + text

    except Exception as e:
        return None