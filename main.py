from flask import Flask, render_template
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template("front_door.html")

@app.route('/about/')
def about_message():
	with open('content/about_msg.htm','r') as f:
		about_msg_str = f.read()
	
	return about_msg_str

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
