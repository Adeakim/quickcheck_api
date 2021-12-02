from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from hacker_news_backend import HackNewsBackend
from rest_framework.response import Response
from rest_framework import status

from hakernews_api.models import Comment
from hakernews_api.serializers import ReadCommentSerializer


class ReadCommentViewset(ReadOnlyModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = ReadCommentSerializer
    hacker_news_backend = HackNewsBackend("topstories")

    def save_item_data(self):
        res = self.hacker_news_backend.get_all_stories()
        try:
            for story in res[0:10]:
                res_story = self.hacker_news_backend.get_a_story(story)
                comments = res_story["kids"]
                for comment in comments:
                    comment_data = self.hacker_news_backend.getcomments(comment)
                    create_comment = Comment.objects.get_or_create(
                        author=comment_data["by"],
                        parent=res_story["title"],
                        text=comment_data["text"],
                        time=comment_data["time"],
                        item_id=comment_data["id"],
                        is_hacker_comment=True
                    )
                    create_comment.save()
                serializer = ReadCommentSerializer(create_comment)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(errors=err)

    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            data = self.queryset.get(pk=kwargs.get("pk"))
            serializer = self.serializer_class(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(
                errors={"detail": "Text field cannot be blank"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as err:
            return Response(
                errors={"detail": err},
                status=status.HTTP_404_NOT_FOUND,
            )


class WriteCommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = ReadCommentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = ReadCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def list(self, request):
        queryset = Comment.objects.all()
        serializer = ReadCommentSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = ReadCommentSerializer(comment)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(
                errors={"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            id = self.kwargs.get("pk")
            story = Comment.objects.filter(pk=id).values("is_hacker_comment")[0]
            is_hacker = story["is_hacker_comment"]
            data = self.queryset.get(pk=kwargs.get("pk"))
            if is_hacker:
                return Response(errors={"errors": "Not allowed"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                serializer = self.serializer_class(
                    data, data=request.data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_200_OK)
                return Response(
                    errors={"detail": "Field cannot be blank"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception:
            return Response(
                {"detail": "Comment not found"},
                status.HTTP_404_NOT_FOUND,
            )

    def destroy(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        story = Comment.objects.filter(pk=id).values("is_hacker_comment")[0]
        is_hacker = story["is_hacker_comment"]
        if is_hacker:
            return Response(errors={"errors": "not allowed"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            comment = self.get_object()
            comment.delete()
            comment.save()
            return Response(data="delete success",  status=status.HTTP_204_NO_CONTENT)
