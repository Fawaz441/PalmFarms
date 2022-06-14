from django.urls import path, include

urlpatterns = [
    path('products/', include(('ajax.products.urls', 'products'))),
    path('chat/', include(('ajax.chat.urls', 'chat'))),
    path('accounts/', include(('ajax.accounts.urls', 'accounts')))
]
