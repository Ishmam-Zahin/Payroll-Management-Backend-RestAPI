from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Logout_View(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK, data={"message": 'loged out!'})