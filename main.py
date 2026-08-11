"""
This is the main entry point for the recommendation system. It loads the rating data and displays the users, items, rating matrix, etc.
"""

from config import RATING_CSV_PATH
from src.analysis import calculate_average_ratings
from src.data_loader import load_ratings
from src.recommender import recommend_book, recommend_books
from src.similarity import find_similar_users
from src.visualization import plot_average_ratings

users, items, ratings = load_ratings(RATING_CSV_PATH)

# useful functions to perform operations

# function to print all users
def print_users():
  print()
  print("Check out all users and their indexes")
  print("-------------------------------------")

  for i, user in enumerate(users):
    print(f"{i}: {user}")
    
  print()
  
# function to get recommendations for a target user
def get_recommendations_for_user(user_index):  
  target_user_index = user_index

  similar_users = find_similar_users(ratings, target_user_index)

  target_user_name = users[target_user_index]

  print()

  print(f"Similar users to {target_user_name}")
  print("----------------------")

  for index, distance in similar_users:
    print(f"{users[index]}: {distance:.3f}")


  recommendations = recommend_books(
    ratings,
    items,
    similar_users,
    target_user_index
  )

  print(f"\nBook recommendations for {target_user_name}")
  print("-----------------------------")


  if len(recommendations) > 0:
    for book, rating, distance in recommendations:
      print(
        f"{book} "
        f"(rated {rating:.1f}/5 by a similar user, "
        f"distance: {distance:.3f})"
      )
  else:
    print(f"{target_user_name} has read all the books and has no new recommendations.")

# function to get the best book recommendation for a target user
def get_best_recommendation_for_user(target_user_name, recommendations):
  best_recommendation = recommend_book(recommendations)

  print(f"\nBest book recommendation for {target_user_name}:")
  if best_recommendation:
    book, rating, distance = best_recommendation
    print(
      f"{book} "
      f"(rated {rating:.1f}/5 by a similar user, "
      f"distance: {distance:.3f})"
    )
  else:
    print(f"{target_user_name} has read all the books and does not need any recommendations.")

# function to calculate and print the average ratings for all books
def print_average_ratings():
  average_ratings = calculate_average_ratings(ratings)

  print()
  print("Average rating for each book")
  print("----------------------------")

  for book, average in zip(items, average_ratings):
    print(f"{book}: {average:.2f}/5")


print()

print("WELCOME TO THE BOOK RECOMMENDATION SYSTEM")
print("------------------------------------------")

print()

operations = [
  "1. Get recommendations for a user",
  "2. Get the best book recommendation for a user",
  "3. Get average ratings for all books",
  "4. Plot average ratings for all books",
  "5. Exit"
  ]

for operation in operations:
  print(operation)

print()

operation = int(input("Enter an operation to perform: "))

print()

while operation != 5:
  if operation == 1:
    print_users()
    user_index = int(input("Enter the index of the target user: "))
    get_recommendations_for_user(user_index)
    
  elif operation == 2:
    print_users()
    user_index = int(input("Enter the index of the target user: "))
    similar_users = find_similar_users(ratings, user_index)
    recommendations = recommend_books(
      ratings,
      items,
      similar_users,
      user_index
    )
    get_best_recommendation_for_user(users[user_index], recommendations)
    
  elif operation == 3:
    print_average_ratings()
    
  elif operation == 4:
    average_ratings = calculate_average_ratings(ratings)
    plot_average_ratings(items, average_ratings)
    
  else:
    print("Invalid operation. Please try again.")

  print()

  for operation in operations:
    print(operation)

  print()

  operation = int(input("Enter an operation to perform: "))

print()