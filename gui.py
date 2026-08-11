"""
PyQt6 desktop interface for the book recommendation system.

Wraps the existing src/ modules (data_loader, similarity, recommender,
analysis) in a graphical front end instead of the console menu in main.py.
"""

import sys

import numpy as np
from matplotlib import cm
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import (
  QApplication,
  QComboBox,
  QHBoxLayout,
  QHeaderView,
  QLabel,
  QListWidget,
  QMainWindow,
  QMessageBox,
  QPushButton,
  QTableWidget,
  QTableWidgetItem,
  QTabWidget,
  QVBoxLayout,
  QWidget,
)

from config import RATING_CSV_PATH
from src.analysis import calculate_average_ratings
from src.data_loader import load_ratings
from src.recommender import recommend_book, recommend_books
from src.similarity import find_similar_users


class RecommendationsTab(QWidget):
  def __init__(self, users, items, ratings):
    super().__init__()
    self.users = users
    self.items = items
    self.ratings = ratings

    layout = QVBoxLayout(self)

    self.get_button = QPushButton("Get Recommendations")
    self.get_button.clicked.connect(self.show_recommendations)
    layout.addWidget(self.get_button)

    self.best_label = QLabel("Select a user and click “Get Recommendations”.")
    self.best_label.setWordWrap(True)
    self.best_label.setStyleSheet(
        "font-weight: bold; padding: 8px; background: #03573f; border-radius: 4px;"
    )
    layout.addWidget(self.best_label)

    lists_layout = QHBoxLayout()

    similar_column = QVBoxLayout()
    similar_column.addWidget(QLabel("Similar users"))
    self.similar_list = QListWidget()
    similar_column.addWidget(self.similar_list)
    lists_layout.addLayout(similar_column)

    rec_column = QVBoxLayout()
    rec_column.addWidget(QLabel("Recommended books"))
    self.rec_table = QTableWidget(0, 3)
    self.rec_table.setHorizontalHeaderLabels(["Book", "Rating", "Distance"])
    self.rec_table.horizontalHeader().setSectionResizeMode( # type: ignore
        0, QHeaderView.ResizeMode.Stretch
    )
    self.rec_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    rec_column.addWidget(self.rec_table)
    lists_layout.addLayout(rec_column, stretch=2)

    layout.addLayout(lists_layout)

  def show_recommendations(self):
    user_index = self.window().selected_user_index() # type: ignore
    if user_index is None:
      return

    target_user_name = self.users[user_index]
    similar_users = find_similar_users(self.ratings, user_index)

    self.similar_list.clear()
    for index, distance in similar_users:
      self.similar_list.addItem(f"{self.users[index]}  ({distance:.3f})")

    recommendations = recommend_books(
      self.ratings, self.items, similar_users, user_index
    )

    self.rec_table.setRowCount(0)
    for book, rating, distance in recommendations:
      row = self.rec_table.rowCount()
      self.rec_table.insertRow(row)
      self.rec_table.setItem(row, 0, QTableWidgetItem(str(book)))
      self.rec_table.setItem(row, 1, QTableWidgetItem(f"{rating:.1f}/5"))
      self.rec_table.setItem(row, 2, QTableWidgetItem(f"{distance:.3f}"))

    best = recommend_book(recommendations)
    if best:
      book, rating, distance = best
      self.best_label.setText(
        f"Best recommendation for {target_user_name}: {book} "
        f"(rated {rating:.1f}/5 by a similar user, distance: {distance:.3f})"
      )
    else:
      self.best_label.setText(
        f"{target_user_name} has read all the books and has no new recommendations."
      )


class AverageRatingsTab(QWidget):
  def __init__(self, items, ratings):
    super().__init__()
    self.items = items
    self.ratings = ratings

    layout = QVBoxLayout(self)

    refresh_button = QPushButton("Refresh Average Ratings")
    refresh_button.clicked.connect(self.populate_table)
    layout.addWidget(refresh_button)

    self.table = QTableWidget(0, 2)
    self.table.setHorizontalHeaderLabels(["Book", "Average Rating"])
    self.table.horizontalHeader().setSectionResizeMode( # type: ignore
        0, QHeaderView.ResizeMode.Stretch
    )
    self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    layout.addWidget(self.table)

    self.populate_table()

  def populate_table(self):
    average_ratings = calculate_average_ratings(self.ratings)
    ranked = sorted(zip(self.items, average_ratings), key=lambda x: x[1], reverse=True)

    self.table.setRowCount(0)
    for book, average in ranked:
      row = self.table.rowCount()
      self.table.insertRow(row)
      self.table.setItem(row, 0, QTableWidgetItem(str(book)))
      self.table.setItem(row, 1, QTableWidgetItem(f"{average:.2f}/5"))


class ChartTab(QWidget):
  def __init__(self, items, ratings):
    super().__init__()
    self.items = items
    self.ratings = ratings

    layout = QVBoxLayout(self)

    plot_button = QPushButton("Plot Average Ratings")
    plot_button.clicked.connect(self.plot_average_ratings)
    layout.addWidget(plot_button)

    self.figure = Figure(figsize=(11, 6), dpi=100)
    self.canvas = FigureCanvasQTAgg(self.figure)
    layout.addWidget(self.canvas)

    self.plot_average_ratings()

  def plot_average_ratings(self):
    average_ratings = calculate_average_ratings(self.ratings)

    self.figure.clear()
    ax = self.figure.add_subplot(111)

    colors = cm.rainbow(np.linspace(0.1, 0.9, len(self.items)))

    bars = ax.bar(
      self.items,
      average_ratings,
      color=colors,
      edgecolor="#333333",
      linewidth=0.8,
      width=0.6,
      zorder=3,
    )

    ax.set_title("Average Rating of Each Book", fontsize=14, fontweight="bold", pad=12, color="#2c3e50")
    ax.set_xlabel("Books", fontsize=11, fontweight="bold", labelpad=8, color="#2c3e50")
    ax.set_ylabel("Average Rating (0 – 5)", fontsize=11, fontweight="bold", labelpad=8, color="#2c3e50")
    ax.set_ylim(0, 5.5)
    ax.set_xticks(range(len(self.items)))
    ax.set_xticklabels(self.items, rotation=45, ha="right", fontsize=8, color="#333333")
    ax.tick_params(axis="y", labelsize=9)
    ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=7, fontweight="bold", color="#2c3e50")
    ax.grid(axis="y", linestyle="--", alpha=0.6, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#888888")
    ax.spines["bottom"].set_color("#888888")

    self.figure.tight_layout()
    self.canvas.draw()


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Book Recommendation System")
    self.resize(950, 650)

    try:
        self.users, self.items, self.ratings = load_ratings(RATING_CSV_PATH)
    except Exception as exc:
        QMessageBox.critical(self, "Failed to load data", str(exc))
        raise

    central = QWidget()
    self.setCentralWidget(central)
    layout = QVBoxLayout(central)

    header = QHBoxLayout()
    header.addWidget(QLabel("Target user:"))
    self.user_combo = QComboBox()
    self.user_combo.addItems([str(user) for user in self.users])
    header.addWidget(self.user_combo, stretch=1)
    layout.addLayout(header)

    self.tabs = QTabWidget()
    self.tabs.addTab(
        RecommendationsTab(self.users, self.items, self.ratings), "Recommendations"
    )
    self.tabs.addTab(AverageRatingsTab(self.items, self.ratings), "Average Ratings")
    self.tabs.addTab(ChartTab(self.items, self.ratings), "Chart")
    layout.addWidget(self.tabs)

  def selected_user_index(self):
    index = self.user_combo.currentIndex()
    if index < 0:
      QMessageBox.warning(self, "No user selected", "Please select a user first.")
      return None
    return index


def main():
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())


if __name__ == "__main__":
  main()