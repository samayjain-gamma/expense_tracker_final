from datetime import datetime

print(datetime.now())
print(type(datetime.now()))


time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
print(time)
print(type(time))
