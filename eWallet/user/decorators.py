from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            if not (request.user.groups.name == 'AppAdmin'):
                messages.error(request,'you are not authorized to perform this action.')
                return redirect('homepage')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

