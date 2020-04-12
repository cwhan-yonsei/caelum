from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class UserManager(BaseUserManager):
    def creat_user(self, email, password=None, portal_id=None, name=None, dept_major=None, username=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            portal_id = portal_id,
            name = name,
            dept_major = dept_major,
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, portal_id, name, dept_major, username):
        user = self.creat_user(
            email,
            password=password,
            portal_id = portal_id,
            name = name,
            dept_major = dept_major,
            username = username,
        )

        user.is_admin = True
        user.is_active = True
        user.is_email_verified = True

        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    portal_id = models.CharField(
        max_length=10,
        unique=True,
        null=True,
    )
    name = models.CharField(
        max_length=30,
        null=True,
    )
    dept_major = models.CharField(
        max_length=50,
        null=True,
    )
    username = models.SlugField(
        max_length=30,
        null=True,
        unique=True,
    )

    # Not active until email verification
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = [

    ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

