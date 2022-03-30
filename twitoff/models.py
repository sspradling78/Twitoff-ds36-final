from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()


class User(DB.Model):
    '''For getting our user and inputing user
       into our database.'''
    id = DB.Column(DB.BigInteger, primary_key=True)
    username = DB.Column(DB.String, nullable=False)

    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f"<User: {self.username}>"


class Tweet(DB.Model):
    '''Gathering the tweets of the user in our database.
       Also, getting the vectors of those tweets and
       loading them into our database for comparisions.'''
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'),
                        nullable=False)

    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    vect = DB.Column(DB.PickleType, nullable=False)

    def __repr__(self):
        return f"<Tweet: {self.text}>"
