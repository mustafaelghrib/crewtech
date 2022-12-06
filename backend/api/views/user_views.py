from rest_framework import views, status, response

from ..models.user_model import User
from ..serializers.user_serializers import UserSerializer


class UsersAPI(views.APIView):

    def post(self, request, action):
        if action == "register":
            return self.user_register(request)
        elif action == "login":
            return self.user_login(request)
        else:
            return response.Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Action should be register or login",
            })

    def get(self, request, user_id):
        if user_id:
            return self.get_user(user_id)
        else:
            return self.get_users_list()

    def patch(self, request, user_id):
        return self.update_user(request, user_id)

    def put(self, request, user_id):
        return self.update_user(request, user_id)

    def delete(self, request, user_id):
        return self.delete_user(user_id)

    @staticmethod
    def user_register(request):
        return response.Response({
            "status": status.HTTP_200_OK,
            "message": "User registered successfully!",
        })

    @staticmethod
    def user_login(request):
        return response.Response({
            "status": status.HTTP_200_OK,
            "message": "User logged successfully!",
        })

    @staticmethod
    def get_user(user_id):

        try:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return response.Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "User is not found!"
                })
        except Exception as e:
            return response.Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": f"Invalid userId! | {e}"
            })

        return response.Response({
            "status": status.HTTP_200_OK,
            "message": f"User fetched successfully!",
            "crews": UserSerializer(user).data
        })

    @staticmethod
    def get_users_list():

        users = User.objects.all()

        return response.Response({
            "status": status.HTTP_200_OK,
            "message": f"A list of users fetched successfully!",
            "users": UserSerializer(users, many=True).data
        })

    @staticmethod
    def update_user(request, user_id):

        try:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return response.Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "User is not found!"
                })
        except Exception as e:
            return response.Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": f"Invalid userId! | {e}"
            })

        payload = request.data

        user.name = payload["name"]
        user.image = payload["image"]
        user.save()

        return response.Response({
            "status": status.HTTP_200_OK,
            "message": "User updated successfully!",
            "user": UserSerializer(user).data
        })

    @staticmethod
    def delete_user(user_id):

        try:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return response.Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "User is not found!"
                })
        except Exception as e:
            return response.Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": f"Invalid userId! | {e}"
            })

        user.delete()

        return response.Response({
            "status": status.HTTP_200_OK,
            "message": "User deleted successfully!",
        })
