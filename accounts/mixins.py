from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class UnAuthenticatedUserMixin(UserPassesTestMixin):
    def handle_no_permission(self):
        return redirect("accounts:user-view")

    def test_func(self):
        return not self.request.user.is_authenticated


class FarmerMixin(UserPassesTestMixin):
    def handle_no_permission(self):
        return redirect("accounts:user-view")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_farmer
