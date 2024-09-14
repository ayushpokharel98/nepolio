from django.urls import path, include
from . import views
from . import tools
urlpatterns = [
    path('', views.index),
    path('login', views.login_view, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_view, name="logout"),
    path('stock/<str:stock_name>', views.stocks, name="stock"),
    path('get-stock-names', tools.return_js_names, name="get-stock-names"),
    path('get-index-data', tools.get_index_data, name="get-index-data"),
    path('delete-stock/<str:stock_name>', views.deleteStock, name="delete-stock"),
    path('get-stocks-data', tools.get_stock_data, name="get-stock-data"),
    path('all-data', tools.get_all_stock_data, name="all_data"),
]