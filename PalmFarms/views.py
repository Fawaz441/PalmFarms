from django.views.generic import TemplateView
from accounts.mixins import UnAuthenticatedUserMixin


class LandingPage(UnAuthenticatedUserMixin, TemplateView):
    template_name = "landing-page.html"
