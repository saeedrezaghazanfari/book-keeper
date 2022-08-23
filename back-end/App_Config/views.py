from django.http import HttpResponse
from django.utils.translation import activate
from django.shortcuts import redirect


# url: /change/language/
def activate_language(request):
    lang = request.GET.get('lang')
    next_url = request.GET.get('url')
    activate(lang)
    return redirect(f'/{lang}/{next_url}')


def select_lang_redirect(request):
    return redirect('/fa')


# url: /admin
def admin_fake_page(request):
    return HttpResponse('''
        <body style="padding: 0; margin: 0;">
        <img src="http://127.0.0.1:8000/site_static/img/fingers.png" style="width: 100%; height: 100%" />
        </body>
    ''')