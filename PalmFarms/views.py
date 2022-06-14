from django.views.generic import TemplateView
from accounts.mixins import UnAuthenticatedUserMixin
from accounts.models import FAQ


class LandingPage(UnAuthenticatedUserMixin, TemplateView):
    template_name = "landing-page.html"


class AboutPage(TemplateView):
    template_name = "about-page.html"


class FAQPage(TemplateView):
    template_name = "faq.html"

    def get_context_data(self):
        context = super().get_context_data()
        context['faqs'] = FAQ.objects.all()
        return context


class ContactUsPage(TemplateView):
    template_name = "contact-us.html"
