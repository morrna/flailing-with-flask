from google.appengine.api import users
from google.appengine.ext import ndb

from flask import Flask, render_template, request
import flask as fl
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

### 
@app.route('/')
def hello():
    "Displays front page."
    return render_template("front_door.html")

@app.route('/about/')
def about_message():
    with open('content/about_msg.htm','r') as f:
        about_msg_str = f.read()
    
    return render_template("simple_page.html", pagetitle="About"
                                , content=about_msg_str)

@app.route('/user/')
def user_profile():
    user = users.get_current_user()

    if user:
        user_message = 'Hello ' + user.nickname() + ', good to see you!'
    else:
        user_message = 'Good day Mr./Ms. Anonymous!' \
                + ' <a href="' + users.create_login_url(request.url) + \
                '">Log in</a> with a Google account to change this message.'

    return render_template('simple_page.html', pagetitle = 'User' \
                            , content = user_message )



@app.route('/wall/', methods=['POST', 'GET'])
def wall_page():
#    ## Temporarily deter interlopers
#    excuse_msg = "Sorry, but I'm not done figuring this part out yet." \
#            + " Come back later!"
#    return render_template("simple_page.html"
#                            , pagetitle = "Under Construction"
#                            , content = excuse_msg
#                            )

    if request.method == 'POST':
        my_wall.add_message(request.form["new_message"])
        ## May not be needed if template is rendered after anyway.
        #return fl.redirect(fl.url_for("wall_page"))

    my_wall.load_messages()

    return render_template('wall_page.html', pagetitle='Wall', my_wall=my_wall)

@app.route('/oauth2callback/')
def oauth2callback():
    return fl.redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template('simple_page.html', pagetitle = '404 error' \
            , content='Sorry, nothing at this URL.') \
            , 404

WALL_NAME = 'default_wall'

def wall_key(this_name = WALL_NAME):
    return ndb.Key('Wall_of_Posts', this_name)

class Post_Author(ndb.Model):
    nickname = ndb.StringProperty(indexed=False)

class Wall_Post(ndb.Model):
    text = ndb.TextProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
    author = ndb.StructuredProperty(Post_Author)

### Tools etc.
class Wall:
    """
    An object for storing and loading a limited list of messages.
    This will probably need to be updated to work off of the Datastore.
    For now, the messages are not persistent.
    """

    def __init__(self, name_of_wall = WALL_NAME):
        self.max_messages = 12
        self.messages = []
        self.wall_name = name_of_wall

    def add_message(self, message):
        new_post = Wall_Post(parent=wall_key(self.wall_name))
        # Add parent key as attribute of Wall? It could perhaps be set on instantiation.

        if users.get_current_user():
            new_post.author = Post_Author( nickname = users.get_current_user().nickname() )
        else:
            new_post.author = Post_Author( nickname = "someone anonymous" )

        new_post.text = message
        new_post.put()

    def load_messages(self):
        
        post_query = Wall_Post.query( ancestor=wall_key(self.wall_name) ).order(-Wall_Post.time)
        self.messages = post_query.fetch(self.max_messages)




my_wall = Wall()

