import uuid
import hashlib
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
 
print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%B %d, %Y %H:%M:%S")
print("date and time =", dt_string)

print(str(uuid.uuid4()))

hash_gen = hashlib.sha512()
hash_gen.update("12345".encode('utf-8'))
print("First: " + hash_gen.hexdigest())

hash_gen.update("12345".encode('utf-8'))
print("Second: " + hash_gen.hexdigest())