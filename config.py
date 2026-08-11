"""
Configurations for the recommendation system will all be loaded here for reusability and maintainability.
"""

from pathlib import Path

# Project Paths
PROJECT_ROOT = Path(__file__).resolve().parents[0]

RATING_CSV_PATH = PROJECT_ROOT / "data" / "ratings.csv"