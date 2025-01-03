import MediaCat
import os
import shutil
import logging
from create_mediacat_db import executeInserts
from flask import Flask, request, render_template, session, redirect, g, url_for

logging.basicConfig(filename='mc.log', level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# This route clears any user info and sets the user and user_id when a user signs in.
@app.before_request
def before_request():
    g.user = None
    g.password = None
    g.user_id = None

    # Checking if a user is currently logged in, if so set g for user and user_id.
    if 'user' in session:
        g.user = session['user']
        g.user_id = session['user_id']
    
        
# main route def for home directory.        
@app.route("/")
def home():
    return render_template('index.html')

# route for login page.
@app.route("/login", methods=['GET', 'POST'])

def login():
    if request.method == 'POST':

        # Clear current user info (if there is any)
        session.pop('user', None)

        # Get username and password from login form and create a user object
        usr = MediaCat.create_user(str(request.form['user']), str(request.form['password']))

        # Log the login attempt
        app.logger.info('Processing login request for username: ' + str(usr.username) + ' user id: ' + str(usr.user_id))
        
        try:
            # Get username and user id. 
            session['user'] = usr.username
            session['user_id'] = usr.user_id
            #g.user = usr.user_id
            u = usr.user_id
            app.logger.info('Username: ' + usr.username + ' user id: ' + usr.user_id + ' logged in')
            return redirect(url_for('files', usr=u, _external=True))
            
        except:
            # Login failed attempt
            app.logger.info('User: ' + usr.username + ' failed to login')
            return render_template('login.html')
    return render_template('login.html')

# logout route clears all user info for that session
@app.route("/logout")
def logout():
    # Reset user and user_id
    g.user = None
    g.user_id = None
    # remove user from session
    session.pop('user', None)
    return render_template('index.html')




@app.route('/files/<usr>', methods=['GET', 'POST'])
def files(usr):

    usr = MediaCat.create_user_with_id(usr)
    usr_id = usr.user_id

    #total, used, free = shutil.disk_usage("/Users/zach.stall/Downloads")
    total, used, free = shutil.disk_usage("/")

    t=(total // (2**30))
    u=(used // (2**30))
    f=(free // (2**30))
    
    pf=f"{(f/t):.0%}"
    pu=f"{(u/t):.0%}"


    data = [ 
        ['Storage', 'GB'], 
        ['Free', f], 
        ['Used', u],  
    ] 

    top_10_dir = MediaCat.query_mediacat("select file_path, count(*) total, sum(file_size) size from files group by file_path order by total desc limit 10;")
    file_sum = MediaCat.query_mediacat("select sum(file_size) from files;")
    total_file = MediaCat.query_mediacat("select count(file_name) from files;")
    largest_file = MediaCat.query_mediacat("select file_size from files order by file_size desc limit 1;")
    file_type_totals = MediaCat.query_mediacat("select file_type, count(file_type) from files group by file_type order by count desc limit 10;")



    if request.method == 'POST' and 'pattern_to_query' in request.form:
        file_to_search = request.form['pattern_to_query']
        files = MediaCat.query_mediacat("select file_path, file_name, file_size from files where file_name ilike '%"+file_to_search+"%';")


        try:

            return render_template("home_file_view.html", 
                                file_to_search=file_to_search,
                                files=files, 
                                top_10_dir=top_10_dir, 
                                file_sum=file_sum, 
                                largest_file=largest_file, 
                                total_file=total_file, 
                                file_type_totals=file_type_totals, 
                                user=usr.username, 
                                total_used_mem=u,
                                total_free_mem=f, 
                                total_mem=t, 
                                pct_used_mem=pu, 
                                pct_free_mem=pf,
                                data=data, 
                                user_id=usr_id, 
                                u=usr,
                                admin=usr.admin,
                                super_user=usr.super_user)
        except TypeError as e:

            # Code to handle the TypeError
            app.logger.error("TypeError occurred: ", e)
            return render_template('index.html')
    
    if request.method == 'POST' and 'query_database' in request.form:
        database_query = request.form['query_database']
        query_results = MediaCat.query_mediacat(database_query)

        print(database_query)
        print(query_results)

        try:

            return render_template("home_file_view.html", 
                                database_query=database_query, 
                                query_results=query_results, 
                                top_10_dir=top_10_dir, 
                                file_sum=file_sum, 
                                largest_file=largest_file, 
                                total_file=total_file, 
                                file_type_totals=file_type_totals, 
                                user=usr.username, 
                                total_used_mem=u,
                                total_free_mem=f,  
                                total_mem=t, 
                                pct_used_mem=pu, 
                                pct_free_mem=pf,
                                data=data, 
                                user_id=usr_id, 
                                u=usr,
                                admin=usr.admin,
                                super_user=usr.super_user)
        except TypeError as e:

            # Code to handle the TypeError
            app.logger.error("TypeError occurred: ", e)
            return render_template('index.html')
            

    try:

        return render_template('home_file_view.html', 
                            top_10_dir=top_10_dir, 
                            file_sum=file_sum, 
                            largest_file=largest_file, 
                            total_file=total_file, 
                            file_type_totals=file_type_totals, 
                            user=usr.username, 
                            total_used_mem=u,
                            total_free_mem=f, 
                            total_mem=t, 
                            pct_used_mem=pu, 
                            pct_free_mem=pf,
                            data=data, 
                            user_id=usr_id, 
                            u=usr,
                            admin=usr.admin,
                            super_user=usr.super_user)
    except TypeError as e:

                # Code to handle the TypeError
                app.logger.error("TypeError occurred: ", e)
                return render_template('index.html')
    

@app.route('/walk_dir',  methods=['GET', 'POST'])
def query_for_file():

    #usr = MediaCat.create_user(str(request.form['user']), str(request.form['password']))
    u =session['user']
    u_id = session['user_id']


    if request.method == 'POST':
        q = request.form['new_dir']
        MediaCat.explore_directory(q)

        #print(u)
        #print(u_id)
        return redirect(url_for('files', usr=u_id, _external=True))
    return render_template('home_file_view.html', usr=u_id, _external=True)



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
