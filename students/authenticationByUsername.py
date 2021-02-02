from django.contrib.auth.models import User

class AuthenticateByEmail:
    def authenticate(self, username, password):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            else:
                return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExistL
            return None
        else:
            return user
