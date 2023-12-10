from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import VideoCreateSerializer, VideoListSerializer
from ..models import Video
from users.utils import add_success_response, add_error_response, format_errors, get_paginated_list
from users.custom_views import CustomAuthenticateView


# @method_decorator(csrf_exempt, name='dispatch')
class VideoCreateView(CustomAuthenticateView):
    permission_classes = []
    authentication_classes = ()

    def get_response(self, request, user):
        # user = request.user
        print('Logged In User --- ', user)
        video_id = request.data.get('id')
        if video_id:
            video = get_object_or_404(Video, id=video_id)
            serializer = VideoCreateSerializer(video, data=request.data)
        else:
            serializer = VideoCreateSerializer(data=request.data)

        if serializer.is_valid():
            obj = serializer.save(view_on_app=True, created_by=user)

            # Set duration
            from moviepy.video.io.VideoFileClip import VideoFileClip
            from django.conf import settings
            import os
            file_path = os.path.join(settings.MEDIA_ROOT, obj.file.name)
            clip = VideoFileClip(file_path)
            d = clip.duration
            print('duration  = ', d)
            clip.close()

            obj.duration = d
            obj.save()

            return add_success_response({
                'message': 'Video created successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return add_error_response({
                'error': format_errors(serializer.errors)
            })


class VideoListView(CustomAuthenticateView):
    permission_classes = []
    authentication_classes = ()

    def get_response(self, request, user):
        # if not request.user.is_authenticated:
        #     return Response({'status': False, 'logged_in': False})

        page = request.POST.get('page', 1)
        per_page = request.POST.get('per_page', 10)

        video_id = request.data.get('id')
        if not video_id:
            videos = Video.objects.all()
            data = get_paginated_list(videos, page, per_page)
            serializer = VideoListSerializer(data['data'], many=True)
            # return Response({'status': True, 'data': serializer.data})
            data['data'] = serializer.data
            print('data ---- ', data)
            return add_success_response(data)
            # return Response(data)

            # if not request.user.is_authenticated:
            #     return Response({'status': False, 'logged_in': False})
        else:
            video = get_object_or_404(Video, id=video_id)
            serializer = VideoListSerializer(video)
            return add_success_response({'data': serializer.data})


class VideoDeleteView(CustomAuthenticateView):
    def post(self, request):
        video_id = request.data.get('id')
        video = get_object_or_404(Video, id=video_id)
        video.delete()
        return add_success_response({'message': 'Video deleted.'})
