import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    '''Determines which of two users would more likly say
       the inserted tweet. This is where we are fitting
       our model to get our predictions.'''

    # Getting the users from the Database who we want to compare.
    user0 = User.query.filter(User.username == user0_name).one()
    user1 = User.query.filter(User.username == user1_name).one()

    # Getting the tweet vectors of each users tweets.
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Vertically stacking the vectors on top of one another
    # to make a single array.
    vects = np.vstack([user0_vects, user1_vects])
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    # Fitting(Train) the model to predict outcome.
    log_reg = LogisticRegression().fit(vects, labels)

    # Vectorizing the hypothetical tweet.
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # Return prediction result.
    return log_reg.predict([hypo_tweet_vect])
