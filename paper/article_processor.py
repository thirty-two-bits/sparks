



def process_article(article_id):
    article = Article.objects.get(pk=article_id)
    if article.processed:
        return

    # normalize_url

    # Do any aritcles with a raw, or url if so delete this one
