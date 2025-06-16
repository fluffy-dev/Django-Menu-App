from django.shortcuts import render


def index_view(request):
    """Renders the main page."""
    return render(request, 'menu/page.html', {'title': 'Главная страница'})


def about_view(request):
    """Renders the 'About Us' page."""
    return render(request, 'menu/page.html', {'title': 'О нас'})


def services_view(request):
    """Renders the main services page."""
    return render(request, 'menu/page.html', {'title': 'Наши услуги'})

def terms_of_service_page_view(request):
    return render(request, 'menu/page.html', {'title': 'Условия пользования'})

def service_detail_view(request, service_slug: str):
    """
    Renders a specific service detail page.

    Args:
        request: The HTTP request object.
        service_slug: The slug identifying the specific service.
    """
    title = f'Услуга: {service_slug.replace("-", " ").capitalize()}'
    return render(request, 'menu/page.html', {'title': title})