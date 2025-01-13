from rest_framework.views import APIView
from rest_framework.response import Response

class HelloAPIView(APIView):
    def get(self, request, *args, **kwargs):
        base_url = request.build_absolute_uri('/')[:-1].strip("/")
        routes = [
            f'{base_url}/api/schema/swagger-ui/'
        ]
        return Response(routes)