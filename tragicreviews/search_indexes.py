from haystack import indexes
from tragicreviews.models import Article, UserProfile

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Article

class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='user')

    def get_model(self):
        return UserProfile
