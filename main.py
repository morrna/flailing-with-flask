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

    return render_template('wall_page.html', pagetitle='Wall', my_wall=my_wall)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template('simple_page.html', pagetitle = '404 error' \
            , content='Sorry, nothing at this URL.') \
            , 404

### Tools etc.
class Wall:
    """
    An object for storing and loading a limited list of messages.
    This will probably need to be updated to work off of the Datastore.
    For now, the messages are not persistent.
    """

    def __init__(self):
        self.max_messages = 12
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)


my_wall = Wall()

