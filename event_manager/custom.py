from functools import wraps 
from django.shortcuts import redirect
from django.urls import reverse

def require_key(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'key' not in request.session:
            request.session['return_url'] = request.get_full_path()
            return redirect('admin_key')
        return func(request, *args, **kwargs)
    return wrapper 