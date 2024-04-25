from django.urls import reverse
from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render
from authors.models import Profile
from django.contrib.auth.decorators import login_required
from authors.forms import ProfileForm
from django.contrib import messages
from django.utils.decorators import method_decorator


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
    def get_profile(self, id=None):
        profile = Profile.objects.filter(
            pk=id
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
        profile = self.get_profile(id)

        form = ProfileForm(instance=profile)

        return self.render_profile(form)

    def post(self, request, id=None):
        profile = self.get_profile(id)

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

            profile.save()
            messages.success(request, 'Profile created/edited successfully!')
            return redirect(reverse('authors:profile_edit', args=(
                        profile.id,
                )
              )
            ) # noqa E501

        return self.render_profile(form)
