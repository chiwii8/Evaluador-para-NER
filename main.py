# This is a script that evaluated the results between an input_file and a test_file
# Added the evaluation a valid_file and fail_file labelled  with only two labels

# TODO: update the dockerfile and the min_req.txt
# Import classes

from typing import List
import argparse
import os
from Evaluation import EvaluatorPlain,EvaluatorLabelled

seqEval = ['Precision', 'Recall', 'F-measure']
typeOfFile=['plain','labelled']

def is_file(path) -> bool:
    return os.path.isfile(path)


def main():
    parser = argparse.ArgumentParser(
        description="Script que nos permite evaluar los resultados  F obtenidos para ficheros csv. "
                    "Hay dos tipos de evaluación con ficheros planos, y con ficheros etiquetados."
    )
    parser.add_argument('-e', '--eval_file', required=False, type=str,
                        help='Dirección del fichero de evaluación plano')
    parser.add_argument('-i', '--input_file', required=False, type=str,
                        help='Dirección del fichero a evaluar plano')
    parser.add_argument('-v','--valid_file',required=False, type=str,
                        help='Dirección del fichero etiquetado con los resultados recuperados')
    parser.add_argument('-f','--fail_file',required=False, type=str,
                        help='Dirección del fichero etiquetado con los resultados no recuperados')
    parser.add_argument('-l','--label',required=False, type=str, default='0',
                        help='Establece la etiqueta que quieres evaluar como no relevantes')
    parser.add_argument('-o', '--output_file', required=False, type=str, default='./Output/Evaluation_Results.txt',
                        help='Fichero de salida con los resultados obtenidos')
    parser.add_argument('-b', '--betta_value', required=False, type=float, default=1,
                        help='Valor de betta para el cálculo de la medida F.')
    parser.add_argument('-t','--type_of_file',required=True, type=str, default='plain',
                        help='Selecciona sobre los tipos de fichero sobre el que vamos a trabajar {plain,labelled}')

    args = parser.parse_args()

    # Ficheros para texto plano
    test_file: str = args.test_file
    input_file: str = args.input_file

    # Ficheros para dataset etiquetado
    valid_file: str = args.valid_file
    fail_file: str = args.fail_file
    label: str = args.label

    # Datos comunes
    output_file: str = args.output_file
    betta_value: float = args.betta_value
    type_of_file: str = args.type_of_file

    assert type_of_file in typeOfFile, 'El tipo de fichero debe ser plain o labelled'
    assert betta_value > 0, 'Valor de Betta no permitido. Betta > 0 '

    if type_of_file=='plain':
        assert is_file(test_file) & is_file(input_file), 'Uno de los ficheros es inválido'
        evaluator = EvaluatorPlain()
        evaluator.evaluated(test_path=test_file, input_path=input_file, betta_value=betta_value)
        evaluator.save(output_path=output_file)
    else:
        assert is_file(valid_file) & is_file(fail_file), 'Uno de los ficheros es inválido'
        evaluator = EvaluatorLabelled()
        evaluator.evaluated(valid_path=valid_file,fail_path=fail_file, betta_value=betta_value,label=label)
        evaluator.save(output_path=output_file)



if __name__ == '__main__':
    main()
