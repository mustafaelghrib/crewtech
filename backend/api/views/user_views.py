from rest_framework import views, status, response


class UsersAPI(views.APIView):

    def post(self, request):
        return self.user_register(request)

    def get(self, request):
        return self.get_users()

    @staticmethod
    def user_register(request):
        return response.Response({
            "status": status.HTTP_200_OK,
            "message": "User registered successfully",
        })

    @staticmethod
    def get_users():
        return response.Response({
            "status": status.HTTP_200_OK,
            "message": "Users fetched successfully",
        })


class UserAPI(views.APIView):

    def get(self, request, user_id):
        return self.get_user(request, user_id)

    def patch(self, request, user_id):
        return self.update_user(request, user_id)

    def put(self, request, user_id):
        return self.update_user(request, user_id)

    def delete(self, request, user_id):
        return self.delete_user(request, user_id)

    @staticmethod
    def get_user(request, user_id):
        return response.Response({
            "status": status.HTTP_200_OK,
            "message": f"User {user_id} fetched successfully",
        })

    @staticmethod
    def update_user(request, user_id):
        return response.Response({
            "status": status.HTTP_200_OK,
            "message": f"User {user_id} updated successfully",
        })

    @staticmethod
    def delete_user(request, user_id):
        return response.Response({
            "status": status.HTTP_200_OK,
            "message": f"User {user_id} deleted successfully",
        })
