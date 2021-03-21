from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, ValidationError, Schema
import os
# from model import db
from flask_restful import Resource, Api
from thread import process


app = Flask(__name__)

api = Api(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def validate_item(item):
    items = ['book', 'pen', 'folder', 'bag']
    if item not in items:
        raise ValidationError("Item cannot be accepted")

class items(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    status = db.Column(db.VARCHAR(20))
    item = db.Column(db.VARCHAR(20))

class ItemsSchema(Schema):
    item = fields.String(validate=validate_item)

class GetMethod(Resource):
    def get(self,delay_value):
        duration = process(delay_value)
        return {'time_taken' : duration},200

class PostMethod(Resource):
    def post(self):
        item = request.get_json()
        val = item['item']
        try:
            result = ItemsSchema().load(item)
            data = items(item=val,status="pending")
            db.session.add(data)
            db.session.commit()
            return {'item': data.item, 'status' : data.status, 'id' : data.id},200
        except ValidationError as err:
            return {'error' : err.messages['item'] },400
    
    def get(self):
        li = []
        data  = items.query.all()
        for i in data:
            li.append({'he' : [i.item,i.status,i.id] })
        return {'op' : li}


api.add_resource(GetMethod, '/delay/<int:delay_value>')
api.add_resource(PostMethod, '/add')


if __name__ == '__main__':
    app.run(debug=True)