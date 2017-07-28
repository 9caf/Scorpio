# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask_restful import Api, Resource
 
app = Flask(__name__)
api = Api(app)
 
USER_LIST = {
    '1': {'name':'Michael'},
    '2': {'name':'Tom'},
}
 
class UserList(Resource):
    def get(self):
        return USER_LIST
 
    def post(self):
        user_id = int(max(USER_LIST.keys())) + 1
        user_id = '%i' % user_id
        USER_LIST[user_id] = {'name': request.form['name']}
        return USER_LIST
 
api.add_resource(UserList, '/users')

@app.route('/')
def index():
    return render_template('test.html')
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)