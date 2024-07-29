from typing import List
import os
import csv
import pandas as pd


def open_file_plain(path_file: str, extract='') -> List[str]:
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


def open_file_labelled(path_file: str) -> pd.DataFrame:
    csv_file = pd.read_csv(path_file, sep=',', encoding='utf-8')
    return csv_file


def calculated_f(betta: float, precision: float, recall: float) -> float:
    print(f'Calculated the f measure with betta value `{betta}`')
    betta_pow = pow(betta, 2)
    f_measure_top = (betta_pow + 1) * precision * recall
    f_measure_bot = (betta_pow * precision) + recall
    f_measure = f_measure_top / f_measure_bot
    if f_measure < 0:
        f_measure = 0

    return f_measure


class Evaluator:
    def __init__(self):
        super().__init__()
        self.confusion_matrix = {
            "True_Positive": 0,  # Relevantes recuperados
            "True_Negative": 0,  # No Relevantes No recuperados
            "False_Positive": 0,  # No Relevantes recuperados
            "False_Negative": 0  # Relevantes no recuperado
        }
        self.results = None

    def calculated_confusion_matrix(self):
        raise NotImplementedError('Está clase no implementa esté método')

    def calculated_precision(self) -> float:
        print('Calculated the precision measure')
        tp = self.confusion_matrix["True_Positive"]
        fp = self.confusion_matrix["False_Positive"]
        return tp / (tp + fp)

    def calculated_recall(self) -> float:
        print('Calculated the precision recall measure')
        tp = self.confusion_matrix["True_Positive"]
        fn = self.confusion_matrix["False_Negative"]
        return tp / (tp + fn)

    def save(self, output_path: str) -> None:
        print(f'The results of the evaluation is save in `{os.path.basename(output_path)}`')
        with open(output_path, 'w') as file:
            file.write(self.results)


class EvaluatorPlainBinary(Evaluator):
    def __init__(self):
        super().__init__()
        self.input_file = None
        self.test_file = None

    def evaluated(self, test_path: str, input_path: str, betta_value: float) -> None:
        print(f'Start the evaluation of the file `{os.path.basename(input_path)}`')
        # read the input files
        self.test_file = open_file_plain(test_path, extract=';')
        self.input_file = open_file_plain(input_path, extract='')

        # Calculated the confusion_matrix values
        self.calculated_confusion_matrix()

        # Once calculated the confusion matrix values, we can start calculating the precision, recall and f-measure
        precision = self.calculated_precision()
        recall = self.calculated_recall()

        f_measure = calculated_f(betta=betta_value, precision=precision, recall=recall)

        self.results = f"""Results of the evaluation
                Precision:`{precision}`
                Recall: `{recall}`
                F_measure `{f_measure}`
                Matrix-Confusion
                TP: `{self.confusion_matrix['True_Positive']}`
                TN: `{self.confusion_matrix['True_Negative']}`
                FP: `{self.confusion_matrix['False_Positive']}`
                FN: `{self.confusion_matrix['False_Negative']}`
                """

        print(self.results)

    def evaluated_parametric(self, test_file: List[str], input_file: List[str], betta_value: float):
        print(f'Start the evaluation of the files ')
        # read the input files
        self.test_file = test_file
        self.input_file = input_file

        # Calculated the confusion_matrix values
        self.calculated_confusion_matrix()

        # Once calculated the confusion matrix values, we can start calculating the precision, recall and f-measure
        precision = self.calculated_precision()
        recall = self.calculated_recall()

        # Finally save the results in a parameter and return it
        results = self.confusion_matrix
        results['precision'] = precision
        results['recall'] = recall
        results['f_measure'] = calculated_f(betta=betta_value, precision=precision, recall=recall)

        return results

    def calculated_confusion_matrix(self):
        print('Calculated the confusion matrix')

        for _ in self.input_file:
            if _ in self.test_file:
                self.confusion_matrix["True_Positive"] += 1
            else:
                self.confusion_matrix["False_Positive"] += 1

        for _ in self.test_file:
            if _ not in self.input_file:
                self.confusion_matrix["False_Negative"] += 1


class EvaluatorLabelledBinary(Evaluator):
    def __init__(self, label: str):
        super().__init__()
        self.valid_file = None
        self.fail_file = None
        self.label = label

    def evaluated(self, valid_path: str, fail_path: str, betta_value: float) -> None:
        print(f'Start the evaluation of the files.')

        self.valid_file = open_file_labelled(valid_path)
        self.fail_file = open_file_labelled(fail_path)

        # Calculated the confusion_matrix values
        self.calculated_confusion_matrix()

        # Once calculated the confusion matrix values, we can start calculating the precision, recall and f-measure
        precision = self.calculated_precision()
        recall = self.calculated_recall()

        f_measure = calculated_f(betta=betta_value, precision=precision, recall=recall)

        self.results = f"""Results of the evaluation
                        Precision:`{precision}`
                        Recall: `{recall}`
                        F_measure `{f_measure}`
                        Matrix-Confusion:
                        TP: `{self.confusion_matrix['True_Positive']}`
                        TN: `{self.confusion_matrix['True_Negative']}`
                        FP: `{self.confusion_matrix['False_Positive']}`
                        FN: `{self.confusion_matrix['False_Negative']}`"""

        print(self.results)

    def evaluated_parametric(self, valid_file: pd.DataFrame, fail_file: pd.DataFrame, betta_value: float):
        print(f'Start the evaluation of the files.')
        # read the input files
        self.valid_file = valid_file
        self.fail_file = fail_file

        # Calculated the confusion_matrix values
        self.calculated_confusion_matrix()

        # Once calculated the confusion matrix values, we can start calculating the precision, recall and f-measure
        precision = self.calculated_precision()
        recall = self.calculated_recall()

        # Finally save the results in a parameter and return it
        results = self.confusion_matrix
        results['precision'] = precision
        results['recall'] = recall
        results['f_measure'] = calculated_f(betta=betta_value, precision=precision, recall=recall)

        return results

    def calculated_confusion_matrix(self):
        print('Calculated the confusion matrix')

        for ner_tags in self.valid_file['ner_tags']:
            try:
                index = ner_tags.index(self.label)
                self.confusion_matrix['False_Positive'] += 1
            except ValueError:
                self.confusion_matrix['True_Positive'] += 1

        for ner_tags in self.fail_file['ner_tags']:
            try:
                index = ner_tags.index(self.label)
                self.confusion_matrix['True_Negative'] += 1
            except ValueError:
                self.confusion_matrix['False_Negative'] += 1
