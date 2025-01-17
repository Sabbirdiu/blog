
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from posts.views import index, post_list,search,PostDetailView,Posts_in_CategoryView,About,post_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('blog/',post_list),
    path('about/',About.as_view(),name='about'),
    path('search/',search,name='search'),
    # path('post/',post),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/<slug:slug>/',post_detail, name='post-detail'),
    path("category/<slug:slug>/posts", Posts_in_CategoryView, name="posts_in_category"),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    #3rd party
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)