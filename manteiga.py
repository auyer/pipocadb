import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_mysql import MySQL
from wtforms import validators
from sqlalchemy_utils import EmailType
from sqlalchemy_views import CreateView, DropView
import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from sqlalchemy import CheckConstraint
from sqlalchemy.orm.session import object_session
from datetime import datetime
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://milho:pipocadepanela@67.205.166.236/pipocadb' 
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# Create models

####### Personal Universe

class fname(db.Model):
	idfname = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.String(15), unique=True,nullable=False)
	
	def __repr__(self):
		return self.fname

class lname(db.Model):
	idlname = db.Column(db.Integer, primary_key=True)
	lname = db.Column(db.String(15), unique=True,nullable=False)
	
	def __repr__(self):
		return self.lname

class country(db.Model):
	idcountry = db.Column(db.Integer, primary_key=True)
	cname = db.Column(db.String(15), unique=True,nullable=False)

	def __repr__(self):
		return self.cname

class person(db.Model):
	idperson = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.ForeignKey('fname.idfname'), nullable=False)
	lname = db.Column(db.ForeignKey('lname.idlname'),nullable=False )
	country = db.Column(db.ForeignKey('country.idcountry'),nullable=False)
	art_name = db.Column(db.String(15),nullable=True)
	
	First_Name = db.relationship('fname')
	Last_Name = db.relationship('lname')
	Country_Name= db.relationship('country') 

	def __repr__(self):
		return self.art_name
	
	def get_aname(idperson):
		session = object_session(person)
		a= session.querry(art_name).filter(person.idperson==idperson)
		print("\n\n\n",a,"\n\n\n")
		return a	

class insert_person(db.Model):
	idperson = db.Column(db.Integer, primary_key=True)
	fnome = db.Column(db.String(15), unique=True,nullable=False)
	lname = db.Column(db.String(15), unique=True,nullable=False)
	country = db.Column(db.String(15), unique=True,nullable=False)
	art_name = db.Column(db.String(15),nullable=True)
###############
######### Content Universe

class content_name(db.Model):
	idcname = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(45), unique=True,nullable=False)
	
	def __repr__(self):
		return self.name
	
	def get_name(self,idn):
		session = object_session(self)
		return session.querry(name).filter(content_name.idcname==idn)		

class cast_job(db.Model):
	idjob = db.Column(db.Integer, primary_key=True)
	jobname = db.Column(db.String(15), unique=True,nullable=False)
	description = db.Column(db.String(145),nullable=True)
	
	def __repr__(self):
		return self.jobname

class content(db.Model):
	idcontent = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.ForeignKey(content_name.idcname), unique=True,nullable=False)
	country = db.Column(db.ForeignKey('country.idcountry'),nullable=False)
	released = db.Column(db.Date(),nullable=False)

	Content_Name = db.relationship('content_name')	
	Country_Name = db.relationship('country')	
	

	def __repr__(self):
		#return content_name.get_name( self ,self.idcontent)
		return str(self.idcontent)

class cast_member(db.Model):
	idperson = db.Column(db.ForeignKey(person.idperson), primary_key=True)
	idcontent = db.Column(db.ForeignKey(content.idcontent),primary_key=True)
	idjob = db.Column(db.ForeignKey(cast_job.idjob),primary_key=True)

	Person = db.relationship(person)
	Content_ID = db.relationship(content)
	Job = db.relationship(cast_job)
	
	def __repr__(self):
		return person.get_aname(self.idperson)
	#Uma pessoa pode ter mais de uma função em um memso filme ( ex: Produtor e DIretor)


###################
##### User Universe

class user(db.Model):
	iduser = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.ForeignKey('fname.idfname'), nullable=False)
	lname = db.Column(db.ForeignKey('lname.idlname'),nullable=False )
	born = db.Column(db.Date(), nullable=False)
	country = db.Column(db.ForeignKey('country.idcountry'),nullable=False)
	#email = db.Column(EmailType,nullable=False)
	email = db.Column(db.String(45), unique=True)
	ative_until = db.Column(db.DateTime())
	CheckConstraint("REGEXP_LIKE(email,'^[a-zA-Z][a-zA-Z0-9_\.\-]+@([a-zA-Z0-9-]{2,}\.)+([a-zA-Z]{2,4}|[a-zA-Z]{2}\.[a-zA-Z]{2})$')", name='emailcheck')	
	First_Name = db.relationship('fname')
	Last_Name = db.relationship('lname')
	Country_Name= db.relationship('country')

	def __repr__(self):
		return str(self.iduser)

class content_viewed(db.Model):
	user_id = db.Column(db.ForeignKey(user.iduser), primary_key=True)
	content_id = db.Column(db.ForeignKey(content.idcontent),primary_key=True)
	datetime = db.Column(db.DateTime(),primary_key=True, default=str(datetime.now()))
	rating = db.Column(db.Boolean())
	percentage = db.Column(db.Numeric, nullable=True)
	CheckConstraint('percentage <100 ', name='percentagecheck')

	Content = db.relationship('content')
	User = db.relationship('user')
	
	
class search(db.Model):
	user_id = db.Column(db.ForeignKey(user.iduser), primary_key=True)
	terms_hash = db.Column(db.String(145) ,primary_key=True)
	datetime = db.Column(db.DateTime(),nullable=False, default=str(datetime.now()))

	User_ID = db.relationship('user') 
#################
# Flask views
@app.route('/')
def index():
	return '<a href="/admin/">Click me to get to Admin!</a>'


# Create admin
admin = admin.Admin(app, name='PiPoCa Admin', template_mode='bootstrap3')

# Add views
admin.add_view(sqla.ModelView(fname, db.session))
admin.add_view(sqla.ModelView(lname, db.session))
admin.add_view(sqla.ModelView(country, db.session))
admin.add_view(sqla.ModelView(person, db.session))
admin.add_view(sqla.ModelView(insert_person, db.session))
admin.add_view(sqla.ModelView(content_name, db.session))
admin.add_view(sqla.ModelView(cast_job, db.session))
admin.add_view(sqla.ModelView(content, db.session))
admin.add_view(sqla.ModelView(cast_member, db.session))
admin.add_view(sqla.ModelView(user, db.session))
admin.add_view(sqla.ModelView(content_viewed, db.session))
admin.add_view(sqla.ModelView(search, db.session))

if __name__ == '__main__':
	db.create_all()

	# Start app
	app.run(debug=True, host='67.205.166.236', port=80)
