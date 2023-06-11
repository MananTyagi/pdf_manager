from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("upload", views.upload_pdf_file, name="upload"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("invite_form", views.invite_form, name="invite_form"),
    path("comment_adder", views.comment_adder, name="comment_adder"),
    path("search_pdf", views.search_pdf, name="search_pdf"),
    path("view_invited_pdf/<str:encoded>", views.view_invited_pdf, name="view_invited_pdf"),
    path("pdf_file/<str:id>/", views.pdf_file_viewer, name="pdf_file")
    
]