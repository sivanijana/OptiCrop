# OptiCrop - Smart Agricultural Production Optimization Engine

OptiCrop is a production-quality Flask and machine learning application that predicts the most suitable crop based on soil and climate variables such as nitrogen, phosphorus, potassium, temperature, humidity, pH, and rainfall. The app features a polished, animated, responsive UI designed to feel like a modern AI agritech SaaS product.

## Features
- AI-driven crop recommendation engine
- Premium glassmorphism-inspired landing page
- Responsive prediction form with validation and loading states
- Dynamic result page with actionable agronomy advice
- Contact form with validation and feedback
- Dark mode toggle and rich frontend animations

## Tech Stack
- Backend: Python, Flask
- ML: Scikit-Learn, Pandas, NumPy, Pickle
- Visualization: Matplotlib, Seaborn
- Frontend: HTML5, CSS3, Bootstrap 5, JavaScript

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python app.py
```
Then open http://127.0.0.1:5000/

## Folder Structure
- app.py - Flask application
- utils/preprocessing.py - data loading and feature preparation
- utils/predictor.py - model loading and prediction interface
- model/ - trained model artifacts
- templates/ - HTML pages
- static/ - CSS, JS, images
- notebooks/ - training notebook
- dataset/ - crop recommendation dataset

## Future Scope
- Add weather API integration
- Support PDF report export
- Add farmer-specific dashboards
- Deploy to cloud infrastructure
