
from django.contrib import admin
from django.urls import path, include, re_path
from vimacon import views as vimaconviews
from rest_framework.routers import DefaultRouter

from webapp.views import PieceViewSet, ProductViewSet, BudgetViewSet

router = DefaultRouter()
router.register(r'pieces', PieceViewSet)
router.register(r'products', ProductViewSet)
router.register(r'budgets', BudgetViewSet)
    


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vimacon/new-message/', vimaconviews.MessageCreateAPIView.as_view(), name='new-message'),
    path('api/vimacon/', include('vimacon.urls'), name="inbox"),
    re_path('api/vimacon/login', vimaconviews.login),
    re_path('api/vimacon/logout', vimaconviews.LogoutView.as_view()),
    path('api/', include(router.urls)),
    path('api/products/sizes/', ProductViewSet.as_view({'get': 'sizes'}), name='product-sizes'),
    path('api/products/colors/', ProductViewSet.as_view({'get': 'colors'}), name='product-colors'),
    path('api/budgets/calculate_budget/', BudgetViewSet.as_view({'post': 'calculate_budget'}), name='calculate-budget'),
]
