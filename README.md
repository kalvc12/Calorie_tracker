
# Personal Calorie & Macro Tracker 🍏

A lightweight Streamlit web app to log foods from the **OpenFoodFacts** database and see daily calorie & macronutrient totals.

## Features
* 🔍 Search any food by name and add a serving size (grams)
* 📊 Automatic calculation of kcal, protein, carbs, fat
* 💾 Local CSV log stored in `food_log.csv`
* 🗓️ Daily summary table & totals

## Quick Start

1. **Install Python 3.9+**  
   <https://www.python.org/downloads/>

2. **Create and activate a virtual environment (recommended)**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**  
   ```bash
   streamlit run app.py
   ```

5. Visit the local URL (usually http://localhost:8501) in your browser.

## Notes
* The app writes a `food_log.csv` file in the same directory to keep your entries.
* This is a personal-use prototype; OpenFoodFacts data can be incomplete or inconsistent.
* Extend it! Add user authentication, goal tracking, charts, or barcode scanning.

---
© 2025
