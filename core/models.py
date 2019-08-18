from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, User
)
from django.db.models import signals
from django.core.mail import send_mail


class DataBase(models.Model):
    db_name = models.CharField(max_length=100)

    def __str__(self):
        return self.db_name


class UserManager(BaseUserManager):
    
    def create_user(self, email=None, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_staffuser(
            email=email,
            password=password,
        )
        user.email = email
        user.is_staff = True
        user.is_admin = True
        user.role = 'admin'
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, models.Model):
    
    email = models.EmailField(unique=True)
    dbs = models.ManyToManyField(DataBase, related_name='users')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)   
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):        
        return self.email

    
    def has_perm(self, perm, obj=None):        
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):        
        # Simplest possible answer: Yes, always
        return True

    

def user_post_save(sender, instance, signal, created, *args, **kwargs):
    if created:
        # sends email to user when the user is created.
        import pdb;pdb.set_trace()
        subject = 'Your Account is ready'
        message = """
                        Please follow the given link and login with the below mentioned credentials.
                        email: {}
                        password: {}""".format(instance.email, instance.password)
                        
        email_from = settings.EMAIL_HOST_USER         
        # send_mail( subject, message, email_from, [instance.email,])     


signals.post_save.connect(user_post_save, sender=User)



