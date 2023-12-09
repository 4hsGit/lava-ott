from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..serializers import VideoCreateSerializer, VideoListSerializer
from ..models import Video
from users.utils import add_success_response, add_error_response, format_errors, get_paginated_list


# @method_decorator(csrf_exempt, name='dispatch')
class VideoCreateView(APIView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        user = self.request.user
        print('Logged In User --- ', user)
        video_id = request.data.get('id')
        if video_id:
            video = get_object_or_404(Video, id=video_id)
            serializer = VideoCreateSerializer(video, data=request.data)
        else:
            serializer = VideoCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(view_on_app=True, created_by=user)

            return add_success_response({
                'message': 'Video created successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return add_error_response({
                'error': format_errors(serializer.errors)
            })


class VideoListView(APIView):

    def get(self, request):
        from datetime import datetime
        from django.utils import timezone
        print(datetime.now())
        print(timezone.now().astimezone().replace(tzinfo=None))
        print('-------------------------------- Request Data ---------------------------')
        print(request.COOKIES.get('sessionid'))
        # print(request.SESSION)
        print('-------------------------------- Request Data ---------------------------')
        print(request.user)
        # if not request.user.is_authenticated:
        #     return Response({'status': False, 'logged_in': False})

        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 10)

        videos = Video.objects.all()
        data = get_paginated_list(videos, page, per_page)
        serializer = VideoListSerializer(data['data'], many=True)
        # return Response({'status': True, 'data': serializer.data})
        data['data'] = serializer.data
        print('data ---- ', data)
        return add_success_response(data)
        # return Response(data)

    def post(self, request):
        # if not request.user.is_authenticated:
        #     return Response({'status': False, 'logged_in': False})

        video_id = request.data.get('id')
        video = get_object_or_404(Video, id=video_id)
        serializer = VideoListSerializer(video)
        return add_success_response({'data': serializer.data})


class VideoDeleteView(APIView):
    def post(self, request):
        video_id = request.data.get('id')
        video = get_object_or_404(Video, id=video_id)
        video.delete()
        return add_success_response({'message': 'Video deleted.'})
