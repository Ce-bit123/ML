import streamlit as st
import shap
from streamlit_shap import st_shap
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# Title
st.header("Risk prediction of early neurological deterioration within 72 hours after thrombolytic therapy in ischemic stroke")

# Input bar 1
ott = st.number_input("Enter Time from onset to treatment (h)")

# Input bar 2
NIHSS_score_before_thrombolysis = st.number_input("Enter NIHSS score before thrombolysis")
#NIHSS_score_after_thrombolysis1 = st.number_input("Enter NIHSS score after thrombolysis")
hemoglobin = st.number_input("Enter hemoglobin (g/L)")
Thrombin_time = st.number_input("Enter Thrombin_time (sec)")
lymphocyte= st.number_input("Enter lymphocyte_count (×10⁹/L)")
# Dropdown input
prothrombin_time = st.number_input("Enter prothrombin_time (sec)")

# If button is pressed
if st.button("Submit"):
    # Unpickle classifier
    clf = joblib.load("clf1.pkl")

    # Store inputs into dataframe
    X = pd.DataFrame([[ott, NIHSS_score_before_thrombolysis,hemoglobin,
                       Thrombin_time,lymphocyte,prothrombin_time]],
                     columns=["ott", "NIHSS_score_before_thrombolysis","hemoglobin",
                       "Thrombin_time","lymphocyte","prothrombin_time"])


    # Get prediction
    prediction = clf.predict(X)[0]
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(X)
    f = plt.figure()
    shap.force_plot(explainer.expected_value, shap_values[0,:], X.iloc[0,:])
    f.savefig("D:/Documents/shap_force_plot.png", bbox_inches='tight', dpi=600)
    # Output prediction
    P = mpimg.imread("shap_force_plot.png")
    st.image(P, caption="shap_force_plot", channels="RGB")
    st.text(f"This patient has a higher probability of {prediction} within 72 hours")
    st_shap(shap.force_plot(explainer.expected_value, shap_values[0,:], X_display.iloc[0,:]), height=200, width=1000)
    st_shap(shap.force_plot(explainer.expected_value, shap_values[:1000,:], X_display.iloc[:1000,:]), height=400, width=1000)
