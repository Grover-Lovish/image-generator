from django.shortcuts import render,HttpResponse,redirect
from .forms import CustomUserForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Feedback
from image_generator.settings import OPENAI_API_KEY
from django.core.files.base import ContentFile
from .models import Image
import requests

# Create your views here.
def home(request):
    try:
        fbks = Feedback.objects.all()
    except:
        fbks = None
    content = {
        "fbks" : fbks
    }
    return render(request,"index.html",content)

@login_required(login_url="login")
def generator(request):
    import openai
    openai.api_key = OPENAI_API_KEY
    obj = None
    if openai.api_key is not None and request.method == "POST":
        text = request.POST.get('imagination')
        response = openai.Image.create(
            prompt = text,
            size = "256x256"
        )
        print(response)
        img_url = response['data'][0]['url']
        response = requests.get(img_url)
        img_file = ContentFile(response.content)
        
        count = Image.objects.count()+1
        fname = f"image-{count}.jpg"
        obj = Image(phrase = text)
        obj.ai_image.save(fname,img_file)
        obj.save()
    return render(request,"generator.html",{"object":obj})


def register(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already Logged In")
        return redirect("home")
    else:
        form = CustomUserForm()
        if request.method == "POST":
            form = CustomUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                messages.success(request,"Account created successfully")
                return redirect("login")
        content = {
            'form' : form,
            'title' : "Register",
        }
        return render(request,"register.html",content)
    
    
def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already Logged In")
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username = username, password= password)
            if user is not None:
                auth_login(request,user)
                messages.success(request,"Logged In Successfully")
                return redirect("home")
            else:
                messages.error(request,"Invalid Username and Password")
                return redirect('login')
        content = {
            "title" : "Log-In"
        }
        return render(request,"login.html",content)
    
    
@login_required(login_url="login")
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request,"Logged Out Successfully")
    return redirect("home")


@login_required(login_url="login")
def feedback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('mobile')
        message = request.POST.get('message')

        fbk = Feedback(
            name = name,
            email = email,
            phone = phone,
            message = message,
        )
        messages.success(request,"Feedback sent Successfully!")
        fbk.save()
    return redirect("home")

