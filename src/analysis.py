import numpy as np


def calculate_average_ratings(rating_matrix):
  average_ratings = np.nanmean(rating_matrix, axis=0)
  return average_ratings