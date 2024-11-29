from django.shortcuts import redirect
from django.utils.translation import get_language
from django.views import View


class SwitchLanguageView(View):
    def get(self, request, *args, **kwargs):
        current_language = get_language()
        new_language = 'fr' if current_language == 'en' else 'en'
        next_url = request.GET.get('next', request.path)

        if next_url.startswith(f'/{current_language}/'):
            next_url = f'/{new_language}{next_url[3:]}'
        else:
            next_url = f'/{new_language}{next_url}'
        
        return redirect(next_url)
