"""libsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^admin/',views.admin,name="admin"),
    url(r'^user/', views.logIn),
    url(r'^postsign/', views.postsign),
    url(r'^postsign2/', views.borrow,name="borrow"),
    url(r'^adminpage/',views.adminpage,name="adminpage"),
    url(r'^librarianpage/',views.librarianpage,name="librarianpage"),
    url(r'^user/', views.logout,name="log"),
    url(r'^signup/', views.signup,name="signup"),
    url(r'^postsignup/', views.postsignup),
    url(r'^books/',views.books,name="books"),
    url(r'^book_detail/',views.book_detail,name="book_detail"),
    url(r'^log/',views.log,name="login"),
    url(r'^profile/',views.profile,name="profile"),
    url(r'^librarian/',views.librarian,name="librarian"),
    url(r'^$',views.home,name="home"),
    url(r'^book_sign/',views.book_sign,name="book_sign"),
    url(r'^addbook/',views.addbook,name="addbook"),
    url(r'^newbook/',views.newbook,name="newbook"),
    url(r'^reqs/',views.reqs,name="reqs"),
    url(r'^detailed_requests/',views.book_req,name="book_req"),
    url(r'^rqst/',views.accept,name="accept"),
    url(r'^rqst/',views.reject,name="reject"),
    url(r'^profile1/',views.book1,name="book1"),
    url(r'^profile2/',views.book2,name="book2"),
    url(r'^librarians/',views.librarians,name="librarians"),
    url(r'^users/',views.users,name="users"),
    url(r'^user_profile/',views.user_profile,name="user_profile"),
    url(r'^librarian_profile/',views.librarian_profile,name="librarian_profile"),
    url(r'^astatus/',views.astatus,name="astatus"),
    url(r'^istatus/',views.istatus,name="istatus"),
    url(r'role1-yes',views.rol1Y,name="rol1Y"),
    url(r'role1-no',views.rol1N,name="rol1N"),
    url(r'role2-yes',views.rol2Y,name="rol2Y"),
    url(r'role2-no',views.rol2N,name="rol2N"),
    url(r'role3-yes',views.rol3Y,name="rol3Y"),
    url(r'role3-no',views.rol3N,name="rol3N"),
    url(r'^newlib',views.newlib,name="newlib"),
    url(r'^new_librarian',views.new_librarian,name="new_librarian"),
]
