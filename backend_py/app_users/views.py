# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class UserListView(APIView):
    def get(self, request):
        print("GET request received")
        users = User.objects.all().values()
        user_list = list(users)
        data = {
            'status': 'ok',
            'msg': 'Getting Users',
            'users': user_list,
        }
        return JsonResponse(data, safe=False)

class UserCreateView(APIView):
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')

        try:
            if name and email and password and username:
                hashed_password = make_password(password)
                user = User.objects.create(name=name, email=email, password=hashed_password, username=username)
                user_serialized = {
                    'name': user.name,
                    'email': user.email,
                    'username': user.username
                }
                return Response({'status': 'ok', 'msg': 'User created successfully', 'user': user_serialized}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'error', 'msg': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'error', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = self.get_user_by_email(email)


        if user is not None:
            password_hashed = user.password

            is_valid = self.compare_password(password_hashed, password)
            if is_valid:
                Token.objects.get_or_create(user=user)

                return Response({
                    'status': 'ok',
                    'token': 'token',
                    'msg': 'User logged In successfully'
                    }, status=status.HTTP_200_OK)

            else:
                return Response({'status': 'Error', 'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'ststus':'error','msg': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_user_by_email(email):
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def compare_password(password_hashed, password):
        return check_password(password, password_hashed)

        