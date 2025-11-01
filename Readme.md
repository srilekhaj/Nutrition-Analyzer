# 🥗 AI Nutrition Analyzer [https://nutrition-analyzerz.streamlit.app/]

**AI Nutrition Analyzer** is a Streamlit web app that uses **Google Gemini AI** to analyze meal images and provide detailed **nutrition insights**, **calorie estimates**, and **health advice**.
You can upload one meal to analyze or compare two meals side by side!

---

## Features

- **Single Meal Analysis**

* Upload a food image.
* AI identifies food items, estimates calories, and gives health advice.

- **Meal Comparison Mode**

* Upload two meal images.
* AI compares nutrients, health scores, and provides a final verdict on which meal is healthier.

- **Interactive Visuals**

* Nutrition breakdown shown via interactive **Plotly bar charts**.

- **Powered by Google Gemini**

* Uses the `gemini-2.5-flash` model for fast, multimodal (image + text) understanding.

---

## 🧠 Tech Stack

* **Python 3.9+**
* **Streamlit** – for the web app UI
* **Google Generative AI (Gemini API)** – for image + text analysis
* **PIL (Pillow)** – for image processing
* **Plotly** – for interactive nutrient visualization
* **dotenv** – for managing API keys

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-nutrition-analyzer.git
cd ai-nutrition-analyzer
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate         # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```txt
streamlit
google-generativeai
python-dotenv
Pillow
plotly
```

### 4. Set Up Your API Key

Create a `.env` file in the root directory:

```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

You can obtain your Gemini API key from:
 [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

## Run the App

```bash
streamlit run app.py
```

Then open the app in your browser (usually [http://localhost:8501](http://localhost:8501)).

---

## App Structure

```
ai-nutrition-analyzer/
│
├── app.py                # Main Streamlit application
├── .env                  # Contains your Google API key
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## How It Works

1. The user uploads one or two meal images.
2. The image(s) and a natural-language **prompt** are sent to Gemini (`gemini-2.5-flash`).
3. Gemini returns structured JSON containing:

   ```json
   {
     "items": ["chicken", "broccoli", "rice"],
     "total_calories": 560,
     "nutrients": {"protein": 25, "fat": 20, "carbs": 60},
     "health_advice": "Add more greens and reduce fried items.",
     "health_score": 7
   }
   ```
4. Streamlit visualizes this data using `st.metric`, `st.image`, and `plotly` charts.
5. In comparison mode, both meals are analyzed and ranked by health score.

---

## Example Use Cases

* Nutrition tracking for gym or diet plans.
* Comparing restaurant meals or homemade dishes.
* Educational demo for AI-powered food analysis.

---
