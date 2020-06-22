
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from posts.views import index, post_list,search,PostDetailView,Posts_in_CategoryView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('blog/',post_list),
     path('search/',search,name='search'),
    # path('post/',post),
    path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/<id>/',post, name='post-detail'),
    path("category/<int:id>/posts", Posts_in_CategoryView, name="posts_in_category"),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    #3rd party
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)