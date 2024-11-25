from django.core.management.base import BaseCommand
from app.models import *


class Command(BaseCommand):

    def create_users(self):
        users_data = [
            {"username": "user1", "password": "pass1"},
            {"username": "user2", "password": "pass2"},
            {"username": "user3", "password": "pass3"},
        ]
        users = []
        for user_data in users_data:
            if not User.exists(user_data["username"]):
                user = User.create(**user_data)
            else:
                user = User.fetch(user_data["username"])
            users.append(user)
        return users

    def create_articles(self, users):
        articles_data = [
            {
                "title": "Article1",
                "author": users[0],
                "synopsis": "Synposis article 1",
                "content": "Content article 1",
            },
            {
                "title": "Article2",
                "author": users[1],
                "synopsis": "Synposis article 2",
                "content": "Content article 2",
            },
            {
                "title": "Article3",
                "author": users[2],
                "synopsis": "Synposis article 3",
                "content": "Content article 3",
            },
            {
                "title": "Article4",
                "author": users[0],
                "synopsis": "Synposis article 4",
                "content": "Content article 4",
            },
            {
                "title": "Article5",
                "author": users[1],
                "synopsis": "Synposis article 5",
                "content": "Content article 5",
            },
        ]
        articles = []
        for article_data in articles_data:
            if not Article.exists(article_data["title"]):
                article = Article.create(article_data)
            else:
                article = Article.fetch(article_data["title"])
            articles.append(article)
        return articles

    def handle(self, *args, **options):
        try:
            users = self.create_users()
            articles = self.create_articles(users)
            self.stdout.write(self.style.SUCCESS("Data population complete."))
        except Exception as e:
            self.stdout.write(self.style.ERROR("An error occurred: %s") % e)
