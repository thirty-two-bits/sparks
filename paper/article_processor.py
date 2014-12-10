

def process_articles(article_id):
    article = Article.objects.get(pk=article_id)
    if article.processed:
        return

    # Do any aritcles with a raw, or url if so delete this one
