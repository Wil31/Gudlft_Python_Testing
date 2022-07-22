import json
import logging
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def check_outdated_competitions(competitions):
    now = datetime.today()
    for competition in competitions:
        if competition["date_time_obj"] < now:
            competition["outdated"] = True
        else:
            competition["outdated"] = False


def create_app(config):
    app = Flask(__name__)
    app.config.from_object("config")
    app.config["TESTING"] = config.get("TESTING")

    competitions = loadCompetitions()
    clubs = loadClubs()

    for competition in competitions:
        comp_date_time = competition["date"]
        competition["date_time_obj"] = datetime.strptime(
            comp_date_time, "%Y-%m-%d %H:%M:%S"
        )

    check_outdated_competitions(competitions)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/showSummary", methods=["POST"])
    def showSummary():
        try:
            club = [club for club in clubs if club["email"] == request.form["email"]][0]
        except IndexError:
            logging.info("Email not found")
            return render_template("email_not_found.html"), 403
        check_outdated_competitions(competitions)
        return render_template("welcome.html", club=club, competitions=competitions)

    @app.route("/book/<competition>/<club>")
    def book(competition, club):
        try:
            foundClub = [c for c in clubs if c["name"] == club][0]
            foundCompetition = [c for c in competitions if c["name"] == competition][0]
        except IndexError:
            return render_template("404.html"), 404

        if foundCompetition["outdated"] is True:
            flash("Info: cannot book a past competition!")
            return (
                render_template(
                    "welcome.html", club=foundClub, competitions=competitions
                ),
                406,
            )
        elif int(foundClub["points"]) <= 0:
            flash("Info: you don't have any points for booking!")
            return (
                render_template(
                    "welcome.html", club=foundClub, competitions=competitions
                ),
                406,
            )

        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )

    @app.route("/purchasePlaces", methods=["POST"])
    def purchasePlaces():
        competition = [
            c for c in competitions if c["name"] == request.form["competition"]
        ][0]
        club = [c for c in clubs if c["name"] == request.form["club"]][0]
        placesRequired = int(request.form["places"])
        pointsRequired = placesRequired * 3

        if pointsRequired > int(club["points"]):
            flash("Error: cannot book more than your available points!")
            return (
                render_template("welcome.html", club=club, competitions=competitions),
                406,
            )

        if placesRequired > 12:
            flash("Error: cannot book more than 12 places!")
            return (
                render_template("welcome.html", club=club, competitions=competitions),
                406,
            )

        if club["name"] in competition:
            if competition[club["name"]] + placesRequired > 12:
                flash("Error: cannot book more than 12 places per competition!")
                return (
                    render_template(
                        "welcome.html", club=club, competitions=competitions
                    ),
                    406,
                )
            competition[club["name"]] += placesRequired
        else:
            competition[club["name"]] = placesRequired

        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
        club["points"] = int(club["points"]) - pointsRequired
        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)

    @app.route("/clubsBoard")
    def clubsBoard():
        return render_template("clubs_board.html", clubs=clubs)

    @app.route("/logout")
    def logout():
        return redirect(url_for("index"))

    return app


app = create_app({"TESTING": False})

if __name__ == "__main__":
    app.run()
