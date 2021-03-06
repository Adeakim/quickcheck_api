from django.urls import path, include
from hakernews_api.views.story_views import ReadStoryViewset, WriteStoryViewSet
from hakernews_api.views.comment_views import ReadCommentViewset, WriteCommentViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register("stories", ReadStoryViewset, basename="story")
router.register("comment", ReadCommentViewset, basename="comment")
router.register("addstory", WriteStoryViewSet, basename="addstory")
router.register("addcomment", WriteCommentViewSet, basename="addcomment")

urlpatterns = [
    path("story", ReadStoryViewset.as_view({"get": "list"}), name="story"),
    path("", include(router.urls)),
]
