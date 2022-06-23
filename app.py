from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource
from schemas import movie_schema, movies_schema
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}
db = SQLAlchemy(app)

api = Api(app)
movie_ns = api.namespace("movies")


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = Movie.query.all()
        # all_movies = db.session.query(Movie.id, Movie.title, Movie.description, Movie.rating,
        #                              Movie.trailer, Genre.name.label('genre'),
        #                              Director.name.label('director')).join(Genre).join(Director)
        return movies_schema.dump(all_movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        one_movie = Movie.query.get(mid)
        # one_movie = db.session.query(Movie.id, Movie.title, Movie.description, Movie.rating,
        #                              Movie.trailer, Genre.name.label('genre'),
        #                              Director.name.label('director')).join(Genre).join(Director).filter(
        #     Movie.id == mid).first()
        if not one_movie:
            return "Нет такого фильма", 404
        return movie_schema.dump(one_movie), 200

    def patch(self, mid:int):
        one_movie = Movie.query.get(mid)
        req_json = request.json
        if 'title' in req_json:
            one_movie.title = req_json['title']
        elif 'description' in req_json:
            one_movie.title = req_json['description']
        elif 'trailer' in req_json:
            one_movie.title = req_json['trailer']
        elif 'year' in req_json:
            one_movie.title = req_json['year']
        elif 'rating' in req_json:
            one_movie.title = req_json['rating']
        elif 'genre_id' in req_json:
            one_movie.title = req_json['genre_id']
        elif 'director_id' in req_json:
            one_movie.title = req_json['director_id']
        db.session.add(one_movie)
        db.session.commit()
        return "", 201










if __name__ == '__main__':
    app.run(port=5001, debug=True)
