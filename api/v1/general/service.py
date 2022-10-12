from api.v1.company.models.models import Company
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from api.v1.accounts.models import User

def create_data(data):
    if data.is_valid():
        data.save()
        return {
            'success': True,
            'error':[],
            'data': data.data
        }
    return {
        'success': False,
        'error':make_errors(data.errors),
        'data': []
    }
    
    
def get_data(data):
    return {
        'success': True,
        'error':[],
        'data': data.data
    }
    


def update_data(data):
    if data.is_valid():
        data.save()
        return {
            'success': True,
            'error':[],
            'data': data.data
        }
    return {
        'success': False,
        'error':make_errors(data.errors),
        'data': []
    }
    
def delete_data(item):
    try:
        item.is_active = False
        item.is_deleted = True
        item.save()
    except Exception as e:
        return {
            'success': False,
            'error':str(e),
            'data': []
        }
    return {
            'success': True,
            'error':[],
            'message': "Successfuly deleted.",
            'data': []
        }


def not_found_error(pk):
    return {
        'success': False,
        'error': f'Not found! ID {pk}',
        'data': []
    }

def get_object(items, pk):
    try:
        item = items.filter(is_active=True, is_deleted=False, id=pk).first()
    except:
        return None
    return item


def make_errors(errors):
    return [
        {
            "key": i,
            "error": errors[i][0],
        }
        for i in errors]





# def get_user(request):
#     try:
#         token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
#         valid_data = AccessToken(token)
#     except:
#         return None

#     return valid_data['user_id']


# paginator = LimitOffsetPagination()
#         result_page = paginator.paginate_queryset(products, request)
#         serializer = ProductGetSerializer(result_page, many=True)
#         paginator_response = paginator.get_paginated_response(result_page).data
#         return Response(
#             {
#                 "count": paginator_response["count"],
#                 "next": paginator_response["next"],
#                 "previous": paginator_response["previous"],
#                 "products": serializer.data,
#             },
#             status=status.HTTP_200_OK,
#         )

