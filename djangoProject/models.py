from mongoengine import Document, fields
from djongo import models


class Index(Document):
    URL = fields.StringField()
    Description = fields.StringField()
    Title = fields.StringField()
    words = fields.ListField()

    # def __str__(self):
    #     return f"URL: {self.URL}, Descr: {self.Description}, Title: {self.Title}, words: {self.words}"
