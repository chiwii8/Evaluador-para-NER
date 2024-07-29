import streamlit as st
import pandas as pd
from typing import List
import csv
from io import StringIO
from Evaluation import EvaluatorPlainBinary, EvaluatorLabelledBinary


def open_file_plain(plain_file, extract='') -> List[str]:
    data = []
    file_content = plain_file.read().decode('utf-8')
    file = StringIO(file_content)
    reader_csv = csv.reader(file)

    for row in reader_csv:
        data.append(row[0].rstrip(extract))
    return data


def table_confusion_matrix(results):
    # Set the First Row
    aux, row1, aux = st.columns(3, vertical_alignment='center')
    with row1:
        st.write("""### Confusión Matrix""")
        st.write("""### Real Values""")

    # Set the Second Row
    row2, row3 = st.columns([1, 3], vertical_alignment='center')

    with row2:
        st.write("""### Predictions""")

    with row3:
        confusion_matrix = pd.DataFrame({
            '': ['Positive', 'Negative'],
            "Positive": [results['True_Positive'], results['False_Positive']],
            "Negative": [results['False_Negative'], results['True_Negative']]
        })
        st.dataframe(confusion_matrix)


st.set_page_config(page_title='Script for binary NER predictions', layout='wide', initial_sidebar_state='auto',
                   menu_items={
                       'About': 'This is a Evaluator to calculated the f-measure for binary NER model predictions or '
                                'de a Baseline with the first predictions and a manual annotation file'})

st.sidebar.title('About')
st.sidebar.write('This is a **Evaluator** to calculated the f-measure for binary NER model predictions or de a Baseline'
                 ' with the first predictions and a manual annotation file')
st.sidebar.divider()
st.sidebar.title('Predictions files')
st.sidebar.write('You can divided in two files, one with the elements with the elements predicted postive and the '
                 'other file with the elements predicted negative')
st.sidebar.divider()
st.sidebar.title('Baseline')
st.sidebar.write('You can use two files, one with the predictions of the model and a manual annotation file with '
                 'the correct predictions')

# Logo and Navigation
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.title('Evaluator For NER Predictions')

    type_of_evaluation = st.radio('Select the type of evaluation',
                                  ['***Predictions***', '***Baseline***'],
                                  captions=["Evaluation of the predictions result with the division of the positive and"
                                            " negative predictions",
                                            "Evaluation of the prediction file comparing a manuel annotations file"
                                            " with predictions to create a Baseline"])
    # When we are using the predictions files

    if type_of_evaluation == '***Predictions***':
        upload_valid_file = st.file_uploader("choose a csv positive predictions file", type={"csv"})
        upload_fail_file = st.file_uploader("choose a csv negative predictions file", type={"csv"})
        fail_df = None
        valid_df = None
        if upload_valid_file is not None:
            # read file as dataframe:
            valid_df = pd.read_csv(upload_valid_file, sep=',', encoding='utf-8')
            st.dataframe(valid_df, height=175, use_container_width=True)
        if upload_fail_file is not None:
            # read file as dataframe:
            fail_df = pd.read_csv(upload_fail_file, sep=',', encoding='utf-8')
            st.dataframe(fail_df, height=175, use_container_width=True)

        if valid_df is not None and fail_df is not None:
            if st.button('Evaluation'):
                evaluator = EvaluatorLabelledBinary('0')
                result = evaluator.evaluated_parametric(valid_file=valid_df, fail_file=fail_df, betta_value=1)
                tab_result, tab_matrix = st.tabs(["Metric", "Confusion Matrix"])
                with tab_result:
                    st.write('**Results of the Evaluation:**')
                    st.write(f"***Precision:*** {result['precision']}")
                    st.write(f"***Recall:*** {result['recall']}")
                    st.write(f"***F1-Measure:*** {result['f_measure']}")
                with tab_matrix:
                    table_confusion_matrix(result)

    elif type_of_evaluation == '***Baseline***':
        upload_prediction_file = st.file_uploader("choose a csv prediction file", type=["csv"])
        upload_manual_file = st.file_uploader("choose a csv manual annotation", type=["csv"])
        prediction_file = None
        manual_file = None

        if upload_prediction_file is not None:
            # read file csv as plain:
            prediction_file = open_file_plain(upload_prediction_file)
            st.dataframe(prediction_file, height=175, use_container_width=True)

        if upload_manual_file is not None:
            # read file csv as plain:
            manual_file = open_file_plain(upload_manual_file, extract=';')
            st.dataframe(manual_file, height=175, use_container_width=True)

        if prediction_file is not None and manual_file is not None:
            if st.button('Evaluation'):
                evaluator = EvaluatorPlainBinary()
                result = evaluator.evaluated_parametric(test_file=prediction_file, input_file=manual_file,
                                                        betta_value=1)

                tab_result, tab_matrix = st.tabs(["Metric", "Confusion Matrix"])
                with tab_result:
                    st.write('**Results of the Evaluation:**')
                    st.write(f"***Precision:*** {result['precision']}")
                    st.write(f"***Recall:*** {result['recall']}")
                    st.write(f"***F1-Measure:*** {result['f_measure']}")
                with tab_matrix:
                    table_confusion_matrix(result)
