import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.mysql import MySQL
from wtforms import validators

import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters

app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://milho:pipocadepanela@67.205.166.236/pipocadb'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# Create models

####### Personal Universe

class fname(db.Model):
		idfname = db.Column(db.Integer, primary_key=True)
		fname = db.Column(db.String(15), unique=True,nullable=False)

		def __str__(self):
				return self.fname

class lname(db.Model):
		idlname = db.Column(db.Integer, primary_key=True)
		lname = db.Column(db.String(15), unique=True,nullable=False)

		def __str__(self):
				return self.lname

class country(db.Model):
		idcountry = db.Column(db.Integer, primary_key=True)
		cname = db.Column(db.String(15), unique=True,nullable=False)

		def __str__(self):
				return self.cname

class person(db.Model):
		idperson = db.Column(db.Integer, primary_key=True)
		fname = db.Column(db.ForeignKey('fname.idfname'), nullable=False)
		lname = db.Column(db.ForeignKey('lname.idlname'),nullable=False )
		country = db.Column(db.ForeignKey('country.idcountry'),nullable=False)
		art_name = db.Column(db.String(15),nullable=True)

		def __int__(self):
				return self.idperson

###############
######### Content Universe

class content_name(db.Model):
		idname = db.Column(db.Integer, primary_key=True)
		name = db.Column(db.String(45), unique=True,nullable=False)

		def __str__(self):
				return self.name


class cast_job(db.Model):
		idjob = db.Column(db.Integer, primary_key=True)
		jobname = db.Column(db.String(15), unique=True,nullable=False)
		description = db.Column(db.String(145),nullable=True)

		def __str__(self):
				return self.name

class content(db.Model):
		idcontent = db.Column(db.Integer, primary_key=True)
		name = db.Column(db.ForeignKey(content_name.idname), unique=True,nullable=False)
		country = db.Column(db.ForeignKey('country.idcountry'),nullable=False)
		released = db.Column(db.Date(),nullable=False)

class cast_member(db.Model):
		idperson = db.Column(db.ForeignKey(person.idperson), primary_key=True)
		idcontent = db.Column(db.ForeignKey(content.idcontent),primary_key=True)
		idjob = db.Column(db.ForeignKey(cast_job.idjob),primary_key=True)
		#Uma pessoa pode ter mais de uma função em um memso filme ( ex: Produtor e DIretor)


###################

# Flask views
@app.route('/')
def index():
		return '<a href="/admin/">Click me to get to Admin!</a>'


# Create admin
admin = admin.Admin(app, name='piPoCa DB', template_mode='bootstrap3')

# Add views
#admin.add_view(fname_admin(fname, db.session))
admin.add_view(sqla.ModelView(fname, db.session))
admin.add_view(sqla.ModelView(lname, db.session))
admin.add_view(sqla.ModelView(country, db.session))
admin.add_view(sqla.ModelView(person, db.session))
admin.add_view(sqla.ModelView(content_name, db.session))
admin.add_view(sqla.ModelView(cast_job, db.session))
admin.add_view(sqla.ModelView(content, db.session))
admin.add_view(sqla.ModelView(cast_member, db.session))


if __name__ == '__main__':
		# Build a sample db on the fly, if one does not exist yet
		db.create_all()
		# Start app
		app.run(debug=True, host='67.205.166.236', port=80)
