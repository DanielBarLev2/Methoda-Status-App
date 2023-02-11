from algorithms.update import update_orphans, update_init, update_finals, get_statuses_stats
from flask import Blueprint, render_template, request, redirect
from classes.Transition import Transition
from classes.Status import Status

import setup

basic_routes_handling = Blueprint('basic_routes_handling', __name__)
db = setup.db


@basic_routes_handling.route("/", methods=['GET'])
def get_status():
    # packs data as: (Status.name, is_init, is_orphan, is_final)
    status_table = []

    for index in range(len(Status.query.all())):
        status_table += [[Status.query.all()[index].name, False, True, True]]

    # packs data as a list
    transition_table = list(Transition.query.all())

    # update init, orphan and final
    if status_table:
        status_table, init_status_name = update_init(status_table=status_table, new_init_status=status_table[0][0])

        if transition_table:
            update_orphans(database=db, status_table=status_table,
                           init_status_name=init_status_name, counter=1)

            update_finals(database=db, status_table=status_table,
                          init_status_name=init_status_name, counter=1)

        status_table = get_statuses_stats(status_table)

    return render_template("homepage.html", status_table=status_table, transition_table=transition_table,
                           status_name=request.args.get("statusName", default=""))


# @todo: radio input is not working
@basic_routes_handling.route("/init", methods=['post'])
def set_init_status():
    return


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


@basic_routes_handling.route("/status/delete", methods=['post'])
def delete_status():
    # delete status
    status = Status.query.filter_by(name=request.form['status_name']).first()
    if status is not None:
        db.session.delete(status)
        db.session.commit()

        # delete all related transitions
        transition_list = Transition.query.filter_by(from_status=request.form['status_name']).all()
        transition_list += Transition.query.filter_by(to_status=request.form['status_name']).all()

        for transition in transition_list:
            db.session.delete(transition)

        db.session.commit()

        return redirect('/')
    return redirect('/')


@basic_routes_handling.route("/transition", methods=['post'])
def add_transition():
    # checks for duplications in all fields
    if db.session.query(Transition.name).filter_by(name=request.form['name']).first() is None:
        if db.session.query(Transition).filter(Transition.from_status == request.form['from_status']).first() is None \
                or db.session.query(Transition).filter(Transition.to_status == request.form['to_status']).first() \
                is None:
            # create new status
            if request.form['name'] is not None and request.form['name'] != "":
                new_transition = Transition(name=request.form['name'], to_status=request.form['to_status'],
                                            from_status=request.form['from_status'])
                db.session.add(new_transition)
                db.session.commit()
                return redirect('/')
    return redirect('/')


@basic_routes_handling.route("/transition/delete", methods=['post'])
def delete_transition():
    # check for duplications
    transition = Transition.query.filter_by(name=request.form['transition_name']).first()
    if transition is not None:
        db.session.delete(transition)
        db.session.commit()

        return redirect('/')
    return redirect('/')


@basic_routes_handling.route("/reset", methods=['post'])
def reset():

    reset_list = Status.query.all()
    reset_list += Transition.query.all()

    for data in reset_list:
        db.session.delete(data)

    db.session.commit()

    return redirect('/')
