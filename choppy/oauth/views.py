from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect

from .models import GitHubUser

# Set your GitHub OAuth URLs
client_id = settings.GITHUB_CLIENT_ID
client_secret = settings.GITHUB_CLIENT_SECRET
auth_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"
user_url = "https://api.github.com/user"


# Initiate the OAuth process
def initiate_oauth(request):
    params = {
        "client_id": client_id,
        "redirect_uri": "http://127.0.0.1:8000/oauth/authenticate",
        "scope": "user",
        "allow_signup": "true",
    }
    url = f"{auth_url}?{urlencode(params)}"
    return HttpResponseRedirect(url)


# Handle GitHub's redirect with the code
def handle_oauth(request):
    code = request.GET.get("code")
    if not code:
        return HttpResponse("No code provided", status=400)

    print(code)

    # Exchange code for access token
    token_response = requests.post(
        token_url,
        headers={"Accept": "application/json"},
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": "http://127.0.0.1:8000/oauth/authenticate",
        },
    )
    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        return HttpResponse("Failed to authenticate", status=400)

    # Use access token to fetch user information
    user_response = requests.get(
        user_url, headers={"Authorization": f"token {access_token}"}
    )
    user_data = user_response.json()

    # Create or get the GitHub user
    github_id = user_data["id"]
    username = user_data["login"]
    avatar_url = user_data.get("avatar_url")
    email = user_data.get("email")

    user, created = GitHubUser.objects.get_or_create(
        github_id=github_id,
        defaults={
            "username": username,
            "access_token": access_token,
            "avatar_url": avatar_url,
            "email": email,
        },
    )
    if not created:
        # Update the access token if user already exists
        user.access_token = access_token
        user.save()

    # Log in the user
    login(request, user)
    return HttpResponse(f"Authenticated as {user.username}")
