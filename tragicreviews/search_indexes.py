from haystack import indexes
from tragicreviews.models import Article, UserProfile

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    autocomplete = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Article

class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='user')
    autocomplete = indexes.EdgeNgramField(model_attr='user')

    def get_model(self):
        return UserProfile
