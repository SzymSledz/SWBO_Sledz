from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from swbo import db
from swbo.models import users, calendarEvent
from datetime import datetime

calendar = Blueprint('calendar', __name__)


@calendar.route("/calendar", methods=["GET", "POST"])
def calendar_page():
    if "logged_in" not in session:
        return redirect(url_for("user.login_page"))

    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        description = request.form.get("description", "")
        user_id = users.query.filter_by(login=session['login']).first().id

        new_event = calendarEvent(title=title, date=datetime.strptime(date, '%Y-%m-%d'), description=description,
                                  user_id=user_id)
        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for("calendar.calendar_page"))

    else:  # method == GET
        login_in_session = session["login"]
        user_id = users.query.filter_by(login=login_in_session).first().id
        user_events = calendarEvent.query.filter_by(user_id=user_id).all()

        events = []
        for event in user_events:
            events.append({
                'id': event.id,
                'title': event.title,
                'start': event.date.strftime('%Y-%m-%d'),
                'description': event.description,
            })

        return render_template("calendar.html", events=events)


@calendar.route("/delete_event/<event_id>", methods=["DELETE"])
def delete_event(event_id):
    if "logged_in" not in session:
        return redirect(url_for("user.login_page"))

    event = calendarEvent.query.filter_by(id=event_id).first()
    if event and event.user_id == users.query.filter_by(login=session['login']).first().id:
        db.session.delete(event)
        db.session.commit()
        return '', 204

    return '', 403


@calendar.route("/add_event", methods=["GET", "POST"])
def add_event():
    if "logged_in" not in session:
        return redirect(url_for("user.login_page"))

    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        description = request.form.get("description", "")
        user_id = users.query.filter_by(login=session['login']).first().id

        new_event = calendarEvent(title=title, date=datetime.strptime(date, '%Y-%m-%d'), description=description,
                                  user_id=user_id)
        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for("calendar.calendar_page"))

    date = request.args.get("date")
    return render_template("event_form.html", form_title="Dodaj Wydarzenie", form_action=url_for("calendar.add_event"),
                           event=None, date=date, button_text="Dodaj")


@calendar.route("/edit_event/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    if "logged_in" not in session:
        return redirect(url_for("user.login_page"))

    event = calendarEvent.query.filter_by(id=event_id).first()

    if request.method == "POST":
        event.title = request.form["title"]
        event.date = datetime.strptime(request.form["date"], '%Y-%m-%d')
        event.description = request.form.get("description", "")
        db.session.commit()
        return redirect(url_for("calendar.calendar_page"))

    return render_template("event_form.html", form_title="Edytuj Wydarzenie",
                           form_action=url_for("calendar.edit_event", event_id=event_id), event=event,
                           date=event.date.strftime('%Y-%m-%d'), button_text="Zapisz zmiany")