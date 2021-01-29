from flask import Flask, render_template, abort
import requests
import time

api_key = '1fc649858151a2c4dd43a79d6ac7266b'
app = Flask(__name__)

genres_dict = { 28 : "Боевик", 12 : "Приключения", 16 : "Анимация",
35 : "Комедия", 80 : "Криминал", 99 : "Документальный", 18 : "Драма",
10751 : "Семейный", 14 : "Фэнтези", 36 : "История", 27 : "Ужасы",
10402 : "Музыкальный", 9648 : "Детектив", 10749 : "Мелодрама", 878 : "Научная Фантастика",
10770 : "TV Movie", 53 : "Триллер", 10752 : "Военный", 37 : "Вестерн"}


def make_request(api_key, genre, year, page):

	api = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=ru&sort_by=popularity.desc&page={page}&with_original_language=ko&include_video'

	if genre:
		api += f'&with_genres={genre}'
	if year:
		api += f'&primary_release_date.gte={year}-01-01&primary_release_date.lte={year}-12-31'

	time.sleep(1.500)
	r = requests.get(api)
	
	if r.status_code == 200:
		response = r.json()
	else:
		response = None

	return response

@app.route('/',  defaults={'genre': 0, 'year': 0, 'page': 1})
@app.route('/<int:genre>/<int:year>/<int:page>')
def index(genre, year, page):

	response = make_request(api_key, genre, year, page)

	if not response:
		abort(404)
		
	return render_template('index.html',
		response=response,
		genres_dict=genres_dict,
		genre=genre,
		year=year,
		page=page)

@app.errorhandler(404)
def error(error):
	return render_template('404.html'), 404


if __name__ == '__main__':
	app.run()