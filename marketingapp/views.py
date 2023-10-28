from django.shortcuts import render

# Create your views here.
def marketing_dashboard(request):
    return render(request, "index1111.html")

def facebook_campaign(request):
    return render(request, "facebook.html")

def instagram_campaign(request):
    return render(request, "instagram.html")

def linkedin_campaign(request):
    return render(request, "linkedin.html")

def tiktok_campaign(request):
    return render(request, "tiktok.html")

def youtube_campaign(request):
    return render(request, "youtube.html")

def twitter_campaign(request):
    return render(request, "twitter.html")

def marketing_profile(request):
    return render(request, "profile-setting.html")



