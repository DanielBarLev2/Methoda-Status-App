from classes.Transition import Transition


def update_init(status_table: list):
    """
    Sets the first status of the list as an init status.
    :param status_table:
    :return: updated status table. In addition, returns init status's name.
    """
    # sets the first status as init
    if status_table:
        status_table[0][1] = True
        status_table[0][2] = False
        init_status = status_table[0][0]

        return status_table, init_status


def update_orphans(database, status_table: list, init_status_name: str):
    """

    :param database:
    :param status_table:
    :param init_status_name:
    :return:
    """
    if database.session.query(Transition)\
            .filter(Transition.from_status == init_status_name).first() is not None:

        # finds init status
        from_status_name = database.session.query(Transition)\
            .filter(Transition.from_status == init_status_name).first().from_status

        if from_status_name:
            # finds the next link to init
            if from_status_name == init_status_name:
                # check if next exist
                if database.session.query(Transition)\
                        .filter(Transition.from_status == init_status_name).first().to_status:
                    # sets the next chain in the link
                    next_init_status_name = database.session.query(Transition)\
                        .filter(Transition.from_status == init_status_name).first().to_status

                    # algorithms the orphan value
                    for index, status in enumerate(status_table):
                        if status[0] == next_init_status_name:
                            status_table[index][2] = False

                    return update_orphans(database=database, status_table=status_table,
                                          init_status_name=next_init_status_name)

    # eventually, return the updated list
    return status_table


