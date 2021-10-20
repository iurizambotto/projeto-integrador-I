from app.extensions.database import db
from flask import request, jsonify, render_template, abort
from app.models.tables import Users



'''
import requests
data = {
    "name": "Iuri Zambotto",
    "email": "iurizambotto13@gmail.com"
}
res = requests.post('http://127.0.0.1:5000/api/users/', json=data)




[
    {""}
]

import requests
res = requests.post('http://127.0.0.1:5000/api/user/', json={"name":"lalala"})
if res.ok:
    print(res.json())
    

User.query.limit(1).all()

res = requests.patch('http://127.0.0.1:5000/api/users/3', json={"name":"Iuri Zambotto"})
res.json()

res = requests.delete('http://127.0.0.1:5000/api/users/3')

res = requests.delete('http://127.0.0.1:5000/api/users/all/')

'''