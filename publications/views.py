from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Publication
from .forms import PublicationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def publication_list(request):
    query = request.GET.get('q')
    search_field = request.GET.get('search_field', 'title')  # За замовчуванням шукаємо за назвою
    view_type = request.GET.get('view', 'list')  # За замовчуванням список рядками
    per_page = request.GET.get('per_page', 5)  # Кількість елементів на сторінку

    publications = Publication.objects.all().order_by('-created_at')

    if query:
        if search_field == 'title':
            publications = publications.filter(title__icontains=query)
        elif search_field == 'author':
            publications = publications.filter(author__icontains=query)
        elif search_field == 'annotation':
            publications = publications.filter(annotation__icontains=query)
        elif search_field == 'publication_type':
            publications = publications.filter(publication_type__name__icontains=query)
        elif search_field == 'publication_year':
            try:
                publications = publications.filter(publication_year=int(query))
            except ValueError:
                publications = Publication.objects.none()  # Якщо введено нечислове значення
        elif search_field == 'page_count':
            try:
                publications = publications.filter(page_count=int(query))
            except ValueError:
                publications = Publication.objects.none()  # Якщо введено нечислове значення

    # Пагінація
    paginator = Paginator(publications, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'publications/publication_list.html', {
        'page_obj': page_obj,
        'view_type': view_type,
        'query': query,
        'per_page': per_page,
        'search_field': search_field  # Додаємо поле пошуку до контексту
    })


# Перегляд окремої публікації
def publication_detail(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    return render(request, 'publications/publication_detail.html', {'publication': publication})


# Створення нової публікації
@login_required
def publication_create(request):
    if request.method == "POST":
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.created_by = request.user  # Зберігаємо автора публікації (користувача)
            publication.save()
            messages.success(request, 'Публікацію успішно створено!')
            return redirect('publication_list')
    else:
        form = PublicationForm()
    return render(request, 'publications/publication_form.html', {'form': form})


# Редагування публікації
@login_required
def publication_edit(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    # Перевірка, чи є поточний користувач автором публікації
    if publication.created_by != request.user:
        raise PermissionDenied  # Якщо не автор, викидаємо помилку доступу
    # Обробка форми редагування
    if request.method == "POST":
        form = PublicationForm(request.POST, request.FILES, instance=publication)
        if form.is_valid():
            form.save()
            messages.success(request, 'Публікацію успішно оновлено!')
            return redirect('publication_detail', pk=pk)
    else:
        form = PublicationForm(instance=publication)
    return render(request, 'publications/publication_form.html', {'form': form})


# Видалення публікації
@login_required
def publication_delete(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    # Перевірка, чи є поточний користувач автором публікації
    if publication.created_by != request.user:
        raise PermissionDenied  # Якщо не автор, викидаємо помилку доступу
    # Видалення публікації після підтвердження
    if request.method == "POST":
        publication.delete()
        messages.success(request, 'Публікацію успішно видалено!')
        return redirect('publication_list')
    return render(request, 'publications/publication_confirm_delete.html', {'publication': publication})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматично логінемо користувача після реєстрації
            return redirect('publication_list')  # Перенаправлення після успішної реєстрації
    else:
        form = UserCreationForm()
    return render(request, 'publications/register.html', {'form': form})


@login_required
def user_profile(request):
    return render(request, 'publications/profile.html')
