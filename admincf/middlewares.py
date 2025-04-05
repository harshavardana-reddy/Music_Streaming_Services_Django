from django.contrib.messages import get_messages

class ClearMessagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        response = self.get_response(request)

        # Clear messages after the response is processed
        storage = get_messages(request)
        for message in storage:
            pass  # Messages are now consumed and cleared

        return response