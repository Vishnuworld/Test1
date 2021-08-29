from firstapp.models import CustomUser

user = CustomUser.objects.first()
print(user)

print(user.usertype)

user.usertype.add(2)  # seller
user.save()

print(user.usertype.all())

user.usertype.add(1)  # seller
user.save()
print(user.usertype.all())
