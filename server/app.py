from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages',methods=["POST","GET"])
def messages():
    if request.method=="GET":
     for message in Message.query.all():
        all_messages=[]
        message_dict={
            "id":message.id,
            "body" :message.body,
            "username":message.username,
            "created_at":message.created_at,
            "updated_at":message.updated_at                      
        }   
        all_messages.append(message_dict)
        response=make_response(all_messages,200)
        return response
    elif request.method=="POST":
       all_new_messages=request.get_json()
       new_Message=Message(
          body=all_new_messages.get("body"),
          username=all_new_messages.get("username")
       )
       db.session.add(new_Message)
       db.session.commit()
       new_Message_dict=new_Message.to_dict()
       response=make_response(new_Message_dict,201)
       return response
@app.route('/messages/<int:id>',methods=["PATCH","DELETE"])
def messages_by_id(id):
    message=Message.query.filter(Message.id==id).first()   
    if request.method=="PATCH":  
         if not message:
            res_dict={
               "message":"Meassage does not exist"
            }    
            response= make_response(res_dict,404) 
            return response
         my_data=request.get_json()  
         for attr in my_data:
            # setattr(message,attr,request.form.get(attr))
            # db.session.add(message)
            # db.session.commit()
            # response_dict=message.to_dict()            
            # response=make_response(response_dict,200)
            # return response  
            setattr(message,attr,my_data.get(attr))
            db.session.add(message)
            db.session.commit()
            bakery_serialized1=message.to_dict()            
            response=make_response(bakery_serialized1,200)
            return response       
            
    elif request.method=="DELETE":
       if message:
          db.session.delete(message)
          db.session.commit()
          response_dict={
          "Message":"Message deleted successfully"
          } 
          response=make_response(response_dict,200)
          return response
       else:
          error_mes={
             "error":"Message not found"
          } 
          response=make_response(error_mes,404)
          return response
       
if __name__ == '__main__':
    app.run(port=5555)
