from config import Config

my_c = Config()

print("Config dict")
print(my_c.__dict__)

my_c.locoid = "br187"

print("Config dict")
print(my_c.__dict__)

my_c.save()