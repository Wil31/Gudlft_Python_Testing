from tests.conftest import client, captured_templates


def test_should_status_code_ok(client):
    response = client.get("/")
    assert response.status_code == 200


def test_should_return_index(client, captured_templates):
    response = client.get("/")

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "index.html"


def test_login_email(client, captured_templates):
    rv = client.post(
        "showSummary", data=dict(email="john@simplylift.co")
    )
    assert rv.status_code == 200

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "welcome.html"


def test_login_unknown_email(client, captured_templates):
    rv = client.post(
        "showSummary", data=dict(email="unknown_email@nope.com")
    )
    assert rv.status_code == 403

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "email_not_found.html"


def test_login_no_email(client, captured_templates):
    rv = client.post(
        "showSummary", data=dict(email="")
    )
    assert rv.status_code == 403

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "email_not_found.html"


def test_book_status_code_ok(client):
    response = client.get("/book/Spring Festival/Simply Lift")
    assert response.status_code == 200


def test_book_should_return_booking_template(client, captured_templates):
    response = client.get("/book/Spring Festival/Simply Lift")

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "booking.html"


def test_purchase_places(client, captured_templates):
    competition = "Spring Festival"
    club = "Simply Lift"
    club_points = 13
    placesRequired = 2
    response = client.post(
        "purchasePlaces", data=dict(competition=competition,
                                    club=club,
                                    places=str(placesRequired))
    )
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "welcome.html"
    assert context['club']['points'] == club_points - placesRequired


def test_purchase_more_places_than_club_points_should_406(client, captured_templates):
    competition = "Spring Festival"
    club = "Simply Lift"
    club_points = 13
    placesRequired = 14
    response = client.post(
        "purchasePlaces", data=dict(competition=competition,
                                    club=club,
                                    places=str(placesRequired))
    )
    assert response.status_code == 406

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "welcome.html"
    assert int(context['club']['points']) == club_points
