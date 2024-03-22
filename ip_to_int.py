# import IPy
#
#
# ip = '200.233.1.2'
#
#
# int_ip = IPy.IP(ip).int()
#
# print(int_ip)


from flask import Flask


import os
import base64
import secrets


app = Flask(__name__)
app.secret_key = base64.b64encode(os.urandom(24))
print(app.secret_key)
app.secret_key = secrets.token_hex(16)
print(app.secret_key)









