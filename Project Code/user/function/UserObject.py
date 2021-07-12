from registration.models import UserRegistration


def returnUserName(useremail):
    user_object = UserRegistration.objects.get(uemail=useremail)
    user_name = user_object.uname
    return user_name
