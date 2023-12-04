from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from ..serializers import CarouselSerializer, CarouselListSerializer
from ..forms import CarouselForm
from ..models import Carousel


@api_view(['POST'])
def carousel_create(request):
    serializer = CarouselSerializer(data=request.data)
    if serializer.is_valid():
        images = serializer.validated_data.get('image')
        print('images = ', images)

        carousel_objs = [Carousel(image=image) for image in images]

        Carousel.objects.all().delete()
        Carousel.objects.bulk_create(carousel_objs)

        return Response({'status': True, 'message': 'Carousel created successfully.'},
                        status=status.HTTP_201_CREATED)
    else:
        return Response({'status': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def carousel_list(request):
    carousel = Carousel.objects.all()
    return Response({'status': True, 'data': [c.image.url for c in carousel]}, status=status.HTTP_200_OK)

