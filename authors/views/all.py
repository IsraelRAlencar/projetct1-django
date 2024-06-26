from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from authors.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe


def register_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('authors:dashboard'))

    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse("authors:register_create")
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'User created successfully!')

        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Login successful!')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials!')
    else:
        messages.error(request, 'Invalid username or password!')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if request.POST:
        if request.POST.get('username') != request.user.username:
            messages.error(request, 'Invalid logout user!')
            return redirect(reverse('authors:login'))
    else:
        if not request.META.get('HTTP_REFERER'):
            messages.error(request, 'Invalid logout request!')
            return redirect(reverse('authors:login'))

        if request.META['HTTP_REFERER'] != request.build_absolute_uri(reverse('authors:profile_edit', args=(request.user.pk,))): # noqa E501
            messages.error(request, 'Invalid logout request!')
            return redirect(reverse('authors:login'))

    messages.success(request, 'Logout successful!')
    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        author=request.user,
        is_published=False
    ).order_by('-id')

    return render(
        request,
        'authors/pages/dashboard.html',
        context={'recipes': recipes}
    )
