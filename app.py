from flask import Flask,render_template,request,redirect,url_for,flash
import requests
from dotenv import load_dotenv
from os import getenv
from pprint import pprint

#make a request to the api.
def make_request(title,num_of_page):

    params = {
        "apikey":getenv("apikey"),
        "s":title,
        "type":"movie",
        "page":num_of_page,
        "plot":"movies"
    }

    data = requests.get(getenv("api_url"),params)
    return data.json()
#get data with the id
def make_request_by_id(movie_id):
    params = {
        "apikey":getenv("apikey"),
        "i":movie_id,
        "type":"movie",
        "plot":"full"
    }
    request = requests.get(getenv("api_url"),params)

    return request.json()


#callback function to sort elements by year
def ByYear(element):
    return element['Year']

def create_app():
    app = Flask(__name__)
    load_dotenv()

    #getting the title.
    @app.route('/',methods=["GET","POST"])
    def index():
        if request.method == "POST":
            movie_title = request.form["input-movie-title"]
            data = make_request(movie_title,1)
            if data['Response'] == 'False':
                flash('Data not found, try again.')
            else:
                return redirect(url_for('gallery',keyword=movie_title,page=1))
        return render_template("base.html")

    
    #Listing all the movies with an especific title
    @app.route('/<string:keyword>/<int:page>',methods=["GET","POST"])
    def gallery(keyword,page):
        data = make_request(keyword, page)

        if request.method == "POST":
            movie_title = request.form["input-movie-title"]
            data = make_request(movie_title,1)
            if data['Response'] == 'False':
                flash('Data not found, try again.')
            else:
                return redirect(url_for('gallery',keyword=movie_title,page=1))
        if not data['Response'] == "False":
            pprint(data)
            num_of_pages = int(int(data['totalResults'])/9)
            movies = data['Search']
            movies.sort(key=ByYear,reverse=True)
            presentation = make_request_by_id(movies.pop(0)['imdbID'])
            return render_template("gallery.html",presentation=presentation,movies=movies,num_of_pages=num_of_pages,keyword=keyword)

        return redirect(url_for('index'))


    #show detail information about an especific movie.

    @app.route('/<string:movieID>',methods=["GET","POST"])
    def showMovie(movieID):
        data = make_request_by_id(movieID)
        

        #converting the string to a list.
        if not data['Response'] == "False":
            data['Actors'] = data['Actors'].split(',')
            data['Writer'] = data['Writer'].split(',')
            data['Director'] = data['Director'].split(',')
        return render_template('movie.html',movie=data)
    return app


