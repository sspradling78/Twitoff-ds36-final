from os import getenv
from flask import Flask, render_template, request
from .predict import predict_user
from .models import DB, User
from .twitter import add_or_update_user


def create_app():
    '''The flow of our twitoff app and all the pages that we
       are routing to.'''

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    # Create a route for the home page.
    @app.route("/")
    def home():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    # Create a route for the reset page.
    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset DB')

    # Create a route for the update page.
    @app.route("/update")
    def update():
        usernames = [user.username for user in User.query.all()]
        for username in usernames:
            add_or_update_user(username)
        return render_template('base.html', title='Updating Users')

    # Create a route for populating users for testing purposes.
    # @app.route("/populate")
    # def populate():
    #     add_or_update_user('nasa')
    #     add_or_update_user('austen')
    #     add_or_update_user('ryanallred')
    #     add_or_update_user('SVogt1229')
    #     add_or_update_user('Athletics')
    #     add_or_update_user('RiffsAndBeards')
    #     return render_template('base.html', title='Populate')

    # Create a route for adding a user to our database for comparisions.
    @app.route('/user', methods=["POST"])
    @app.route('/user/<name>', methods=["GET"])
    def user(name=None, message=''):

        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} Succesfully added!".format(name)

            tweets = User.query.filter(User.username == name).one().tweets

        except Exception as e:
            message = "Error adding {}: {}".format(name, e)

            tweets = []

        return render_template(
            "user.html",
            title=name,
            tweets=tweets,
            message=message)

    # Create a route for the final comparing page with results.
    @app.route('/compare', methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values["user1"]])

        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            prediction = predict_user(
                user0, user1, request.values["tweet_text"])
            message = "'{}' is more likely to be said by {} than {}!".format(
                request.values["tweet_text"],
                user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template(
            'prediction.html',
            title="Prediction",
            message=message)

    return app
