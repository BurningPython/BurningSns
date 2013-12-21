from django.test import TestCase
from Accounts.models import MyUser,OpenAuth

def test():
    
    pass

def main():
    user = MyUser.objects.get(username = "a418146081")
    auth = user.openauth_set.all()[0]
    print(auth.site)
    print(auth.access_token)
    print(auth.refresh_token)
    print(auth.openid)

if __name__ == "__main__":
    main()