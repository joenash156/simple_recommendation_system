"""
This is the main entry point for the recommendation system. It loads the rating data and displays the users, items, rating matrix, etc.
"""

from config import RATING_CSV_PATH
from src.analysis import calculate_average_ratings
from src.data_loader import load_ratings
from src.recommender import recommend_book, recommend_books
from src.similarity import euclidean_distance, find_similar_users
from src.visualization import plot_average_ratings

users, items, ratings = load_ratings(RATING_CSV_PATH)

print("Users:")
print(users)

print("\nItems:")
print(items)

print("\nRating Matrix:")
print(ratings)

print("\nMatrix Shape:")
print(ratings.shape)

print()

alice = ratings[0]
bob = ratings[1]

distance = euclidean_distance(alice, bob)

print("Alice:", alice)
print("Bob:", bob)
print("Euclidean distance:", distance)

print()

target_user_index = 0

similar_users = find_similar_users(ratings, target_user_index)

target_user_name = users[target_user_index]

print(f"Similar users to {target_user_name}:")

for index, distance in similar_users:
  print(f"{users[index]}: {distance:.3f}")


recommendations = recommend_books(
  ratings,
  items,
  similar_users,
  target_user_index
)

print(f"\nBook recommendations for {target_user_name}:")

for book, rating, distance in recommendations:
  print(
    f"{book} "
    f"(rated {rating:.1f}/5 by a similar user, "
    f"distance: {distance:.3f})"
  )

# recommend the best book for the target user
best_recommendation = recommend_book(recommendations)

print(f"\nBest book recommendation for {target_user_name}:")
if best_recommendation:
  book, rating, distance = best_recommendation
  print(
    f"{book} "
    f"(rated {rating:.1f}/5 by a similar user, "
    f"distance: {distance:.3f})"
  )

print()

# calculate the average ratings for each book
average_ratings = calculate_average_ratings(ratings)

print("\nAverage rating for each book:")

for book, average in zip(items, average_ratings):
  print(f"{book}: {average:.2f}/5")


plot_average_ratings(items, average_ratings)

print()