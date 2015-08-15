from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello! This is a personal project owned by Nathan Morrison.' \
				+ '<br>Content is likely to change drastically without warning.' \
				+ '<br><br>What are you doing here, anyway?'

@app.route('/about/')
def about_message():
	with open('static/about_msg.htm','r') as f:
		about_msg_str = f.read()
	
	return about_msg_str

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
