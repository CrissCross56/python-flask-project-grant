from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

#python3 -m pipenv install ~~~
#python3 -m pipenv shell

db = PostgresqlDatabase("freecompany", user="grantterdoslavich", password='', host = 'localhost', port = "5432")

class BaseModel(Model):
    class Meta:
        database = db

class Avatar(BaseModel):
    name = CharField()
    job = CharField()
    rank = CharField()

db.connect()
#delete
db.drop_tables([Avatar])
#create
db.create_tables([Avatar])

#here we add something to the table, replace with what you will
Avatar(name='Fen Yor', job="Dark Knight", rank = 'officer').save()
Avatar(name="Garkin Silverleaf", job="Paladin", rank="Free Company Leader").save()
Avatar(name="Sala Mander", job="Warior", rank="officer").save()
Avatar(name="Felina Silverleaf", job="Bard", rank="Officer").save()
#initialize 
app = Flask(__name__)

@app.route('/avatars/',methods=['GET','POST'])
@app.route('/avatars/<id>', methods=['GET','PUT','DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            
            return jsonify(model_to_dict(Avatar.get(Avatar.id == id)))
        else:
            avatar_list = []
            for avatar in Avatar.select():
                avatar_list.append(model_to_dict(avatar))
            return jsonify(avatar_list)
    if request.method == 'POST':
        new_avatar = dict_to_model(Avatar,request.get_json())
        new_avatar.save()
        return jsonify({'success': True})
    if request.method == 'PUT':
        body = request.get_json()
        Avatar.update(body).where(Avatar.id == id).execute()
        return f'Avatar {id} has been updated'
    if request.method == 'DELETE':
        Avatar.delete().where(Avatar.id == id).execute()
        return f'Avatar {id} has been deleted'
    
@app.route('/')
def index():
    return 'I do enjoy my the company of my Free Company'

app.run(port=5000, debug=True)