from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
