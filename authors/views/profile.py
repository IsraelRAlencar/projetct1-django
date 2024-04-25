from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from authors.models import Profile
from django.contrib.auth.decorators import login_required
from authors.forms import ProfileForm
from django.contrib import messages


class ProfileView(TemplateView):
    template_name = 'authors/pages/profile.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        profile_id = context.get('id')
        profile = Profile.objects.filter(
            pk=profile_id
        ).select_related('author').first()

        if not profile:
            return redirect(reverse('authors:profile_view'))

        return self.render_to_response({
            **context,
            'profile': profile
        })


@login_required(login_url='authors:login', redirect_field_name='next')
def profile_view(request):
    profile = Profile.objects.filter(author=request.user).first()

    if profile:
        return redirect(reverse('authors:dashboard'))

    profile_form_data = request.session.get('profile_form_data', None)
    form = ProfileForm(profile_form_data)
    return render(request, 'authors/pages/profile_create.html', {
        'form': form,
        'form_action': reverse("authors:profile_create")
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def profile_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['profile_form_data'] = POST
    form = ProfileForm(request.POST)

    if form.is_valid():
        profile = form.save(commit=False)
        profile.author = request.user
        profile.pk = request.user.pk
        profile.profile_cover = request.FILES.get('profile_cover', None)

        profile.save()
        messages.success(request, 'Profile created successfully!')

        del (request.session['profile_form_data'])
        return redirect(reverse('authors:profile', kwargs={'id': request.user.pk})) # noqa E501

    return redirect(reverse('authors:profile_view'))
