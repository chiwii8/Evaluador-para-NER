import streamlit as st
import pandas as pd
from typing import List
import csv


def read_plain_file(path_file: str, extract='') -> List[str]:
    data = []
    with open(path_file, 'r', newline='', encoding='utf-8') as file:
        reader_csv = csv.reader(file)

        first_line = True

        for line in reader_csv:
            if first_line:
                first_line = False
                continue

            # Only have 1 element
            data.append(line[0].rstrip(extract))

    return data

# Page Config: See how to upgrade


st.set_page_config(page_title="Script de Evaluación para NER", header_title="Evaluador NER", layout="centered",
                   initial_sidebar_state = "auto", menu_items= {'About': 'This is a Evaluator to calculated the f-measure for binary NER model predictions or do a Baseline with the first predictions and a manual annotation file'}

                   social_icons=[{"url": "https://github.com/chiwii8/Evaluador-para-NER",
                                  "title": "Github",
                                  "classes": "fa-brands fa-github fa-xl",
                                  "color": "#fff"
                                  }
                                 ])



type_of_evaluation = st.radio("Select the type of evaluation",
                              ["***Predictions***, ***Baseline***"],
                              captions=["Evaluation of the predictions result with the division of the positive and "
                                        "negative predictions",
                                        "Evaluation of the prediction file comparing with a manuel annotations file "
                                        "to create a Baseline"],
                              )

if type_of_evaluation == "Predictions":
    upload_valid_file = st.file_uploader("choose a csv positive predictions file", type={"csv"})
    upload_fail_file = st.file_uploader("choose a csv negative predictions file", type={"csv"})
    fail_df = None
    valid_df = None
    if upload_valid_file is not None:
        # read file as dataframe:
        fail_df = pd.read_csv(upload_valid_file, sep=',', encoding='utf-8')

    if upload_fail_file is not None:
        # read file as dataframe:
        valid_df = pd.read_csv(upload_fail_file, sep=',', encoding='utf-8')

    if valid_df is not None & fail_df is not None:
        st.write("The files are valid")
else:
    upload_prediction_file = st.file_uploader("choose a csv prediction file", type={"csv"})
    upload_manual_file = st.file_uploader("choose a csv manual annotation", type={"csv"})
    prediction_file = None
    manual_file = None
    if upload_prediction_file is not None:
        # read file csv as plain:
        prediction_file = read_plain_file(upload_prediction_file)

    if upload_manual_file is not None:
        # read file csv as plain:
        manual_file = read_plain_file(upload_manual_file, extract=';')

    if prediction_file is not None & manual_file is not None:
        st.write("The files are valid")
