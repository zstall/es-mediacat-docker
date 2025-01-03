import hashlib
import os
import json
import shutil
import heapq
import time
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from pymediainfo import MediaInfo
from operator import attrgetter

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configure SQLAlchemy 
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://admin:admin@postgres:5432/mc'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Users - Database Model ~ Single Row Within DB
class Users(db.Model):
    # Class Variables
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Files - Database Model
class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_sha1 = db.Column(db.String(100), unique=True, nullable=False)
    file_name = db.Column(db.String(255), unique=False, nullable=False)
    file_type = db.Column(db.String(255), unique=False, nullable=True)
    file_path = db.Column(db.String(1000), unique=False, nullable=False)
    file_size = db.Column(db.Integer, unique=False, nullable=True)
    file_date_created = db.Column(db.DateTime, unique=False, nullable=False)
    file_date_updated = db.Column(db.DateTime, unique=False, nullable=False)
    file_attributes = db.Column(db.JSON, unique=False, nullable=True)

    # input_string is the directory + file name ex) /home/user/test.txt
    def set_sha1(self, input_string):
        self.file_sha1 = hashlib.sha1(input_string.encode()).hexdigest()

def explore_directory(directory, trace=True):
    for root, sub_dirs, files in os.walk(directory):
        if trace:
            print(
                f"Root: {root}\n"
                f"Sub Directories: {sub_dirs}\n"
                f"Files: {files}\n\n"
            )
        for file in files:
            input_string = root + '/' + file
            new_file = Files(file_name=file)

            general_track = runMediaInfo(input_string)
            date_created = time.ctime(os.path.getctime(input_string))
            fjson = json.dumps(general_track.__dict__)


            new_file.set_sha1(input_string)
            new_file.file_name = file
            new_file.file_type = general_track.file_extension
            new_file.file_path = root
            new_file.file_size = general_track.file_size
            new_file.date_created = date_created
            new_file.file_updated = general_track.file_last_modification_date
            new_file.file_attributes = fjson
            
            check_file = Files.query.filter_by(file_sha1=new_file.file_sha1).first()
            if check_file:
                pass
            else:
                db.session.add(new_file)
                db.session.commit()

def runMediaInfo(file):
    media_info = MediaInfo.parse(file)
    general_track = media_info.general_tracks[0]
    return (general_track)


# Routes
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

@app.route("/login_page")
def login_page():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("login.html")

# Login
@app.route("/login", methods=["Post"])
def login():
    # Collect the user information from the form
    username = request.form['username']
    password = request.form['password']
    # Create Users object if user exists in DB
    user = Users.query.filter_by(username=username).first()
    # IF User exists and Password is correct, create a new session for user, else return to index
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template("index.html")

# Register
@app.route("/register", methods=["POST"])
def register():
        username = request.form['username']
        password = request.form['password']
        # Create Users object if user exists in DB
        user = Users.query.filter_by(username=username).first()

        if user:
            return render_template("index.html", error="User already exists")
        else:
            new_user = Users(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect(url_for('login_page'))

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        # Get user id from usr object passed into function
        #user_id = usr.user_id

        # Use shutil to get total storage, used, and free on device
        total, used, free = shutil.disk_usage("/")

        # convert to GB
        t=(total // (2**30))
        u=(used // (2**30))
        f=(free // (2**30))

        # Calculate percentages of free and used
        pf=f"{(f/t):.0%}"
        pu=f"{(u/t):.0%}"

        # Create an array of data
        data = [ 
            ['Storage', 'GB'], 
            ['Free', f], 
            ['Used', u],  
        ] 
        
        dir = {}
        ext = {}
        file_sum = 0
        files = Files.query.all()

        if files:
            for d in files:
                dir.setdefault(d.file_path, 0)
                dir[d.file_path] = dir[d.file_path] + 1
                ext.setdefault(d.file_type, 0)
                ext[d.file_type] = ext[d.file_type] + 1
                file_sum += d.file_size

            max_attr = max(files, key=attrgetter('file_size'))

            top_10_dir = heapq.nlargest(10, dir.items(), key=lambda item: item[1])
            total_file = len(files)
            largest_file = max_attr.file_size
            file_type_totals = heapq.nlargest(10, ext.items(), key=lambda item: item[1])
            

            print(top_10_dir)
            print(total_file)
            print(largest_file)
            print(file_type_totals)
            print(file_sum)

            return render_template('dashboard.html', 
                                    username=session['username'],
                                    top_10_dir=top_10_dir, 
                                    file_sum=file_sum, 
                                    largest_file=largest_file, 
                                    total_file=total_file, 
                                    file_type_totals=file_type_totals,  
                                    total_used_mem=u,
                                    total_free_mem=f, 
                                    total_mem=t, 
                                    pct_used_mem=pu, 
                                    pct_free_mem=pf,
                                    data=data)
    
        elif session['username']:
    
            return render_template('dashboard.html', 
                            username=session['username'],  
                            total_used_mem=u,
                            total_free_mem=f, 
                            total_mem=t, 
                            pct_used_mem=pu, 
                            pct_free_mem=pf,
                            data=data)
        else:
            return redirect('home')

@app.route("/walk_dir", methods=['POST'])
def query_for_file():
    if "username" in session:
        dir = request.form['directory']
        explore_directory(dir)
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('home'))


# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)