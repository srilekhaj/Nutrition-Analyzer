import os,io
from flask import Flask, request, jsonify
import google.generativeai as genai
from PIL import Image
import plotly.graph_objects as go
import json
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")
app = Flask(__name__)

def get_response(image,prompt):
    response = model.generate_content([image,prompt])
    return response.text


@app.route('/predict', methods=['POST'])
def predict():
    print("Received request for /predict")
    if 'image' not in request.files or 'prompt' not in request.form:
        return jsonify({"error": "Missing image or prompt"}), 400
    print(request.files)
    print(request.form)
    print("Image and prompt received")


    image_file = request.files['image']
    prompt = request.form['prompt']
    image = Image.open(image_file)
    # # image = Image.open(io.BytesIO(image_file.read()))
    # response_text = get_response(image, prompt)

    # image = Image.open(io.BytesIO(image_file.read()))

    prompt = request.form.get("prompt", "")
    result = get_response(image, prompt)
    return jsonify({"response": result})

# @app.route('/compare', methods=['POST'])
# def compare():
#     meal1 = request.files.get('image1')
#     meal2 = request.files.get('image2')
#     prompt = request.form.get("prompt", "")
#     if not meal1 or not meal2:
#         return jsonify({"error": "Both meal images are required"}), 400
    
#     try:
#         img1 = Image.open(meal1)
#     except Exception as e:
#         print(f"Error reading Meal 1 image: {e}")
#     try:
#         img2 = Image.open(meal2)
#     except Exception as e:
#         print(f"Error reading Meal 2 image: {e}")
    
#     response1 = get_response(img1, prompt)
#     response2 = get_response(img2, prompt)
#     return jsonify({"meal1_response": response1, "meal2_response": response2})


@app.route('/compare', methods=['POST'])
def compare():
    meal1 = request.files.get('image1')
    meal2 = request.files.get('image2')
    prompt = request.form.get("prompt", "")

    if not meal1 or not meal2:
        return jsonify({"error": "Both meal images are required"}), 400

    # Try loading images
    try:
        img1 = Image.open(meal1)
    except Exception as e:
        print(f"Error reading Meal 1 image: {e}")
        return jsonify({"error": "Invalid or unreadable image1"}), 400

    try:
        img2 = Image.open(meal2)
    except Exception as e:
        print(f"Error reading Meal 2 image: {e}")
        return jsonify({"error": "Invalid or unreadable image2"}), 400

    # Process images
    try:
        response1 = get_response(img1, prompt)
        response2 = get_response(img2, prompt)
    except Exception as e:
        return jsonify({"error": f"Error generating responses: {str(e)}"}), 500

    return jsonify({
        "meal1_response": response1,
        "meal2_response": response2
    })

if __name__ == "__main__":
    app.run(debug=True)