from django.http import JsonResponse
from accounts.forms import ContactMessageForm, User


def get_user_details(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse(data={'has_data': False})
    return JsonResponse(data={
        'has_data': True,
        'first_name': user.first_name,
        'last_name': user.surname,
        'phone_no': str(user.phone_number)
    })


def submit_contact_message(request):
    form = ContactMessageForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'Submitted Successfully'})
    return JsonResponse({'message': str(form.errors)}, status=400)
