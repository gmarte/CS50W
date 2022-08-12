from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),    
    path("login", views.login_view, name="login"),    
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("auction/<int:auction_id>/", views.auction_view, name="view"),
    path("auctionc/<int:auction_id>/", views.auction_close, name="close"),
    path("comment/<int:auction_id>/", views.comment_post, name="comment"),    
    path("watchlist/<int:auction_id>/", views.watchlist_add, name="watchlist"),
    path("bid/<int:auction_id>/", views.bid, name="bid"),
    path("watchlist", views.watchlist_view, name="watchlist_view"),
    path("categories", views.categories_view, name="categories"),
    path("categories/<int:category_id>/", views.categories_detail, name="categories_detail"),

]
