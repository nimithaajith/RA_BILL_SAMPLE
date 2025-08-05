from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from functools import wraps

# Custom decorator to check if user is authenticated and is project 
def project_required(view_func):
    @wraps(view_func)
    @login_required  
    def _wrapped_view(request, *args, **kwargs):        
        if request.user.is_authenticated and request.user.user_type == 'project':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")    
    return _wrapped_view
