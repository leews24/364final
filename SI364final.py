import os
import requests
import json
from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash


############################
# Application configurations
############################
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string from si364'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres:0000@localhost/wwsleefinal"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

##################
### App setup ####
##################
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) # set up login manager

owmkey = "6414e7704376b3841968b4f46522a771"

#########################
##### Set up Models #####
#########################

## All provided.

# Association tables

a_search_locations = db.Table('a_search_locations', db.Column('searchlog_id', db.Integer, db.ForeignKey('searchlog.id')), db.Column('locations_id', db.Integer, db.ForeignKey('locations.id')))

a_user_collection = db.Table('a_user_collection', db.Column('locations_id', db.Integer, db.ForeignKey('locations.id')), db.Column('userweatherset_id', db.Integer, db.ForeignKey('userweatherset.id')))


### Database of users
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    collection = db.relationship("Locations", backref="User")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

### Database of all previously searched locations
class Locations(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer,primary_key=True)
    zip = db.Column(db.String(8))
    city = db.Column(db.String(64))
    users = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "{}: {}".format(self.zip, self.city)

### Database of user curated sets of locations
class UserWeatherSet(db.Model):
    __tablename__ = "userweatherset"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255))
    #one-to-many
    users = db.Column(db.Integer, db.ForeignKey('users.id'))
    #many to many
    locations = db.relationship("Locations", secondary=a_user_collection, backref=db.backref('UserWeatherSet', lazy='dynamic'), lazy='dynamic')


class SearchLog(db.Model):
    __tablename__ = "searchlog"
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(32), unique=True)
    locations = db.relationship("Locations", secondary=a_search_locations, backref=db.backref("searches", lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return "{} (ID: {})".format(self.term, self.id)

########################
##### Set up Forms #####
########################

class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            print("test")
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')



class LocationSearchForm(FlaskForm):
    loc = StringField("Enter a zip code:", validators=[Required()])
    submit = SubmitField('Submit')

    def validate_loc(self,field):
        if len(int(field.data)) != 5:
            print("not5")
            raise ValidationError('Please enter 5 digit zipcodes')
        else:
            print("jackson5")

class MemberLocationSearchForm(FlaskForm):
    loc = StringField("Enter a zip code to add to your dashboard:", validators=[Required()])
    submit = SubmitField('Submit')

    def validate_loc(self,field):
        if len(int(field.data)) != 5:
            print("not5")
            raise ValidationError('Please enter 5 digit zipcodes')
        else:
            print("jackson5")

class SetCreateForm(FlaskForm):
    name = StringField('Set Name',validators=[Required()])
    loc_picks = SelectMultipleField('Locations to include')
    submit = SubmitField("Create Set")

class NNButtonForm(FlaskForm):
    submit = SubmitField("Change Name")

class NNLocButtonForm(FlaskForm):
    nickname = StringField('Nickname',validators=[Required()])
    submit = SubmitField("Update Set")

class DeleteButtonForm(FlaskForm):
    submit = SubmitField("Delete")

class DeleteLocButtonForm(FlaskForm):
    submit = SubmitField("Delete Location")

################################
####### Helper Functions #######
################################

def get_loc_by_id(id):
    l = Locations.query.filter_by(id=id).first()
    return l

def get_or_create_set(name, current_user, loc_list=[]):
    check = UserWeatherSet.query.filter_by(name=name, users=current_user.id).first()
    if check:
        return check
    else:
        newset = UserWeatherSet(name=name, users=current_user.id, locations=[])
        for loc in loc_list:
            newset.locations.append(loc)
        db.session.add(newset)
        db.session.commit()
        return newset

def ktof(t):
    t = int(t)*1.8 - 459.67
    return round(t, 1)


###################################
##### Routes & view functions #####
###################################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('memberhome'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home'))

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)


@app.route('/', methods=["GET","POST"])
def home():
    form = LocationSearchForm()
    if request.method == "POST":
        if len(form.loc.data) != 0:
            print("post working")
            zipcode = form.loc.data
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            parameters = {}
            parameters['zip'] = zipcode + ",us"
            parameters["appid"] = owmkey
            resp = requests.get(base_url, params = parameters)
            text = resp.text
            results = json.loads(text)

            return render_template('index.html',form = form, results = results)
        else:
            print("no entry yet")
            results = None
            return render_template('index.html',form = form, results = None)
    else:
        print("nopost")
        results = None
        return render_template('index.html',form = form, results = None)

    return render_template('index.html',form=form)


@app.route('/memberhome', methods=["GET","POST"])
@login_required
def memberhome():
    form = LocationSearchForm()
    if request.method == "POST":
        if len(form.loc.data) != 0:
            print("post working")
            zipcode = form.loc.data
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            parameters = {}
            parameters['zip'] = zipcode + ",us"
            parameters["appid"] = owmkey
            resp = requests.get(base_url, params = parameters)
            text = resp.text
            results = json.loads(text)

            city = results['name']

            newentry = Locations(city = city, zip = zipcode, users = current_user.id)
            db.session.add(newentry)
            db.session.commit()

            return render_template('search.html',form = form, results = results)
        else:
            print("no entry yet")
            results = None
            return render_template('search.html',form = form, results = None)
    else:
        print("nopost")
        results = None
        return render_template('search.html',form = form, results = None)

    return render_template('search.html',form=form)

@app.route('/search_history',methods=["GET","POST"])
def searchhistory():
    locs = Locations.query.all()
    return render_template('search_history.html', locs = locs)

@app.route('/newset',methods=["GET","POST"])
@login_required
def newset():
    form = SetCreateForm()
    locs = Locations.query.all()
    choices = [(str(l.id), str(l.city)) for l in locs]
    form.loc_picks.choices = choices
    if form.validate_on_submit():
        loclist = []
        for pick in form.loc_picks.data:
            loclist.append(get_loc_by_id(pick))
        get_or_create_set(form.name.data, current_user, loclist)
        return redirect(url_for('sets'))
    return render_template('newset.html', form=form)

@app.route('/sets',methods=["GET","POST"])
@login_required
def sets():
    form = DeleteButtonForm()
    form2 = NNButtonForm()
    sets = UserWeatherSet.query.filter_by(users=current_user.id).all()
    return render_template('sets.html', sets=sets, form=form, form2 = form2)

@app.route('/set/<id_num>')
@login_required
def single_set(id_num):
    id_num = int(id_num)
    set = UserWeatherSet.query.filter_by(id=id_num).first()
    locs = set.locations.all()

    rettemps = {}
    retconds = {}

    for l in locs:
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        parameters = {}
        parameters['zip'] = str(l.zip) + ",us"
        parameters["appid"] = owmkey
        resp = requests.get(base_url, params = parameters)
        text = resp.text
        results = json.loads(text)
        rettemps[l.zip] = ktof(results['main']['temp'])
        retconds[l.zip] = results['weather'][0]['main']

    return render_template('set.html',set=set, locs=locs, rettemps = rettemps, retconds = retconds, form=form)

@app.route('/delete/<set>',methods=["GET","POST"])
@login_required
def delete(set):
    db.session.delete(UserWeatherSet.query.filter_by(name=set).first())
    flash("Deleted set <{}>".format(set))
    return redirect(url_for("sets"))

@app.route('/nickname/<set>',methods=["GET","POST"])
@login_required
def add(set):
    form = NNLocButtonForm()
    if form.validate_on_submit():
        entry = UserWeatherSet.query.filter_by(name=set).first()
        entry.name = form.nickname.data
        db.session.commit()
        return redirect(url_for('sets'))
    return render_template('add.html',form=form, set=set)

if __name__ == "__main__":
    db.create_all()
    manager.run()
