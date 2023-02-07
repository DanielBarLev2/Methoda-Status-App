from flask import Blueprint, render_template, request, redirect

import setup
from classes.Status import Status
from classes.Transition import Transition

basic_routes_handling = Blueprint('basic_routes_handling', __name__)
db = setup.db


@basic_routes_handling.route("/", methods=['GET'])
def get_status():
    # pull tables
    status_table = list(Status.query.all())

    transition_table = list(Transition.query.all())

    # @todo: add orphan/init/final
    for trans in transition_table:
        pass

    return render_template("homepage.html", status_table=status_table, transition_table=transition_table,
                           status_name=request.args.get("statusName", default=""))


@basic_routes_handling.route("/status", methods=['post'])
def add_status():
    # check for duplications
    if db.session.query(Status.name).filter_by(name=request.form['status_name']).first() is None:
        # create new status
        new_status = Status(name=request.form['status_name'])
        db.session.add(new_status)
        db.session.commit()
        return redirect('/')
    return redirect(f'/?statusName={request.form["status_name"]}')


@basic_routes_handling.route("/status", methods=['DELETE'])
def delete_status():
    # check for duplications
    status = db.session.query(Status.name).filter_by(name=request.form['status_name']).first()
    if status is not None:
        db.session.remove(status)
        db.session.commit()

        return redirect('/')
    return redirect('/')


@basic_routes_handling.route("/transition", methods=['post'])
def add_transition():
    # check for duplications
    if db.session.query(Transition.name).filter_by(name=request.form['name']).first() is None:
        # create new status
        new_transition = Transition(name=request.form['name'], to_status=request.form['to_status'],
                                    from_status=request.form['from_status'])
        db.session.add(new_transition)
        db.session.commit()
        return redirect('/')
    return redirect('/')


@basic_routes_handling.route("/transition", methods=['DELETE'])
def delete_transition():
    # check for duplications
    transition = db.session.query(Transition.name).filter_by(name=request.form['status_name']).first()
    if transition is not None:
        db.session.remove(transition)
        db.session.commit()

        return redirect('/')
    return redirect('/')
