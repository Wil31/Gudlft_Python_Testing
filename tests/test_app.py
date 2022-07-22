from flask import url_for


def test_should_status_code_ok(client):
    response = client.get("/")
    assert response.status_code == 200


def test_should_return_index(client, captured_templates):
    client.get("/")

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "index.html"


def test_login_email(client, captured_templates):
    rv = client.post("showSummary", data=dict(email="john@simplylift.co"))
    assert rv.status_code == 200

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "welcome.html"


def test_login_unknown_email(client, captured_templates):
    rv = client.post("showSummary", data=dict(email="unknown_email@nope.com"))
    assert rv.status_code == 403

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "email_not_found.html"


def test_login_no_email(client, captured_templates):
    rv = client.post("showSummary", data=dict(email=""))
    assert rv.status_code == 403

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "email_not_found.html"


def test_book_status_code_ok(client):
    response = client.get("/book/Spring Festival/Simply Lift")
    assert response.status_code == 200


def test_book_should_return_booking_template(client, captured_templates):
    client.get("/book/Spring Festival/Simply Lift")

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "booking.html"


def test_book_nonexistant_competition_should_404(client):
    response = client.get("/book/nonexistant comp/Simply Lift")
    assert response.status_code == 404


def test_book_nonexistant_competition_should_return_404_template(
    client, captured_templates
):
    client.get("/book/nonexistant comp/Simply Lift")

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "404.html"


def test_book_nonexistant_club_should_404(client):
    response = client.get("/book/Spring Festival/unknownclub")
    assert response.status_code == 404


def test_book_nonexistant_club_should_return_404_template(client, captured_templates):
    client.get("/book/Spring Festival/unknownclub")

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "404.html"


def test_purchase_places(client, captured_templates):
    competition = "Spring Festival"
    club = "Simply Lift"
    club_points = 13
    placesRequired = 2
    pointsRequired = placesRequired * 3
    response = client.post(
        "purchasePlaces",
        data=dict(competition=competition, club=club, places=str(placesRequired)),
    )
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "welcome.html"
    assert context["club"]["points"] == club_points - pointsRequired


def test_purchase_more_places_than_club_points_should_406(client, captured_templates):
    competition = "Spring Festival"
    club = "Simply Lift"
    club_points = 13
    placesRequired = 5
    response = client.post(
        "purchasePlaces",
        data=dict(competition=competition, club=club, places=str(placesRequired)),
    )
    assert response.status_code == 406

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "welcome.html"
    assert int(context["club"]["points"]) == club_points


def test_purchase_more_than_12_places_at_once_should_406(client, captured_templates):
    competition = "Spring Festival"
    club = "Simply Lift"
    club_points = 13
    placesRequired = 13
    response = client.post(
        "purchasePlaces",
        data=dict(competition=competition, club=club, places=str(placesRequired)),
    )
    assert response.status_code == 406

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "welcome.html"
    assert int(context["club"]["points"]) == club_points


def test_purchase_more_than_12_places_in_competition_should_406(
    client, captured_templates
):
    competition = "Spring Festival"
    club = "Test Club"
    placesRequired1 = 7
    placesRequired2 = 6
    response = client.post(
        "purchasePlaces",
        data=dict(competition=competition, club=club, places=str(placesRequired1)),
    )
    assert response.status_code == 200

    response = client.post(
        "purchasePlaces",
        data=dict(competition=competition, club=club, places=str(placesRequired2)),
    )
    assert response.status_code == 406

    assert len(captured_templates) == 2
    template, context = captured_templates[1]
    assert template.name == "welcome.html"
    assert int(context["club"]["points"]) == 79


def test_booking_outdated_comp_should_return_406(client, captured_templates):
    competition = "Fall Classic"
    club = "Simply Lift"
    response = client.get(f"/book/{competition}/{club}")
    assert response.status_code == 406

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "welcome.html"


def test_should_return_clubs_board(client, captured_templates):
    number_of_clubs = 4
    response = client.get("clubsBoard")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "clubs_board.html"
    assert len(context["clubs"]) == number_of_clubs


def test_logout_should_status_code_302(client):
    response = client.get(url_for("logout"))
    assert response.status_code == 302


def test_logout_should_return_index(client):
    response = client.get(url_for("logout"), follow_redirects=True)

    assert response.request.path == url_for("index")
