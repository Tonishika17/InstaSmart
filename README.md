# InstaSmart

A comprehensive Flask-based web application for Instagram analytics and engagement prediction using machine learning. InstaSmart helps users analyze their Instagram performance, predict post engagement rates, and optimize content strategies through data-driven insights. The application features a production-ready preprocessing pipeline for accurate predictions and includes advanced analytics for traffic sources, call-to-action effectiveness, and time-based optimizations.

## 🚀 Features

- **Advanced Engagement Prediction**: Utilizes a Random Forest Regressor with a robust preprocessing pipeline to predict Instagram post engagement rates. Includes log transformation for skewed features, outlier capping, and time-based feature engineering (e.g., posting periods).
- **Comprehensive Content Analysis**: Analyzes content categories, media types, traffic sources, and posting times to identify best-performing strategies.
- **Real-time Analytics & Insights**: Calculates engagement rates, provides performance comparisons, and offers actionable suggestions based on predictions.
- **Extended Metrics Tracking**: Tracks follower count, likes, comments, shares, saves, followers gained, reach, impressions, hashtags, caption length, and more.
- **Traffic Source Analysis**: Evaluates performance across different traffic sources (e.g., Home Feed, Hashtags, Reels Feed, External).
- **Call-to-Action Optimization**: Assesses the impact of call-to-action elements on engagement.
- **Time-Based Insights**: Analyzes posting hours, days of the week, and posting periods for optimal scheduling.
- **Data Export**: Exports all post data to CSV for further analysis.
- **Web Dashboard**: User-friendly interface for inputting detailed post data and viewing results.
- **Database Storage**: Stores post analytics in a SQLite database for historical tracking and trend analysis.
- **Modular Preprocessing**: Production-style pipeline with separate handling for numeric, categorical, and binary features, including imputation and scaling.

## 🛠 Tech Stack

- **Backend**: Python Flask
- **Database**: SQLAlchemy with SQLite
- **Machine Learning**: scikit-learn (Random Forest Regressor with ColumnTransformer and Pipeline)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn (for model evaluation plots)
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
   This generates `model.pkl` and evaluation plots in the `plots/` directory.

## 🎯 Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the web interface**:
   Open your browser and navigate to `http://localhost:5000`

3. **Input post data**:
   - Follower count
   - Likes, comments, shares, saves
   - Followers gained
   - Reach and impressions
   - Content category (e.g., Technology, Food, Travel)
   - Media type (e.g., image, video, reel)
   - Traffic source (e.g., Home Feed, Hashtags, Reels Feed, External)
   - Day of the week
   - Posting hour (0-23)
   - Caption length
   - Number of hashtags
   - Call-to-action presence

4. **View results**:
   - Predicted engagement rate (based on ML model)
   - Actual engagement rate (calculated from inputs)
   - Performance suggestions (e.g., outperform/underperform predictions)
   - Analytics insights (e.g., hashtag optimization, call-to-action recommendations)
   - Best-performing content categories
   - Historical post data

5. **Export data**:
   Visit `/export` to download `Instagram_Analytics.csv`

## 📁 Project Structure

```
InstaSmart/
├── app.py                 # Main Flask application with prediction logic
├── models.py              # SQLAlchemy database models (Post model)
├── train_model.py         # ML model training script with modular preprocessing
├── verify_ui.py           # UI testing and verification
├── config.py              # Application configuration
├── routes.py              # Additional routes (placeholder)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
├── Instagram_Analytics.csv # Training/sample data
├── model.pkl              # Trained ML model pipeline
├── database.db            # SQLite database (auto-generated)
├── plots/                 # Model evaluation plots (auto-generated)
│   ├── feature_importance.png
│   └── confusion_matrix.png
├── static/
│   └── style.css          # CSS styling
├── templates/
│   └── index.html         # Main dashboard template
└── instance/              # Flask instance folder
```

## 🤖 Machine Learning Pipeline

The model uses a production-style preprocessing pipeline:

- **Data Loading & Cleaning**: Handles missing values, data type conversions, and inconsistencies (e.g., reach > impressions).
- **Feature Engineering**: Adds time-based features (posting periods), engagement calculations, and reach-impression ratios.
- **Outlier Handling**: Caps extreme values at 1st and 99th percentiles.
- **Preprocessing**:
  - Skewed numeric features: Imputation (median), log transformation, standardization.
  - Linear numeric features: Imputation (median), standardization.
  - Binary features: Imputation (constant), standardization.
  - Categorical features: Imputation (constant), one-hot encoding.
- **Model**: Random Forest Regressor with 200 estimators.
- **Evaluation**: MAE, R², feature importance, confusion matrix for binned predictions.

## 📊 Model Performance

After training, the model achieves:
- Mean Absolute Error (MAE): ~0.005
- R² Score: ~0.65
- Feature importance plots and classification reports are generated in `plots/`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
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
