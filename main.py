from flask import Flask, abort, render_template, url_for, jsonify, session, request, flash, redirect
from data import queries
from time import gmtime
import math
import json
import util
from dotenv import load_dotenv
from os import urandom
from flask_cors import CORS

load_dotenv()
app = Flask('codecool_series')
CORS(app)
NUM_MOST_RATED = 15
app.secret_key = urandom(16)

SESSION_USERNAME = "username"
SESSION_PASSWORD = "password"




@app.route('/')
def index():

    shows = queries.get_shows()
    username= session.get(SESSION_USERNAME)

    return render_template('index.html', shows=shows, username=username)


@app.route('/design')
def design():
    return render_template('design.html')




@app.route('/shows/most-rated/<next_page>')
@app.route('/shows/most-rated')
@app.route('/shows/<next_page>')
@app.route('/shows')
def get_most_rated(next_page=1):


    sort_by = request.args.get('sort_by')
    direction = request.args.get('direction')
    if sort_by == None:
        sort_by = 'rating'
    if direction == None:
        direction = 'DESC'


    current_page = int(next_page)
    offset = NUM_MOST_RATED * current_page - NUM_MOST_RATED
    limit = NUM_MOST_RATED
    most_rated = queries.get_most_rated_shows(offset,limit, sort_by, direction)

    if direction == 'DESC':
        new_direction = 'ASC'
    elif direction == 'ASC':
        new_direction = 'DESC'

    maximum = int(queries.get_number_of_shows()) // NUM_MOST_RATED + 1

    username = session.get(SESSION_USERNAME)

    return render_template('most_rated.html', most_rated=most_rated,
                               current_page=current_page, max=maximum,
                               sort_by=sort_by, direction=direction,
                               new_direction=new_direction,
                               username=username)


@app.route('/show/<id>')
def show_show(id):
    show = queries.get_show_by_id(id)
    actors = queries.get_actors_for_show(id)
    seasons = queries.get_seasons_by_show_id(id)

    username = session.get(SESSION_USERNAME)

    return render_template('show.html', show=show, actors=actors,
                           seasons=seasons, username=username)


@app.route('/episodes/<season_id>')
def episodes(season_id):

    episodes_for_season = queries. get_episodes(season_id)
    username= session.get(SESSION_USERNAME)
    return render_template('episode.html', episodes=episodes_for_season,
                           username=username)




@app.route('/register', methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form.get(SESSION_USERNAME)
        password = request.form.get(SESSION_PASSWORD)
        if username == "" or password == "":
            flash("Please, fill in both fields.")
            return redirect(url_for('index'))
        if not queries.check_username(username):
            hash_pass = util.hash_password_salt(password)
            queries.register(username, hash_pass)
            flash("Successful registration. Log in to continue.")
            return redirect(url_for('index'))

        else:
            flash("Try again")
            return redirect(url_for('index'))


@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get(SESSION_USERNAME)
        password = request.form.get(SESSION_PASSWORD)
        if username == "" or password == "":
            flash("Please, fill in both fields.")
            return redirect(url_for('index'))

        if queries.check_username(username):
            stored_pass = queries.get_password(username)[SESSION_PASSWORD]
            if util.verify_psswd(password, stored_pass):
                session[SESSION_USERNAME] = username
                flash("Logged as: ")
                return redirect(url_for('index'))
        flash("Wrong username or password.")
        return redirect(url_for('index'))

    else:
        flash("Try again")
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    if session.get(SESSION_USERNAME):
        session.pop(SESSION_USERNAME)
    return redirect(url_for('index'))


@app.route('/get-shows')
def get_shows():
    shows = queries.get_shows()
    return jsonify(shows)

@app.route('/get-seasons/<show_id>')
def get_seasons(show_id):
    seasons = queries.get_seasons_by_show_id(int(show_id))
    return jsonify(seasons)


@app.route('/get-episodes/<season_id>')
def get_episodes(season_id):
    episodes = queries.get_episodes(season_id)
    return jsonify(episodes)

@app.route('/get-episode-length/<episode_id>')
def get_episode_length(episode_id):
    length = queries.get_episode_length(episode_id)
    return jsonify(length)


@app.route('/actor/<actor_id>')
def get_actor_details(actor_id):
    details = queries.get_actor_details(actor_id)
    if details == None:
        return jsonify( {"status" : "wrong_id"})
        # abort(404)
    return jsonify(details)


@app.route('/actors/genres/<actor_id>')
def get_actor_genres(actor_id):
    genres = queries.get_actor_genres(actor_id)
    return jsonify(genres)


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
