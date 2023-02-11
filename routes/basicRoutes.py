from flask import Blueprint, render_template, request, redirect

import setup
from algorithms.update import update_orphans, update_init, update_finals, get_statuses_stats
from classes.Status import Status
from classes.Transition import Transition

db = setup.db

basic_routes_handling = Blueprint('basic_routes_handling', __name__)


@basic_routes_handling.route("/", methods=['GET'])
def get_status():

    # packs data as: (Status.name, is_init, is_orphan, is_final)
    status_table = []

    for index in range(len(Status.query.all())):
        status_table += [[Status.query.all()[index].name, False, True, True]]

    # packs data as a list
    transition_table = list(Transition.query.all())

    the_chosen_one: str = request.args.get("theChosenOne", default=None)

    # sets default init status and chosen one, if needed
    if (the_chosen_one is None or the_chosen_one == "") and status_table:
        the_chosen_one = status_table[0][0]

    # update init, orphan and final
    if status_table:
        status_table, init_status_name = update_init(status_table=status_table, new_init_status=the_chosen_one)

        if transition_table:
            update_orphans(database=db, status_table=status_table,
                           init_status_name=init_status_name)

            update_finals(database=db, status_table=status_table)

        status_table = get_statuses_stats(status_table)

    return render_template("homepage.html", status_table=status_table, transition_table=transition_table,
                           status_name=request.args.get("statusName", default=""), theChosenOne=the_chosen_one)


@basic_routes_handling.route("/init", methods=['post'])
def set_init_status():
    return redirect(f"/?theChosenOne={request.form.get('init_status', default='')}")


@basic_routes_handling.route("/status", methods=['post'])
def add_status():
    # checks for duplications
    if db.session.query(Status.name).filter_by(name=request.form['status_name']).first() is None:
        new_status = Status(name=request.form['status_name'])
        db.session.add(new_status)
        db.session.commit()

    return redirect('/')
    # return redirect(f'/?statusName={request.form["status_name"]}&'
    #                 f'theChosenOne={request.args.get("theChosenOne", default="")}')


@basic_routes_handling.route("/status/delete", methods=['post'])
def delete_status():

    status_name = request.form['status_name']

    status = Status.query.filter_by(name=status_name).first()

    if status is not None:
        db.session.delete(status)

        # delete all related transitions
        transition_list = Transition.query.filter_by(from_status=status_name).all()
        transition_list += Transition.query.filter_by(to_status=status_name).all()

        for transition in transition_list:
            db.session.delete(transition)

        db.session.commit()

    # if the init status was deleted, sends nothing
    the_chosen_one = request.args.get("theChosenOne", default="")

    if the_chosen_one == status.name:
        return redirect('/')

    return redirect(f'/?theChosenOne={request.args.get("theChosenOne", default="")}')


@basic_routes_handling.route("/transition", methods=['post'])
def add_transition():

    transition_name = request.form['name']
    transition_from_status = request.form['from_status']
    transition_to_status = request.form['to_status']

    # checks for duplications in all fields
    if db.session.query(Transition.name).filter_by(name=transition_name).first() is None:
        if db.session.query(Transition).filter(Transition.from_status == transition_from_status).first() is None \
                or db.session.query(Transition) \
                .filter(Transition.to_status == transition_name).first() is None:

            if transition_name is not None and transition_name != "":
                # checks if from is different from to
                if transition_from_status != transition_to_status:
                    new_transition = Transition(name=transition_name, to_status=transition_to_status,
                                                from_status=transition_from_status)
                    db.session.add(new_transition)
                    db.session.commit()

    return redirect(f'/?theChosenOne={request.args.get("theChosenOne", default="")}')


@basic_routes_handling.route("/transition/delete", methods=['post'])
def delete_transition():

    transition = Transition.query.filter_by(name=request.form['transition_name']).first()

    if transition is not None:
        db.session.delete(transition)
        db.session.commit()

    return redirect(f'/?theChosenOne={request.args.get("theChosenOne", default="")}')


@basic_routes_handling.route("/reset", methods=['post'])
def reset():

    reset_list = Status.query.all()
    reset_list += Transition.query.all()

    for data in reset_list:
        db.session.delete(data)

    db.session.commit()

    return redirect('/')
