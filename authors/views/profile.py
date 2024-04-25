from django.urls import reverse
from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render
from authors.models import Profile
from django.contrib.auth.decorators import login_required
from authors.forms import ProfileForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


class ProfileView(TemplateView):
    template_name = 'authors/pages/profile.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        profile_id = context.get('id')
        profile = Profile.objects.filter(
            pk=profile_id
        ).select_related('author').first()

        if not profile:
            return redirect(reverse('authors:profile_create'))

        return self.render_to_response({
            **context,
            'profile': profile
        })


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class ProfileChangeView(View):
    def get_profile(self):
        profile = Profile.objects.filter(
            pk=self.request.user.pk
        ).first()

        if not profile:
            profile = None

        return profile

    def render_profile(self, form):
        return render(
            self.request,
            'authors/pages/profile_create.html',
            context={
                'form': form,
            }
        )

    def get(self, request, id=None):
        profile = self.get_profile()

        form = ProfileForm(
            instance=profile,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'username': request.user.username,
                'email': request.user.email
            }
        )

        return self.render_profile(form)

    def post(self, request, id=None):
        profile = self.get_profile()

        form = ProfileForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=profile
        )

        if form.is_valid():
            profile = form.save(commit=False)

            profile.author = request.user
            profile.pk = request.user.pk
            if request.FILES.get('profile_cover'):
                profile.profile_cover = request.FILES.get('profile_cover')

            alt_username_password = alter_user_settings(self, form.cleaned_data) # noqa E501

            profile.save()
            messages.success(request, 'Profile created/updated successfully!')

            if alt_username_password:
                return redirect(reverse('authors:logout'))
            else:
                return redirect(reverse('authors:profile_edit', args=(
                            profile.id,
                        )
                    )
                )

        return self.render_profile(form)


def alter_user_settings(self, dict):
    user = User.objects.get(pk=self.request.user.pk)
    altered_username_password = False

    if dict.get('first_name') != user.first_name:
        user.first_name = dict.get('first_name')

    if dict.get('last_name') != user.last_name:
        user.last_name = dict.get('last_name')

    if dict.get('username') != user.username:
        user.username = dict.get('username')
        altered_username_password = True

    if dict.get('email') != user.email:
        user.email = dict.get('email')

    if dict.get('password'):
        user.set_password(dict.get('password'))
        altered_username_password = True

    user.save()
    return altered_username_password
