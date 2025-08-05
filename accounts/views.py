from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login,authenticate,logout
from .models import User
from django.http import JsonResponse
def LoginView(request):
    if request.method == 'POST':
        user_name=request.POST.get('username')
        pw=request.POST.get('password')
        user=authenticate(request,username=user_name,password=pw)
        if user is not None:
            currentuser=User.objects.get(username=user_name)
            login(request,user)            
            if currentuser.user_type == 'project':
                return redirect('project:Dashboard')
            if currentuser.user_type == 'company':
                return redirect('company:Dashboard')
            if currentuser.user_type == 'consultant':
                return redirect('consultant:Dashboard')
            if currentuser.user_type == 'owner':
                return redirect('owner:Dashboard')
            return render(request,'accounts/loginpage.html',{'msg':'Unknown user type, Please login using valid credentials'})
        else:
            return render(request,'accounts/loginpage.html',{'msg':'Unknown user, Please login using valid credentials'})

    return render(request,'accounts/loginpage.html')

def ajax_email_exists(request):
    try:
        emailids=User.objects.values_list('email', flat=True)
        emailid =request.GET.get('email')
        if emailid in emailids:
            return JsonResponse({'result':'reject'})
    except:
        pass
    return JsonResponse({'result':'accept'})
def ajax_email_exists_edit(request):
    try:
        emailids=User.objects.values_list('email', flat=True)
        emailid =request.GET.get('email')
        print(emailid)

        existingemail=request.GET.get('existingemail')
        print(existingemail)
        if emailid in emailids :
            if emailid == existingemail:
                return JsonResponse({'result':'accept'})
            else:
                return JsonResponse({'result':'reject'})
    except:
        pass
    return JsonResponse({'result':'accept'})


from django.contrib.auth.decorators import login_required
@login_required
def userlogout(request):   
    logout(request)
    return redirect('accounts:UserLogin')