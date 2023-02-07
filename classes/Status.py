import setup

db = setup.db


class Status(db.Model):
    name = db.Column(db.String(255), primary_key=True)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f'Status name is: {self.name}'