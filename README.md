# InstaSmart

A Flask-based web application for Instagram analytics and engagement prediction using machine learning.

## Features

- Predict Instagram post engagement rates
- Analyze content categories and posting strategies
- Export analytics data to CSV
- Web-based UI for input and results

## Setup

1. Clone the repository
2. Create and activate virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Train the model:
   ```
   python train_model.py
   ```
5. Run the application:
   ```
   python app.py
   ```
6. Open http://localhost:5000 in your browser

## Files

- `app.py`: Main Flask application
- `models.py`: Database models
- `train_model.py`: ML model training script
- `verify_ui.py`: UI testing script
- `Instagram_Analytics.csv`: Sample data for training/export

## Requirements

See `requirements.txt` for dependencies.
