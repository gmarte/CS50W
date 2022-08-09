from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),    
    path("login", views.login_view, name="login"),    
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("auction/<int:auction_id>/", views.auction_view, name="view"),
    path("comment/<int:auction_id>/", views.comment_post, name="comment"),    
    path("watchlist/<int:auction_id>/", views.watchlist_add, name="watchlist")
]
