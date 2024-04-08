import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.preprocessing import image

from tensorflow.keras.models import load_model

# Load the model
model = load_model('project.h5')

# Define the input image dimensions
img_height = 224
img_width = 224
class_labels = ['Bud Root Dropping', 'Bud Rot', 'Caterpillars', 'Flaccidity', 'Stem Bleeding', 'Yellowing']


def project_sidebar():
    st.sidebar.title("About the Project")
    st.sidebar.info("This app predicts coconut tree diseases from uploaded images and recommends pesticides to cure the disease.Additionally, users can enter soil attributes like NPK values, pH, etc., from IoT sensors. Based on these values,the app recommends fertilizers to optimize production."
    )

# Add a small logo
def add_logo():
    logo_image = Image.open("E:\IV-II project\coconut.png.jpeg")  # Replace with the path to your logo image
    st.sidebar.image(logo_image, use_column_width=True)

# Cure recommendations for each disease
cure_recommendations = {
    'Bud Root Dropping': '''
    * Provide balanced and adequate nutrients through regular fertilization
    * Maintain consistent and proper watering practices to prevent both overwatering and underwatering.
    * Apply a layer of mulch around the base of the coconut tree to retain soil moisture and regulate temperature.
    * Install temporary windbreaks or barriers to shield the coconut tree from strong winds.''',

    'Bud Rot': '''
    CULTURAL CONTROL:
    * Provide adequate drainage in gardens.
    * Adopt Proper spacing and avoid overcrowding in bud rot-prone gardens.

    CHEMICAL CONTROL:
    * Remove all the infected tissues of the crown region and clean it with water. After that, apply Bordeaux paste to the center of the crown.
      {Bordeaux paste -[100g copper sulfate with 100g quick lime] each dissolved in 500 ml water} careful to handle
    * Application of Talc formulation of P.Fluorscens
    * Spraying of liquid formulation of P.Fluorescens.
    * Spraying the palms with Metalaxyl 35EC @ 2g/lt of water.
    * Spraying the palms with Dimenthomorph @ 1g/lt of water.''',

    'Caterpillars': '''
    CULTURAL CONTROL:
    * As a prophylactic measure, the first affected leaves may be cut and burnt during the beginning of the summer season.

    CHEMICAL CONTROL:
    * If the attack is severe, spray the undersurface of the leaves with 0.02% dichlorous, malathion 50 EC 0.05%, quinalphos 0.05%, Phosalone 0.05%
    * Biological control is very effective through the release of parasitoids like Gorriozus nephantidis, Elasmus, and Brachimeria Nosatoi
    * Soluneem the first water-soluble non-toxic neem pesticide.''',

    'Stem Bleeding': '''
    CULTURAL CONTROL:
    * Avoid contact of wounded palm stems with soil.
    * We ask you to remove dead trees completely and do not plant the seedlings again in that pit
    * Destroy the chiseled materials by burning
    * Provide adequate irrigation during summer and drainage during the rainy season along with recommended fertilizer.
    * Along with 50kg FYM, apply 5kg neem cake containing the antagonistic fungi, Trichoderma.

    CHEMICAL CONTROL:
    * Chisel out completely the affected tissues and paint the wound with tridemorph 5% or Bordeaux paste.
      Apply coal tar after 1-2 days on the treated portion. Burn off chiseled pieces.
    * Root feed with Tridemorph 5ml in 100 ml water, thrice a year during April-May, 
      September-October, and January-February to prevent further spread of lesions.''',

    'Flaccidity': '''
    CULTURAL METHODS:
    * Cut and remove disease leaves from the trees.
    * Irrigate coconut palms with at least 250 liters of water in a week.
    * Provide adequate drainage facilities.
    
    BIOLOGICAL METHODS:
    * Apply 50 kg FYM or green manure and 5 kg of neem cake / palm / year.

    CHEMICAL METHODS:
    * Apply fertilizers for coconut palms in average management at the rate of 1.3 kg urea, 2.00 kg super phosphate and 3.5 kg potash (MOP) / palm / year
     in the form of urea, rock phosphate and muriate of potash, respectively.
    * Magnesium may be supplied @ 500 g MgO per palm per year.''',

    'Yellowing': '''
    CULTURAL METHODS:
    * Provide adequate warm and light.
    * Mist the plant with water from a spray bottle every day. 

    CHEMICAL CONTROL:
    * Apply a foliar spray of 2% of urea thrice at fortnightly intervals or soil application of 1 to 2 kg of urea per tree or 1% of urea twice a year.''',
}

# Fertilizer recommendations based on IoT sensor values
def recommend_fertilizers(n, p, k, ph, temperature, moisture, ec):
    recommended_fertilizers = []

    # Soil pH recommendations
    ph_message = ""
    if ph < 5.5:
        ph_message = "Soil pH is too low. Use Lime."
    elif ph > 8.0:
        ph_message = "Soil pH is too high. Use Gypsum."

    # Electrical Conductivity recommendations
    ec_message = ""
    if ec > 3.0:
        ec_message = "High electrical conductivity indicates excess salt content in water. Use Gypsum or Phosphogypsum."

    # Nitrogen recommendations
    nitrogen_fertilizers = []
    if n < 200:
        nitrogen_fertilizers = ["Urea (46-0-0)", "Ammonium Sulfate (21-0-0)", "Calcium Ammonium Nitrate (CAN, 27-0-0)", "Ammonium Nitrate (34-0-0)"]
    elif n > 600:
        nitrogen_fertilizers = ["Implement leaching practices to flush excess nitrogen from the root zone."]
    else:
        nitrogen_fertilizers = ["No specific recommendations for nitrogen levels."]

    # Phosphorus recommendations
    phosphorus_fertilizers = []
    if p < 30:
        phosphorus_fertilizers = ["Rock phosphate", "Triple Superphosphate (TSP)", "Diammonium Phosphate (DAP)", "Monoammonium Phosphate (MAP)", "Phosphoric Acid"]
    elif p > 100:
        phosphorus_fertilizers = ["Implement leaching practices to flush excess phosphorus from the root zone."]
    else:
        phosphorus_fertilizers = ["No specific recommendations for phosphorus levels."]

    # Potassium recommendations
    potassium_fertilizers = []
    if k < 200:
        potassium_fertilizers = ["Potassium Chloride", "Potassium Sulfate", "Potassium Nitrate", "Langbeinite", "Organic Potassium Sources", "Sulfate of Potash Magnesia (SOPM)"]
    elif k > 600:
        potassium_fertilizers = ["Adjust fertilizer application rates and frequency."]
    else:
        potassium_fertilizers = ["No specific recommendations for potassium levels."]

    # Soil Humidity recommendations
    moisture_message = ""
    if moisture < 60:
        moisture_message = "Soil humidity is too low. Implement adequate irrigation practices and incorporate organic matter into the soil."
    elif moisture > 70:
        moisture_message = "Soil humidity is too high. Reduce mulch thickness, adjust irrigation schedules, and ensure proper soil drainage."

    return ph_message, ec_message, nitrogen_fertilizers, phosphorus_fertilizers, potassium_fertilizers, moisture_message

# Streamlit app
def main():
    st.set_page_config(page_title="Coconut disease WebApp", page_icon=":palm_tree:")


    st.markdown(
        """
        <style>
        .header {
            font-size: 24px;
            font-weight: bold;
            color: #1f77b4;
        }
        .subheader {
            font-size: 20px;
            font-weight: bold;
            color: #2ca02c;
        }
        .recommendation {
            font-size: 16px;
            color: #d62728;
            margin-left: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    add_logo()  # Add the logo
    project_sidebar()  # Add the sidebar

    st.subheader("Coconut Disease Prediction,  Pesticides and Fertilizers Recommendation WebApp")

    # Upload image through Streamlit
    uploaded_file = st.file_uploader("Choose a coconut image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image with enhanced styling
        st.image(uploaded_file, caption="Uploaded Image.", width=400, use_column_width=False)

        # Resize the uploaded image
        image_pil = Image.open(uploaded_file)
        image_resized = image_pil.resize((img_width, img_height))

        # Make prediction when the user clicks the button
        if st.button("Predict Disease", key="predict_button"):
            # Preprocess the resized image
            img_array = image.img_to_array(image_resized)
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            img_array /= 255.0  # Rescale pixel values to [0, 1]

            # Make prediction
            predictions = model.predict(img_array)
            predicted_class_index = np.argmax(predictions)
            predicted_class_label = class_labels[predicted_class_index]

            # Display the result with enhanced styling
            st.subheader("Predicted Disease:")
            st.success(predicted_class_label)
            st.subheader("Cure Recommendations:")
            st.info(cure_recommendations.get(predicted_class_label, "No recommendations available."))

    # Fertilizer recommendation section
    st.header("Fertilizer Recommendation")
    with st.expander("Fertilizer Recommendation"):
        # Input sensor values section
        st.subheader("Input Sensor Values")
        n = st.number_input("Nitrogen (ppm)", value=400)
        p = st.number_input("Phosphorous (ppm)", value=60)
        k = st.number_input("Potassium (ppm)", value=400)
        ph = st.number_input("Soil pH", value=6.5)
        temperature = st.number_input("Temperature (°C)", value=27.0)
        moisture = st.number_input("Soil Humidity (%)", value=65)
        ec = st.number_input("Electrical Conductivity (ds/m)", value=1.5)

        # Fertilizer recommendation
        if st.button("Recommend Fertilizers", key="fertilizer_button"):
            st.subheader("Fertilizer Recommendations:")

            ph_message, ec_message, nitrogen_fertilizers, phosphorus_fertilizers, potassium_fertilizers, moisture_message = recommend_fertilizers(n, p, k, ph, temperature, moisture, ec)

            if ph_message:
                st.write(ph_message)

            if ec_message:
                st.write(ec_message)

            if nitrogen_fertilizers:
                st.write("Nitrogen Fertilizers:")
                for fertilizer in nitrogen_fertilizers:
                    st.write("- " + fertilizer)

            if phosphorus_fertilizers:
                st.write("Phosphorus Fertilizers:")
                for fertilizer in phosphorus_fertilizers:
                    st.write("- " + fertilizer)

            if potassium_fertilizers:
                st.write("Potassium Fertilizers:")
                for fertilizer in potassium_fertilizers:
                    st.write("- " + fertilizer)

            if moisture_message:
                st.write(moisture_message)

if __name__ == "__main__":
    main()
