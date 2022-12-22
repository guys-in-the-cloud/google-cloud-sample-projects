from flask import Flask,render_template,request,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json



with open('config.json','r') as c:
    params = json.load(c)["params"]

local_server = True
db = SQLAlchemy()

app = Flask(__name__,static_fold='static',template_folder='template')
if(local_server==True):
    # app.config['SQLALCHEMY_DATABASE_URI'] = params["dev_uri"]
    # app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://Sarthak:"+params["PASSWORD"]+"@"+params["PUBLIC_IP_ADDRESS"]+"/"+params["DBNAME"]+"?unix_socket=/cloudsql/PROJECT_ID:"+params["PROJECT_ID"]+":"+params["INSTANCE_NAME"]
    app.config["SQLALCHEMY_DATABASE_URI"]= "mysql+mysqldb://Sarthak:12345@35.184.174.195:3306/codingthunder?unix_socket=/cloudsql/qwiklabs-gcp-00-cf60061fc83c:us-central1:codingthunder"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]
db.init_app(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_num = db.Column(db.String(12),  nullable=False)
    mes = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime)
   
class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content= db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime)

db.create_all()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/contact', methods=['GET','POST'])
def contact():    
    if(request.method=="POST"):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get("message")

        entry = Contacts(name=name,email=email,phone_num=phone,mes=message,date=datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html',params=params)


@app.route('/post/<string:post_slug>',methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params=params,post=post)
    

if __name__ == '__main__':
    app.run(debug=True)