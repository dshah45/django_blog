from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
from django.core.mail import send_mail
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post


# Create your views here.
def home(request):
    allPosts = Post.objects.all().order_by('-views')
    allatest = Post.objects.all().order_by('-timeStamp')
    context = {'allPosts': allPosts, 'allatest': allatest}
    return render(request, 'home/home.html', context)


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()

            # Send Email
            send_mail(
                'Subject - Django Email Testing',
                'Hello ' + name + ',\n' + 'Thank you for Contacting Us.. We will be on touch with you shortly',
                '',  # Admin
                [
                    email,
                ]
            )

            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")


def about(request):
    return render(request, 'home/about.html')


def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request, "No search result found, Please refine you search")

    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)


def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) > 10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, " Passwords do not match")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " Your Account has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")


def handleLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid, Please try Again")
            return redirect('home')

    return HttpResponse("404 - NOT FOUND")


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')
