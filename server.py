import json
import logging
from flask import Flask, render_template, request, redirect, flash, url_for

logging.basicConfig(level=logging.DEBUG)


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def create_app(config):
    app = Flask(__name__)
    app.config.from_object("config")
    app.config["TESTING"] = config.get("TESTING")

    competitions = loadCompetitions()
    clubs = loadClubs()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def showSummary():
        try:
            club = [club for club in clubs if club['email']
                    == request.form['email']][0]
        except IndexError:
            logging.info("Email not found")
            return render_template('email_not_found.html'), 403
        return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        try:
            foundClub = [c for c in clubs if c['name'] == club][0]
            foundCompetition = [
                c for c in competitions if c['name'] == competition][0]
        except:
            return render_template('404.html'), 404
        if int(foundClub["points"]) <= 0:
            flash(f"Info: you don't have any points for booking!")
            return render_template('welcome.html', club=foundClub, competitions=competitions), 406
        return render_template('booking.html', club=foundClub, competition=foundCompetition)

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        competition = [c for c in competitions if c['name']
                       == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        if placesRequired > int(club['points']):
            flash(f"Error: cannot book more than your available points!")
            return render_template('welcome.html', club=club, competitions=competitions), 406
        competition['numberOfPlaces'] = int(
            competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points']) - placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app


app = create_app({"TESTING": False})

if __name__ == "__main__":
    app.run()
