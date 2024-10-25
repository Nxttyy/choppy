from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class GitHubUserManager(BaseUserManager):
    def create_user(self, github_id, username, access_token, **extra_fields):
        if not github_id:
            raise ValueError("The GitHub ID is required")
        user = self.model(
            github_id=github_id,
            username=username,
            access_token=access_token,
            **extra_fields,
        )
        user.set_unusable_password()  # Password not required, since login is via GitHub
        user.save(using=self._db)
        return user


class GitHubUser(AbstractBaseUser, PermissionsMixin):
    github_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    access_token = models.CharField(max_length=255)
    avatar_url = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    objects = GitHubUserManager()

    USERNAME_FIELD = "github_id"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
