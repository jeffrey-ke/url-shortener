from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'lkwbdjflijFLJSadh'

#Home page
@app.route('/')
def home():
    return render_template('home.html')

#Unique-Url page: After clicking 'submit' on the html file, we land here.
@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST': #Ensuring that the home.html page is using the correct retrieval method.
        urls = {} #initializing dictionary for our json storage file

        if os.path.exists('urls.json'): #checking whether a urls.json file exists
            with open('urls.json') as urls_file: #if it does, open it
                urls = json.load(urls_file) #open the json file as a dictionary

        if request.form['code'] in urls.keys(): #if one of the keys matches the user-given code, alert them that the code's been taken
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('home')) #return user to home page

        if 'url' in request.form.keys(): #if the type returned from the home.html page is url, add a url to the urls dictionary
            urls[request.form['code']] = {'url' : request.form['url']}
        else: #if it's anything else than a url, we assume its a file submitted.
            f = request.files['file'] #temporarily store a file in f
            full_name = request.form['code'] + secure_filename(f.filename) #we're going to get save the file with a different name
            f.save('/Users/jeffk/Documents/GitHub/url-shortener/' + full_name) #saving it in our project directory
            urls[request.form['code']] = {'file':full_name}#updating dictionary

        with open('urls.json', 'w') as url_file: #open our json storage file
            json.dump(urls, url_file) #overwrite previous json data with updated urls dictionary
        return render_template('your_url.html', code=request.form['code']) #direct user to their unique url page
    else:
        return redirect(url_for('home')) #if the incorrect retrival message was used.
