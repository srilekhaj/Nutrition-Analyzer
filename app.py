import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
import plotly.graph_objects as go
import json
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def get_response(image,prompt):
    response = model.generate_content([image,prompt])
    return response.text


def parse_response(response):
    if response is None:
        return None

    if isinstance(response, dict):
        # Already parsed
        return response

    if isinstance(response, str):
        # Clean up code fences if present
        cleaned = response.strip().strip('`')
        cleaned = cleaned.replace("json\n", "").replace("\n", "")
        try:
            json_text = json.loads(cleaned)
            print(type(json_text))
            return json_text
        except json.JSONDecodeError:
            print("❌ JSON decode error. Response was not valid JSON.")
            return None

    # Unexpected type
    return None


def plot_nutrition_chart(nutrients, title):
    fig = go.Figure(data=[
        go.Bar(x=list(nutrients.keys()), y=list(nutrients.values()))
    ])
    fig.update_layout(title=title, xaxis_title="Nutrient", yaxis_title="Grams")
    st.plotly_chart(fig)


st.title("🥗 AI Nutrition Analyzer")
tab1, tab2 = st.tabs(["📸 Single Meal Analysis", "⚖️ Comparison Mode"])

image =""
#streamlit app
def main():
    with tab1:

        upload_image = st.file_uploader("Upload your meal image and get instant nutrition insights powered by Gemini AI!", type=['jpg', 'png', 'jpeg'])
        if upload_image is not None:

            image = Image.open(upload_image)
            prompt = """
                You are a Nutritionist  Assistant
                You need to suggest good nutrition food to user image
                You need to display food items from user image
                You need to calculate and tell how many calories does the menu have
                You need check whether these food items are good to health
                If it not good to health then suggest some good advice and good food to them
                """
            result = get_response(image,prompt)
            st.subheader("🍱 Food Analysis Report")
            st.markdown(result)

            # st.write(result)

    
    with tab2:
        st.subheader("Compare Two Meals")

        col1, col2 = st.columns(2)
        with col1:
            meal1 = st.file_uploader("Upload Meal 1", type=["jpg", "png", "jpeg"], key="meal1")
        with col2:
            meal2 = st.file_uploader("Upload Meal 2", type=["jpg", "png", "jpeg"], key="meal2")

        if meal1 and meal2:
            prompt_json = """
            You are a Nutrition Assistant.
            Return your answer ONLY as valid JSON.
            Do not include explanations or markdown.
            Do not include code blocks or any text before or after the JSON.

            Analyze the given meal image and return data in this exact JSON format:
            {
            "items": ["food1", "food2"],
            "total_calories": 560,
            "nutrients": {"protein": 25, "fat": 20, "carbs": 60},
            "health_advice": "Your suggestion...",
            "health_score": 7
            }
            """

            st.info("Analyzing both meals...")
            try:
                img1 = Image.open(meal1)
            except Exception as e:
                 st.error(f"Error reading Meal 1 image: {e}")
            try:
                img2 = Image.open(meal2)
            except Exception as e:
                st.error(f"Error reading Meal 2 image: {e}")

            res1 = get_response(img1, prompt_json)
            res2 = get_response(img2, prompt_json)
            
            # st.write(res1)
            # st.write(res2)
            print(type(res1))
            print(type(res2))
            print()
            data1 = parse_response(res1)
            data2 = parse_response(res2)
            print(type(data1))
            print(type(data2))
            print(data1)
            print(data2)

            if data1 and data2:
                col1, col2 = st.columns(2)
                with col1:
                    st.image(img1, caption="Meal 1")
                    st.write("Items", f"{data1["items"]}")
                    st.metric("Calories", f"{data1['total_calories']} kcal")
                    st.metric("Health Score", data1["health_score"])
                    plot_nutrition_chart(data1["nutrients"], "Meal 1 Nutrition")
                    st.write("Advice:", data1["health_advice"])
                with col2:
                    st.image(img2, caption="Meal 2")
                    st.write("Items", f"{data2["items"]}")
                    st.metric("Calories", f"{data2['total_calories']} kcal")
                    st.metric("Health Score", data2["health_score"])
                    plot_nutrition_chart(data2["nutrients"], "Meal 2 Nutrition")
                    st.write("Advice:", data2["health_advice"])

                st.divider()
                st.subheader("🏆 Final Verdict")
                if data1["health_score"] > data2["health_score"]:
                    st.success("Meal 1 is healthier 🥦")
                elif data1["health_score"] < data2["health_score"]:
                    st.success("Meal 2 is healthier 🍛")
                else:
                    avg_score = (data1["health_score"] + data2["health_score"]) / 2
                    if avg_score >= 7:
                        st.success("✅ Both meals are equally healthy! Great nutrition choices 🥗")
                        st.info("Tip 💬: Keep this balance of proteins, fiber, and low sugar!")
                    elif avg_score >= 4:
                        st.warning("⚖️ Both meals are moderately healthy — can be improved.")
                        st.info("Tip 💬: Try replacing refined carbs or sugary drinks with healthier options.")
                    else:
                        st.error("Both meals are unhealthy ❌ — try replacing them with more nutritious options.")
                        st.info("Tip 💬: Consider cutting down fried, processed, or high-calorie foods.")
            else:
                st.error("⚠️ Could not parse Gemini response. Try again.")

if __name__ =="__main__":
    main()
