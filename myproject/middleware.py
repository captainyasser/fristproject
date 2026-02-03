from django.shortcuts import render

class SystemProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        # Catch exceptions with the specific message "System expired"
        if str(exception) == "System expired":
            return render(request, 'system_expired.html', status=403)
        return None
