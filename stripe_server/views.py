from django.shortcuts import redirect


def favicon_view(request):
    return redirect('/static/favicon.ico')
