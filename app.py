import os 
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
from PIL import Image
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_responce(input_prompt, image):
    model=genai.GenerativeModel('gemini-pro-vision')
    responce=model.generate_content([input_prompt,image[0]])
    return responce.text

def input_image_setup(upload_file):
    if upload_file is not None:
        bytes_data =upload_file.getvalue()

        image_parts = [
            {
                "mime_type":upload_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else :
        raise FileNotFoundError("No file uploaded")
    
#streamlit app
st.set_page_config(page_title="Nutrition content")
st.header("GEMINI NUTRITION APP")
uploaded_file = st.file_uploader("chose an image", type=["jpg","jpeg","png"])
image=" "
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit= st.button("Tell me about the total calories") 

input_prompt="""
Your an expert in nutritionist, you eed to see every food ideam from the image , and provide calories contains in this food and calculate the total calories, provide the details of every food item with quantity in ounce and calories intake in below format

1. item1 - no of calories
2. item2 - no of calories
"""
if submit:
    image_data= input_image_setup(uploaded_file)
    respo=get_gemini_responce(input_prompt, image_data)
    st.header("Responce-Nutrition value")
    st.write(respo)