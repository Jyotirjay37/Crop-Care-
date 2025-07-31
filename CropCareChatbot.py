import streamlit as st
import pandas as pd
from googletrans import Translator

# Define available languages
languages = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Tamil": "ta",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa",
}

translator = Translator()

def translate_text(text, target_language):
    """Translate text to the chosen language."""
    return translator.translate(text, dest=target_language).text

def input_data(uploaded_file):
    """Load and process dataset."""
    if uploaded_file is not None:
        data = pd.read_csv("data_core.csv")
        return data
    return None

def filter_data(data, crop_type):
    """Filter data for a specific crop type."""
    return data[data["Crop Type"].str.lower() == crop_type.lower()]

def recommend_fertilizer(data, crop_type, selected_language):
    """Provide fertilizer recommendations."""
    crop_data = filter_data(data, crop_type)
    if crop_data.empty:
        return translate_text(f"No data available for {crop_type}.", languages[selected_language])
    
    response = crop_data[['Fertilizer Recommendation', 'Nitrogen', 'Phosphorus', 'Potassium']]
    return response.applymap(lambda x: translate_text(str(x), languages[selected_language]))

def main():
    st.title("Agricultural Advisor ChatBot")
    
    # Language selection
    selected_language = st.selectbox("Choose your language:", list(languages.keys()))

    uploaded_file = st.file_uploader(translate_text("Upload your dataset", languages[selected_language]), type=["csv"])
    if uploaded_file is None:
        st.write(translate_text("Please upload a dataset to proceed.", languages[selected_language]))
        return

    data = input_data(uploaded_file)

    if data is None:
        st.write(translate_text("Invalid dataset format.", languages[selected_language]))
        return

    chatbox = st.container(height=300, border=True)
    prompt = chatbox.chat_input(translate_text("Ask about crop conditions and fertilizers", languages[selected_language]))

    if prompt:
        if "fertilizer" in prompt.lower():
            crop_type = prompt.split("for")[-1].strip()
            response = recommend_fertilizer(data, crop_type, selected_language)
            chatbox.write(response)
        elif "humidity" in prompt.lower():
            chatbox.write(data[['Crop Type', 'Humidity']].applymap(lambda x: translate_text(str(x), languages[selected_language])))
        elif "temperature" in prompt.lower():
            chatbox.write(data[['Crop Type', 'Temperature']].applymap(lambda x: translate_text(str(x), languages[selected_language])))
        else:
            chatbox.write(translate_text("I can provide insights on fertilizers, humidity, and temperature.", languages[selected_language]))

if __name__ == "__main__":
    main()
    


