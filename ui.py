import streamlit as st
import base64
from io import BytesIO
from PIL import Image
import requests
import json
import plotly.graph_objects as go

st.markdown("""
<style>

/* --- GLASS EFFECT CONTAINERS --- */
.glass-card {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 18px;
    padding: 0px;
    border: 1px solid rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.1);
    margin-bottom: 25px;
}

/* Rounded images with soft shadow */
img {
    border-radius: 16px;
    box-shadow: 0 4px 22px rgba(0,0,0,0.20);
}

/* Top-align all column elements */
[data-testid="column"] {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}

/* Align metrics left for cleaner visual */
[data-testid="stMetric"] {
    text-align: left !important;
    padding: 5px 0 !important;
}

/* Reduce container side padding for modern layout */
.block-container {
    padding-top: 3rem !important;
    padding-bottom: 1rem !important;
    max-width: 1100px !important;
}

/* Typography polish */
h1, h2, h3, h4 {
    font-weight: 600;
    letter-spacing: -0.5px;
}

/* Better readability */
.stMarkdown, .stText {
    line-height: 1.55rem;
    font-size: 0.95rem;
}

/* Verdict card style */
.verdict-box {
    background: rgba(0, 255, 150, 0.15);
    border-left: 4px solid #00c983;
    padding: 18px;
    border-radius: 14px;
    backdrop-filter: blur(10px);
    margin-top: 25px;
}

.fixed-meal-image {
    width: 450px !important;
    height: 300px !important;
    object-fit: cover;      /* fills frame without stretching */
    border-radius: 16px;
    box-shadow: 0 4px 22px rgba(0,0,0,0.20);
}
            
/* Optional: gradient app background */
body {
    background: linear-gradient(135deg, #dfe9f3 0%, #ffffff 100%);
}
            

</style>
""", unsafe_allow_html=True)


st.title("🥗 AI Nutrition Analyzer")
tab1, tab2 = st.tabs(["📸 Single Meal Analysis", "⚖️ Comparison Mode"])
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

def show_fixed_image(pil_img, caption=""):
    buffer = BytesIO()
    pil_img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode()

    st.markdown(
        f"<img class='fixed-meal-image' src='data:image/png;base64,{img_b64}'>",
        unsafe_allow_html=True
    )
    if caption:
        st.caption(caption)

def plot_nutrition_chart(nutrients, title):
    fig = go.Figure(data=[
        go.Bar(x=list(nutrients.keys()), y=list(nutrients.values()))
    ])
    fig.update_layout(title=title, xaxis_title="Nutrient", yaxis_title="Grams")
    st.plotly_chart(fig)



image =""
#streamlit app
def main():
    with tab1:

        upload_image = st.file_uploader("Upload your meal image and get instant nutrition insights powered by Gemini AI!", type=['jpg', 'png', 'jpeg'])
        if upload_image is not None:

            # img = Image.open(upload_image)
            prompt = """
                You are a Nutritionist  Assistant
                You need to suggest good nutrition food to user image
                You need to display food items from user image
                You need to calculate and tell how many calories does the menu have
                You need check whether these food items are good to health
                If it not good to health then suggest some good advice and good food to them
                """
            url = "http://localhost:5000/predict"  # Replace with your actual endpoint
            
            
            files = {
                "image": upload_image,
            }
            data={
                "prompt": prompt
            }
            result = requests.post(url, files=files, data=data)
            st.subheader("🍱 Food Analysis Report")
            # st.markdown(result) response object <Response [200]>
            output_json = result.json()
            result_text = output_json.get("response", "")
            st.write(result_text)

    
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
            

            def payload_function(meal1_img, meal2_img, prompt_json):  
                    url = "http://localhost:5000/compare"  # Replace with your actual endpoint
                    files = {
                        "image1": meal1_img,
                        "image2": meal2_img,
                    }
                    data = {
                        "prompt": prompt_json
                    }
                    response = requests.post(url, data=data, files=files)
                    output_json = response.json()
                    return output_json
            
            res1 = payload_function(meal1,meal2, prompt_json)
            # res2 = payload_function(meal2, prompt_json)
            
            # st.write(res1)
            # st.write(res2)
            print(type(res1))
            # print(type(res2))
            print()
            data1 = parse_response(res1['meal1_response'])
            data2 = parse_response(res1['meal2_response'])
            print(type(data1))
            print(type(data2))
            print(data1)
            print(data2)

            if data1 and data2:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    # st.image(Image.open(meal1),width='stretch' ,caption="Meal 1")
                    show_fixed_image(Image.open(meal1), caption="Meal 1")
                    st.subheader("🥣 Meal 1 Nutrition Details")
                    st.write("Items", f"{data1["items"]}")
                    st.metric("Calories", f"{data1['total_calories']} kcal")
                    st.metric("Health Score", data1["health_score"])
                    plot_nutrition_chart(data1["nutrients"], "Meal 1 Nutrition")
                    st.markdown("### 💡 Advice")
                    st.write(data1["health_advice"])
                    st.markdown("</div>", unsafe_allow_html=True)

                with col2:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    # st.image(Image.open(meal2),width='stretch', caption="Meal 2")
                    show_fixed_image(Image.open(meal2), caption="Meal 2")
                    st.subheader("🍽️ Meal 2 Nutrition Details")
                    st.write("Items", f"{data2["items"]}")
                    st.metric("Calories", f"{data2['total_calories']} kcal")
                    st.metric("Health Score", data2["health_score"])
                    plot_nutrition_chart(data2["nutrients"], "Meal 2 Nutrition")
                    st.markdown("### 💡 Advice")
                    st.write(data2["health_advice"])
                    st.markdown("</div>", unsafe_allow_html=True)

                st.divider()
                st.subheader("🏆 Final Verdict")
                
                if data1["health_score"] > data2["health_score"]:
                    st.markdown(
                        "<div class='verdict-box'><strong>Meal 1</strong> is healthier 🥦</div>",
                        unsafe_allow_html=True
                    )
                elif data1["health_score"] < data2["health_score"]:
                    st.markdown(
                        "<div class='verdict-box'><strong>Meal 2</strong> is healthier 🍛</div>",
                        unsafe_allow_html=True
                    )


                else:
                    avg_score = (data1["health_score"] + data2["health_score"]) / 2
                    if avg_score >= 7:
                        # st.success("✅ Both meals are equally healthy! Great nutrition choices 🥗")
                        st.markdown("""
                            <div class="verdict-good">
                                <strong>✅ Both meals are equally healthy!</strong><br>
                                Excellent nutrition balance 🥗🔥
                            </div>
                            """, unsafe_allow_html=True)
                        st.info("Tip 💬: Keep this balance of proteins, fiber, and low sugar!")
                    elif avg_score >= 4:
                        # st.warning("⚖️ Both meals are moderately healthy — can be improved.")
                        
                        st.markdown("""
                        <div class="verdict-medium">
                            <strong>⚖️ Both meals are moderately healthy.</strong><br>
                            There's room for improvement.
                        </div>
                        """, unsafe_allow_html=True)
                        st.info("Tip 💬: Try replacing refined carbs or sugary drinks with healthier options.")
                    else:
                        # st.error("Both meals are unhealthy ❌ — try replacing them with more nutritious options.")
                        st.markdown("""
                            <div class="verdict-bad">
                                <strong>❌ Both meals are unhealthy.</strong><br>
                                Consider healthier alternatives.
                            </div>
                            """, unsafe_allow_html=True)
                        st.info("Tip 💬: Consider cutting down fried, processed, or high-calorie foods.")
            else:
                st.error("⚠️ Could not parse Gemini response. Try again.")




if __name__ =="__main__":
    main()
