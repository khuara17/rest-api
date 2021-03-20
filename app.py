from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
# from model import db,ma
from flask_restful import Resource, Api
from thread import process


app = Flask(__name__)

api = Api(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class items(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    status = db.Column(db.VARCHAR(20))
    item = db.Column(db.VARCHAR(20))


#     def __init__(self,item):
#         self.status = 'pending'
#         self.item = item

class itemsSchema(ma.Schema):
    class Meta:
        fields = ['item','status']

class myapi(Resource):
    def get(self,delay_value):
        duration = process(delay_value)
        return {'time_taken' : duration},200
    


class postmethod(Resource):
    def post(self):
        item = request.json['item']
        data = items(item=item,status="pending")
        db.session.add(data)
        db.session.commit()
        # print(data.id)
        return {'item': data.item, 'status' : data.status, 'id' : data.id}

    def get(self):
        li = []
        data  = items.query.all()
        for i in data:
            li.append({'he' : [i.item,i.status,i.id] })
        return {'op' : li}





api.add_resource(myapi, '/item/<int:delay_value>')
api.add_resource(postmethod, '/add')


if __name__ == '__main__':
    app.run(debug=True)