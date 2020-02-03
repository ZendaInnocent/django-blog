# from django.db import models
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             email = self.normalize_email(email),
#             username = username
#         )
#         user.set_password(password)
#         user.save(using=self._db,)
#         return user


#     def create_superuser(self, username, email, password):
#         user = self.create_user(
#             username, email, password=password
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

# class CustomUser(AbstractBaseUser):
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(verbose_name='Email Address', max_length=255, unique=True)

#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.username

#     USERNAME_FIELD = 'email'
