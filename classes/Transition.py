import setup

db = setup.db


class Transition(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    from_status = db.Column(db.String(255))
    to_status = db.Column(db.String(255))

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f'Transition name is: {self.name}, from: {self.from_status}, to: {self.to_status}'
