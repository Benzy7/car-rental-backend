from rest_framework.response import Response

class ApiResponseFormatterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if isinstance(response, Response):
            data = response.data
            data['success'] = True if response.status_code == 200 else False
            response.data = data

        return response
