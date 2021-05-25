#Required imports
import os
import firebase_admin
from flask import redirect,Flask,render_template, request, session, url_for, make_response
import firebase_admin
from firebase_admin import db
import urllib.request
from PIL import Image
import img2pdf
# import pyrebase
#Initialize Flask app
app = Flask(__name__)
app.secret_key = "super secret key"

cred_object = firebase_admin.credentials.Certificate('key.json')
default_app = firebase_admin.initialize_app(cred_object, { 'databaseURL' : 'https://owasp-test-855b8-default-rtdb.firebaseio.com/' })




@app.route("/Data",methods=["POST"])
def Data():
    if request.method=="POST":
        dis_id = request.form.get("dis_id",False)
    ref = db.reference("/Data")
    everyone = ref.get()
    for i in everyone:
    	if ( everyone[i]['Discord'] == dis_id):
    		session.clear()
    		session['name'] = everyone[i]['Name']
    		session['discord'] = everyone[i]['Discord']
    		return redirect(url_for('secondpage'))
    error = "INVALID DISCORD USERNAME"
    return render_template('index.html', error = error)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/secondpage")
def secondpage():
    print(session['discord'])
    user = {}
    user['name'] = session['name']
    user['discord'] = session['discord']
    user['year'] = []
    user['url'] = []
    baseurl = "https://storage.googleapis.com/owasp-test-855b8.appspot.com/dynamic%20certificate/"
    ref = db.reference('/Certificates')
    everyone = ref.get()
    for i in everyone:
    	if user['discord'] == i:
	    	for j in everyone[i]:
    			year = everyone[i][j]['Year']
    			user['year'].append(year)
    			url = baseurl + user['discord'] + "-" + everyone[i][j]['Year']
    			user['url'].append(url)
    return render_template('secondpage.html', user = user)

@app.route("/Certificate", methods=["POST", "GET"])
def landingpage():
    if request.method == "POST":
    	url = request.form.get("url")
    	a = urllib.request.urlretrieve(url)
    	image = Image.open(a[0])
    	pdf_bytes = img2pdf.convert(image.filename)
    	response = make_response(pdf_bytes)
    	response.headers['Content-Type'] = 'application/pdf'
    	response.headers['Content-Disposition'] = 'inline; filename=Certificate.pdf'
    	return response
    return render_template('Certificate.html')
    

if __name__ == "__main__":
    app.run(debug=True)
