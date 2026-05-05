# InstaSmart

A comprehensive Flask-based web application for Instagram analytics and engagement prediction using machine learning. InstaSmart helps users analyze their Instagram performance, predict post engagement rates, and optimize content strategies through data-driven insights.

## 🚀 Features

- **Engagement Prediction**: Uses machine learning to predict Instagram post engagement rates based on metrics like follower count, likes, comments, hashtags, and posting time.
- **Content Analysis**: Analyzes different content categories (e.g., food, travel, fashion) to identify best-performing types.
- **Real-time Analytics**: Calculates current engagement rates and compares with predicted values.
- **Data Export**: Exports all post data to CSV for further analysis.
- **Web Dashboard**: User-friendly web interface for inputting post data and viewing results.
- **Database Storage**: Stores post analytics in a SQLite database for historical tracking.
- **Optimization Suggestions**: Provides actionable recommendations based on prediction results.

## 🛠 Tech Stack

- **Backend**: Python Flask
- **Database**: SQLAlchemy with SQLite
- **Machine Learning**: scikit-learn (Random Forest Regressor)
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML, CSS (Bootstrap-inspired styling)
- **Serialization**: Joblib for model persistence

## 📋 Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd InstaSmart
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the machine learning model**:
   ```bash
   python train_model.py
   ```

## 🎯 Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the web interface**:
   Open your browser and navigate to `http://localhost:5000`

3. **Input post data**:
   - Follower count
   - Likes and comments
   - Content category
   - Reach and impressions
   - Post type (image/video/reel)
   - Posting hour
   - Caption length
   - Number of hashtags

4. **View results**:
   - Predicted engagement rate
   - Actual engagement rate (if applicable)
   - Performance suggestions
   - Best-performing content categories

5. **Export data**:
   Visit `/export` to download `Instagram_Analytics.csv`

## 📁 Project Structure

```
InstaSmart/
├── app.py                 # Main Flask application
├── models.py              # SQLAlchemy database models
├── train_model.py         # ML model training script
├── verify_ui.py           # UI testing and verification
├── config.py              # Application configuration (placeholder)
├── routes.py              # Additional routes (placeholder)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
├── Instagram_Analytics.csv # Sample/training data
├── model.pkl              # Trained ML model
├── database.db            # SQLite database (auto-generated)
├── templates/
│   └── index.html         # Main web interface
├── static/
│   └── style.css          # CSS styling
└── instance/              # Flask instance folder
```

## 🌐 API Endpoints

- `GET /`: Main dashboard with input form
- `POST /`: Process form data and display results
- `GET /export`: Export data to CSV
- `GET /about`: About page

## 🗄 Database Schema

The application uses a single `Post` table with the following fields:
- `id`: Primary key
- `follower_count`: Integer
- `likes`: Integer
- `comments`: Integer
- `post_hour`: Integer
- `caption_length`: Integer
- `hashtags_count`: Integer
- `content_category`: String
- `reach`: Integer
- `impressions`: Integer
- `media_type`: String
- `engagement_rate`: Float

## 🤖 Machine Learning Model

The prediction model is a Random Forest Regressor trained on Instagram post data. It predicts engagement rates based on:
- Follower count
- Posting hour
- Caption length
- Hashtags count
- Content category
- Reach and impressions
- Media type

**Model Performance** (based on training):
- Mean Absolute Error: ~0.024
- R² Score: ~-0.036 (indicating room for improvement with more data)

## 🧪 Testing

Run the UI verification script:
```bash
python verify_ui.py
```

This tests that the Flask app starts correctly and returns HTTP 200.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [Your GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Flask documentation
- scikit-learn documentation
- Instagram for inspiring this analytics tool
- Open source community for amazing libraries
