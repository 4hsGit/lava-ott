from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..serializers import VideoCreateSerializer, VideoListSerializer
from ..models import Video
from users.utils import format_errors


class VideoCreateView(APIView):
    def post(self, request, *args, **kwargs):
        video_id = request.data.get('id')
        if video_id:
            video = get_object_or_404(Video, id=video_id)
            serializer = VideoCreateSerializer(video, data=request.data)
        else:
            serializer = VideoCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': True,
                'message': 'Video created successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': False,
                'error': format_errors(serializer.errors)
            })


class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoListSerializer(videos, many=True)
        return Response({'status': True, 'data': serializer.data})

    def post(self, request):
        video_id = request.data.get('id')
        video = get_object_or_404(Video, id=video_id)
        serializer = VideoListSerializer(video)
        return Response({'status': True, 'data': serializer.data})


class VideoDeleteView(APIView):
    def post(self, request):
        video_id = request.data.get('id')
        video = get_object_or_404(Video, id=video_id)
        video.delete()
        return Response({'status': True, 'message': 'Video deleted.'})
