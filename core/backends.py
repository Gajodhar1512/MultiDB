from core.models import User
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):

    def authenticate(email= None,password= None):
        import pdb;pdb.set_trace()
        try:
            user = User.objects.get(email=email)

            if user is not None:
                if user.check_password(password):
                    return user
                else :
                    return None
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None