from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import SubscriptionPlanSerializer
from ..models import SubscriptionPlan


@api_view(['POST'])
def subscription_plan_create(request):
    serializer = SubscriptionPlanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': True, 'message': 'Subscription plan created'},
                        status=status.HTTP_201_CREATED)
    else:
        return Response({'status': False, 'message': serializer.errors})


@api_view(['GET'])
def subscription_plan_list(request):
    sub_plans = SubscriptionPlan.objects.all()
    serializer = SubscriptionPlanSerializer(sub_plans, many=True)
    return Response({'status': True, 'data': serializer.data},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def subscription_plan_delete(request):
    sub_plan_id = request.data.get('id')
    try:
        sub_plan = SubscriptionPlan.objects.get(pk=sub_plan_id)
        sub_plan.delete()
        return Response({'status': True, 'message': 'Subscription plan deleted.'}, status=status.HTTP_200_OK)
    except SubscriptionPlan.DoesNotExist:
        return Response({'status': False, 'message': 'ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)
