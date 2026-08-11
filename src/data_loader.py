"""
Data loader for handling rating data from a CSV file.
"""

#import numpy as np
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

# returns users who have at least one unrated movie (NaN) in their vector.
# def get_inactive_users(rating_matrix, user_names):
#   # Convert user_names to NumPy array to safely support boolean indexing
#   user_names = np.array(user_names)
  
#   # Create a boolean mask: True for rows with AT LEAST ONE NaN
#   has_nan_mask = np.isnan(rating_matrix).any(axis=1)
  
#   # Return user names matching the mask
#   return user_names[has_nan_mask]