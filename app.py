from flask import Flask, request
from setup_db import db
from flask_restx import Api, Resource
from schemas import movie_schema, movies_schema
from models import Movie, Director, Genre

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}

# связываем контекст с основным приложением
app.app_context().push()

# связываем БД и приложение
db.init_app(app)

api = Api(app)
movie_ns = api.namespace("movies")
director_ns = api.namespace("directors")
genre_ns = api.namespace("genres")


"""Роуты для фильмов"""

@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = Movie.query
        # all_movies = db.session.query(Movie.id, Movie.title, Movie.description, Movie.rating,
        #                              Movie.trailer, Genre.name.label('genre'),
        #                              Director.name.label('director')).join(Genre).join(Director)
        if 'director_id' in request.args:
            did = request.args.get('director_id')
            all_movies = all_movies.filter(Movie.director_id == did)
        if 'genre_id' in request.args:
            gid = request.args.get('genre_id')
            all_movies = all_movies.filter(Movie.genre_id == gid)
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

    def patch(self, mid: int):
        # one_movie = Movie.query.get(mid)
        one_movie = db.session.query(Movie).get(mid)
        if not one_movie:
            return "Нет такого фильма", 404
        req_json = request.json
        if 'title' in req_json:
            one_movie.title = req_json['title']
        elif 'description' in req_json:
            one_movie.description = req_json['description']
        elif 'trailer' in req_json:
            one_movie.trailer = req_json['trailer']
        elif 'year' in req_json:
            one_movie.year = req_json['year']
        elif 'rating' in req_json:
            one_movie.rating = req_json['rating']
        elif 'genre_id' in req_json:
            one_movie.genre_id = req_json['genre_id']
        elif 'director_id' in req_json:
            one_movie.director_id = req_json['director_id']
        db.session.add(one_movie)
        db.session.commit()
        return "", 201

    def put(self, mid: int):
        one_movie = db.session.query(Movie).get(mid)
        if not one_movie:
            return "Нет такого фильма", 404
        req_json = request.json
        one_movie.title = req_json['title']
        one_movie.description = req_json['description']
        one_movie.trailer = req_json['trailer']
        one_movie.year = req_json['year']
        one_movie.rating = req_json['rating']
        one_movie.genre_id = req_json['genre_id']
        one_movie.director_id = req_json['director_id']
        db.session.add(one_movie)
        db.session.commit()
        return "", 201

    def delete(self, mid: int):
        one_movie = db.session.query(Movie).get(mid)
        db.session.delete(one_movie)
        db.session.commit()
        return "", 204


"""Роуты для режисеров"""

@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = Director.query
        return movies_schema.dump(all_directors), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201
    
@director_ns.route('/<int:dir_id>')
class DirectorView(Resource):
    def put(self, dir_id:int):
        dir_update = db.session.query(Director).get(dir_id)
        if not dir_update:
            return "Нет такого режиссера", 404
        req_json = request.json
        dir_update.name = req_json['name']
        db.session.add(dir_update)
        db.session.commit()
        return "", 201

    def delete(self, dir_id:int):
        dir = db.session.query(Director).get(dir_id)
        db.session.delete(dir)
        db.session.commit()
        return "", 204


"""Роуты для жанров"""

@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = Genre.query
        return movies_schema.dump(all_genres), 200

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201

@genre_ns.route('/<int:genre_id>')
class GenreView(Resource):
    def put(self, genre_id: int):
        genre_update = db.session.query(Genre).get(genre_id)
        if not genre_update:
            return "Нет такого жанра", 404
        req_json = request.json
        genre_update.name = req_json['name']
        db.session.add(genre_update)
        db.session.commit()
        return "", 201

    def delete(self, genre_id: int):
        genre = db.session.query(Genre).get(genre_id)
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(port=5000, debug=True)
