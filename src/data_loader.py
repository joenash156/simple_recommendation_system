"""
Data loader for handling rating data from a CSV file.
"""

import pandas as pd


# a function to load ratings from a CSV file and return the user names, item names, and rating matrix
def load_ratings(filepath):
  # load ratings from a CSV file
  ratings = pd.read_csv(filepath)
  # convert the ratings to a numpy array
  user_names = ratings["User"].to_numpy()

  # drop the "User" column and convert the remaining columns to a numpy array
  rating_matrix = ratings.drop(columns=["User"]).to_numpy(dtype=float)
  # get the item names from the columns of the ratings dataframe
  item_names = ratings.drop(columns=["User"]).columns.to_numpy()

  # return the user names, item names, and rating matrix
  return user_names, item_names, rating_matrix