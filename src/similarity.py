"""
This module provides a function to compute the Euclidean distance between two users based on their ratings.
The Euclidean distance is a measure of similarity between two users, where a smaller distance indicates greater similarity.
"""

import numpy as np


# a function to compute the Euclidean distance between two users based on their ratings
def euclidean_distance(user_a, user_b):
  # create a mask to filter out NaN values from both users' ratings
  mask = ~np.isnan(user_a) & ~np.isnan(user_b)

  # compute the differences between the ratings of the two users for the items they both rated
  differences = user_a[mask] - user_b[mask]
  
  # compute the squared differences and sum them up
  squared_differences = differences ** 2
  
  # take the square root to get the Euclidean distance
  distance = np.sqrt(np.sum(squared_differences))

  return distance


# a function to find similar users based on the Euclidean distance
def find_similar_users(rating_matrix, user_index):
  # get the ratings of the target user
  target_user = rating_matrix[user_index]

  # store the distances between the target user and all other users
  distances = []

  # iterate through all users in the rating matrix
  for index, user in enumerate(rating_matrix):
    # skip the target user itself
    if index == user_index:
      continue
    
    # # get only top 5
    # if index == 5:
    #   break
    
    # compute the Euclidean distance between the target user and the current user
    distance = euclidean_distance(target_user, user)

    distances.append((index, distance))

  # sort the distances in ascending order based on the distance value
  distances.sort(key=lambda x: x[1])

  return distances