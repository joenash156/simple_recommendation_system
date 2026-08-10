import numpy as np


# a function to recommend books to a target user based on the ratings of similar users
def recommend_books(
  rating_matrix,
  item_names,
  similar_users: list[tuple[int, float]],
  target_user_index: int,
  min_rating: int = 4,
) -> list[tuple[str, int, float]]:
  # get the ratings of the target user
  target_user_ratings = rating_matrix[target_user_index]

  recommendations = []

  # iterate through the similar users and their distances
  for user_index, distance in similar_users:
    # get the ratings of the similar user
    similar_user = rating_matrix[user_index]

    # iterate through the items and their ratings for the similar user
    for item_index, rating in enumerate(similar_user):
      # if the target user has not rated the item and the similar user's rating is above the minimum rating
      if np.isnan(target_user_ratings[item_index]) and rating >= min_rating:
        # add the item name, rating, and distance to the recommendations list
        recommendations.append((item_names[item_index], rating, distance))

  return recommendations
  
def recommend_book(recommendations):
  return recommendations[0] if recommendations else None

