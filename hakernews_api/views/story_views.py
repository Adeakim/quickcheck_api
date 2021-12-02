from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from hacker_news_backend import HackNewsBackend
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from hakernews_api.models import Item
from hakernews_api.pagination import DefaultPagination
from hakernews_api.serializers import ReadStorySerializer, ReadAStorySerializer
from hakernews_api.filter import ItemFilter


class ReadStoryViewset(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ReadStorySerializer
    hacker_news_backend = HackNewsBackend("topstories")
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ItemFilter
    error = "Not allowed"
    lookup_field = "id"
    print(error)

    def save_item_data(self):
        create_item = []
        res = self.hacker_news_backend.get_all_stories()
        try:
            for story in res[0:10]:
                print(story)
                res_story = self.hacker_news_backend.get_a_story(story)
                create_item = Item.objects.get_or_create(
                    author=res_story["by"],
                    descendants=res_story["descendants"],
                    score=res_story["score"],
                    title=res_story["title"],
                    url=res_story["url"],
                    time=res_story["time"],
                    item_id=res_story["id"],
                    type=res_story["type"],
                    created_at=res_story["created"],
                    is_hackernews=True,
                )
                print("create item", create_item)
                create_item.save()
            serializer = ReadStorySerializer(create_item)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(err)

    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            data = self.queryset.get(pk=kwargs.get("pk"))
            serializer = ReadAStorySerializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(
                {"detail": "Item field cannot be blank"},
                status.HTTP_400_BAD_REQUEST,
            )
        except Exception as err:
            return Response(
                {"detail": err},
                status.HTTP_404_NOT_FOUND,
            )


class WriteStoryViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ReadStorySerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = ReadStorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def list(self, request):
        queryset = Item.objects.all()
        serializer = ReadStorySerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            serializer = ReadAStorySerializer(item)
            return Response(serializer.data, status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response(
                {"detail": "Item not found"}, status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            id = self.kwargs.get("pk")
            story = Item.objects.filter(pk=id).values("is_hackernews")[0]
            is_hacker = story["is_hackernews"]
            data = self.queryset.get(pk=kwargs.get("pk"))
            if is_hacker:
                return Response({"errors": "Not allowed"}, status.HTTP_401_UNAUTHORIZED)
            else:
                serializer = ReadAStorySerializer(
                    data, data=request.data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_200_OK)
                return Response(
                    {"detail": "Item field cannot be blank"},
                    status.HTTP_400_BAD_REQUEST,
                )
        except Exception:
            return Response(
                {"detail": "Item not found"},
                status.HTTP_404_NOT_FOUND,
            )

    def destroy(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        story = Item.objects.filter(pk=id).values("is_hackernews")[0]
        is_hacker = story["is_hackernews"]
        if is_hacker:
            return Response({"errors": "not allowed"}, status.HTTP_401_UNAUTHORIZED)
        else:
            item = self.get_object()
            item.delete()
            item.save()
            return Response({"data": "delete success"},  status.HTTP_204_NO_CONTENT)
