from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self , phone , email , username , status , password , skills=None):
        if not phone:
            raise ValueError('Error Phone')
        if not email:
            raise ValueError('Error Email')
        if not username:
            raise ValueError('Error Username')
        if not status:
            raise ValueError('Error Status')
        
        user = self.model(
            phone = phone,
            email = self.normalize_email(email),
            username = username,
            status = status,
        )
        if skills is not None:
            user.skills = skills
        
        user.set_password(password)

        user.save(using = self._db)
        return user
        


    def create_superuser(self , phone , email , username , status , password , skills=None):
        user = self.create_user(phone , email , username , status , password , skills)
        user.is_admin = True
        user.save(using = self._db)
        return user