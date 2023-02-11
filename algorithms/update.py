from classes.Transition import Transition


def update_init(status_table: list, new_init_status: str):
    """
    (Status.name, is_init, is_orphan, is_final)
    Sets the first status of the list as an init status.
    :param status_table: list containing statuses and their attributes.
    :param new_init_status: updated init status
    :return: updated status table. In addition, returns init status's name.
    """
    # sets the first status as init
    for index, status in enumerate(status_table):
        if status[0] == new_init_status:
            status_table[index][1] = True
            status_table[index][2] = False
        else:
            status_table[index][1] = False
            status_table[index][2] = True
            status_table[index][2] = True

    return status_table, new_init_status


def update_orphans(database, status_table: list, init_status_name: str, counter: int):
    """
    updates status that have no possible connection or link to init  status. sets orphan True.
    The function is recurring.
    :param database: SQLAlchemy database.
    :param status_table: list containing statuses and their attributes.
    :param init_status_name: the init status, or the latter link.
    :param counter:
    :return:
    """

    transition_list = list(database.session.query(Transition))

    if transition_list:

        for transition in transition_list:

            # finds transition that is linked to init
            if transition.from_status == init_status_name:

                # sets next link and run again
                next_init_status_name = transition.to_status

                if counter > len(status_table):
                    update_orphans(database, status_table, next_init_status_name, counter + 1)

                # sets the orphan value to False
                for index, status in enumerate(status_table):
                    if status[0] == next_init_status_name:
                        status_table[index][2] = False

    # eventually, return the updated list
    return status_table


def update_finals(database, status_table: list, init_status_name: str, counter: int):
    """
    updates status that have no possible connection or link to init status. sets final True.
    The function is recurring.
    :param database: SQLAlchemy database.
    :param status_table: list containing statuses and their attributes.
    :param init_status_name: the init status, or the former link.
    :param counter:
    :return:
    """
    transition_list = list(database.session.query(Transition))

    if transition_list:

        for transition in transition_list:

            # finds transition that is linked to init
            if transition.to_status == init_status_name:

                # sets next link and run again
                prev_init_status_name = transition.from_status

                if counter != len(transition_list):
                    update_finals(database, status_table, prev_init_status_name, counter + 1)

                # sets the orphan value to False
                for index, status in enumerate(status_table):
                    if status[0] == prev_init_status_name:
                        status_table[index][3] = False

    # eventually, return the updated list
    return status_table


# @todo
def get_statuses_stats(status_list: list) -> list:
    """

    :param status_list:
    :return:
    """

    new_status_list = []
    for status in status_list:
        new_status: str = status[0]

        if status[1]:
            new_status += " [INIT]"

        if status[2]:
            new_status += " [ORPHAN]"

        if status[3]:
            new_status += " [FINAL]"

        new_status_list.append([status[0], f'{new_status} '])

    return new_status_list
