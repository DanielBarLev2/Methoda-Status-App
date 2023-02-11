from routes.basicRoutes import basic_routes_handling
import setup

app = setup.app
db = setup.db

app.register_blueprint(basic_routes_handling)


# create database table on first launch
@app.before_first_request
def create_tables():
    # creates db in instance
    db.create_all()


if __name__ == '__main__':
    app.run()
