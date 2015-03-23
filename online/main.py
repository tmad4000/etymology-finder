from flask import Flask, render_template, request
import dblookup

app = Flask(__name__)

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def home():
	return render_template('home.html')

# change below
@app.route('/result', methods=['GET'])
def result():
	lang = 'eng'
	query = str(request.args['query'])
	relations = dblookup.load_data('small.tsv')
	origin = dblookup.get_origin(relations, lang + ": " + query, False)
	cousins = dblookup.get_cousins(relations, lang + ": " + query, language=lang)
	return render_template('result.html', query=query, origin=origin, cousins=cousins)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

if __name__ == '__main__':
    app.run()