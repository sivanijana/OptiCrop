import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.predictor import CropPredictor
from utils.training import train_and_save_model

app = Flask(__name__)
app.secret_key = "opticrop-secret-key"
app.config["SESSION_TYPE"] = "filesystem"

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "model.pkl"
LABEL_ENCODER_PATH = BASE_DIR / "model" / "label_encoder.pkl"

if not MODEL_PATH.exists() or not LABEL_ENCODER_PATH.exists():
    train_and_save_model()

predictor = CropPredictor(model_path=MODEL_PATH, label_encoder_path=LABEL_ENCODER_PATH)

CROP_PROFILE = {
    "rice": {"season": "Rainy Season", "fertilizer": "Urea + Compost", "water": "High", "temp": "20-35°C", "humidity": "70-90%", "tips": "Keep paddy fields flooded and use organic matter to sustain soil fertility."},
    "maize": {"season": "Summer", "fertilizer": "NPK 20-20-20", "water": "Moderate", "temp": "18-30°C", "humidity": "50-70%", "tips": "Ensure well-drained soil and apply balanced nutrients during tasseling."},
    "chickpea": {"season": "Winter", "fertilizer": "DAP + Sulphur", "water": "Low", "temp": "15-25°C", "humidity": "40-60%", "tips": "Avoid waterlogging and use residual soil moisture efficiently."},
    "kidneybeans": {"season": "Spring", "fertilizer": "Compost + Phosphorus", "water": "Moderate", "temp": "20-30°C", "humidity": "55-75%", "tips": "Provide trellis support and monitor for root rot."},
    "pigeonpeas": {"season": "Kharif", "fertilizer": "Rhizobium + Potash", "water": "Low", "temp": "22-35°C", "humidity": "45-65%", "tips": "Use drought-resilient spacing and intercrop with cereals."},
    "mothbeans": {"season": "Arid", "fertilizer": "Organic manure", "water": "Low", "temp": "25-35°C", "humidity": "30-50%", "tips": "Choose sandy loam and limit irrigation to early growth stages."},
    "mungbean": {"season": "Summer", "fertilizer": "Biofertilizer", "water": "Low", "temp": "22-35°C", "humidity": "40-60%", "tips": "Plant after warm soils are established and keep field weed-free."},
    "blackgram": {"season": "Rainy", "fertilizer": "NPK + Sulphur", "water": "Moderate", "temp": "24-35°C", "humidity": "55-75%", "tips": "Use timely sowing and avoid excess moisture during flowering."},
    "lentil": {"season": "Winter", "fertilizer": "Phosphorus + Potash", "water": "Low", "temp": "10-25°C", "humidity": "45-65%", "tips": "Use cool-weather sowing and ensure deep tillage."},
    "pomegranate": {"season": "Dry", "fertilizer": "Balanced NPK", "water": "Moderate", "temp": "20-35°C", "humidity": "35-60%", "tips": "Protect fruit quality with pruning and drip irrigation."},
    "banana": {"season": "Year-Round", "fertilizer": "Potassium-rich", "water": "High", "temp": "25-35°C", "humidity": "80-95%", "tips": "Maintain humidity and use mulch to conserve moisture."},
    "mango": {"season": "Hot", "fertilizer": "Micronutrient mix", "water": "Moderate", "temp": "24-30°C", "humidity": "60-75%", "tips": "Protect blossoms from late frost and provide regular pruning."},
    "grapes": {"season": "Spring", "fertilizer": "Potash + Compost", "water": "Moderate", "temp": "15-30°C", "humidity": "50-70%", "tips": "Train vines and manage canopy for airflow and disease reduction."},
    "watermelon": {"season": "Summer", "fertilizer": "Potassium + Compost", "water": "High", "temp": "25-35°C", "humidity": "50-70%", "tips": "Mulch the soil and avoid overwatering during fruit ripening."},
    "muskmelon": {"season": "Summer", "fertilizer": "Balanced NPK", "water": "Moderate", "temp": "20-30°C", "humidity": "45-65%", "tips": "Use raised beds and ensure good pollination."},
    "apple": {"season": "Temperate", "fertilizer": "Nitrogen + Potassium", "water": "Moderate", "temp": "10-25°C", "humidity": "55-80%", "tips": "Ensure chill hours and timely pruning for higher yields."},
    "orange": {"season": "Winter", "fertilizer": "NPK + Micronutrients", "water": "Moderate", "temp": "15-30°C", "humidity": "60-85%", "tips": "Use fertigation and protect foliage from pests."},
    "papaya": {"season": "Tropical", "fertilizer": "Potassium-rich", "water": "High", "temp": "22-32°C", "humidity": "70-90%", "tips": "Maintain moisture and provide shade for young plants."},
    "coconut": {"season": "Tropical", "fertilizer": "Organic manure", "water": "High", "temp": "27-35°C", "humidity": "80-90%", "tips": "Use mulching and protect against salt stress in coastal regions."},
    "cotton": {"season": "Kharif", "fertilizer": "NPK 15-15-15", "water": "Moderate", "temp": "21-32°C", "humidity": "50-70%", "tips": "Balance irrigation with pest management to preserve fiber quality."},
    "jute": {"season": "Monsoon", "fertilizer": "Nitrogen + Compost", "water": "High", "temp": "25-35°C", "humidity": "80-95%", "tips": "Harvest timely to retain fiber quality and avoid lodging."},
    "coffee": {"season": "Cool humid", "fertilizer": "Organic compost", "water": "Moderate", "temp": "18-28°C", "humidity": "70-85%", "tips": "Use shade management and keep soil naturally rich."},
}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            form_data = {
                "N": float(request.form.get("nitrogen", 0)),
                "P": float(request.form.get("phosphorous", 0)),
                "K": float(request.form.get("potassium", 0)),
                "temperature": float(request.form.get("temperature", 0)),
                "humidity": float(request.form.get("humidity", 0)),
                "ph": float(request.form.get("ph", 0)),
                "rainfall": float(request.form.get("rainfall", 0)),
            }
        except ValueError:
            flash("Please enter valid numeric values for all fields.", "danger")
            return redirect(url_for("predict"))

        if not all(value >= 0 for value in form_data.values()):
            flash("Values cannot be negative.", "danger")
            return redirect(url_for("predict"))

        prediction = predictor.predict(form_data)
        profile = CROP_PROFILE.get(prediction.lower(), {
            "season": "Adaptive",
            "fertilizer": "Balanced nutrition",
            "water": "Moderate",
            "temp": "Ideal local range",
            "humidity": "Adaptable",
            "tips": "Use soil testing and local agronomy guidance for best results."
        })

        session["last_prediction"] = {
            "crop": prediction,
            "confidence": round(float(predictor.predict_proba(form_data)[0]), 3),
            "profile": profile,
            "inputs": form_data,
        }
        history = session.get("history", [])
        history.insert(0, {
            "crop": prediction,
            "confidence": round(float(predictor.predict_proba(form_data)[0]), 3),
        })
        session["history"] = history[:6]
        return redirect(url_for("result"))

    return render_template("predict.html")


@app.route("/result")
def result():
    result_data = session.get("last_prediction")
    if not result_data:
        return redirect(url_for("predict"))
    return render_template("result.html", result=result_data, history=session.get("history", []))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not all([name, email, message]) or "@" not in email:
            flash("Please enter a valid name, email, and message.", "danger")
        else:
            flash("Thank you for your message. Our agronomy team will contact you soon.", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
