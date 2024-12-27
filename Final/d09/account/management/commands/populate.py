from django.core.management.base import BaseCommand
import django.contrib.auth

class Command(BaseCommand):

    def handle(self, *args, **options):
        users_data = [
            {'username': 'user1', 'password': 'pass1'},
            {'username': 'user2', 'password': 'pass2'},
            {'username': 'user3', 'password': 'pass3'}
        ]

        try:
            User = django.contrib.auth.get_user_model()
            for user_data in users_data:
                if not User.objects.filter(username=user_data['username']):
                    User.objects.create_user(username=user_data['username'], password=user_data['password'])
            self.stdout.write(self.style.SUCCESS("Users created successfully."))
        except Exception as e:
            self.stdout.write(self.style.WARNING('An error occurred while populating users.', e))
