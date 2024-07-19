# Evaluador para NER

An evaluator has been created that uses the F1 metric mainly for the evaluation of the prediction files for a Binary NER model.
predictions made for a Binary NER model.

## Prerequisitos

Make
[Docker](https://docs.docker.com/engine/install/ubuntu/)
[Docker Compose](https://docs.docker.com/compose/install/)

## Docker Setup

For simple deployment, a Docker file is included that can be used to deploy the script without the need to set up a custom Python environment.

### Build Docker image

To build the image simply run the following command in the directory that contains the Dockerfile

` Docker build --tag evaluation_ner .`

After building, you can inspect that the image is avaible for running:

` docker images`

## Running the script

To run the evaluation ner image in a container we need to provide the inputs files, and the output directory. To do se we will use mounted volumes.

We might use the following structure for running the script(you can use the current project structure or new one)

<pre>
<code>
project_folder
       | - Eval_files/
                   | - valid_file.csv
                   | - fail_file.csv
       | - Output/
</code>


With the previous structure for our script process we can run the container in windows with the following command from the project directory:

<pre>
    <code>
        docker run --rm `
         --mount type=bind,source="$PWD/Eval_files",target=/home/evaluator/Eval_files `
         --mount type=bind,source="$PWD/Output",target=/home/evaluator/Output `
         evaluation_ner -t labelled
    </code>
</pre>

This command will invoke the main.py script, the arguments for the pipeline are detailed in the Usage section.

# Usage

The script is a simple command argument script that performs 2 things the result of a behavior predictions with a annotated document and the results of the predictions with the files predicted how the True labelled and Others labelled.

You can use this command to see the options of the script:

`py main.py --help`

<pre>
    <code>
        usage: main.py [-h] [-e EVAL_FILE] [-i INPUT_FILE] [-v VALID_FILE] [-f FAIL_FILE] [-l LABEL] [-o OUTPUT_FILE] [-b BETTA_VALUE] [-t TYPE_OF_FILE]         
                                                                                                                                                         
Script que nos permite evaluar los resultados F obtenidos para ficheros csv. Hay dos tipos de evaluación con ficheros planos, y con ficheros etiquetados.
                                                                                                                                                         
options:                                                                                                                                                 
  -h, --help            show this help message and exit                                                                                                  
  -e EVAL_FILE, --eval_file EVAL_FILE
                        Dirección del fichero de evaluación plano
  -i INPUT_FILE, --input_file INPUT_FILE
                        Dirección del fichero a evaluar plano
  -v VALID_FILE, --valid_file VALID_FILE
                        Dirección del fichero etiquetado con los resultados recuperados
  -f FAIL_FILE, --fail_file FAIL_FILE
                        Dirección del fichero etiquetado con los resultados no recuperados
  -l LABEL, --label LABEL
                        Establece la etiqueta que quieres evaluar como no relevante
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Fichero de salida con los resultados obtenidos
  -b BETTA_VALUE, --betta_value BETTA_VALUE
                        Valor de betta para el cálculo de la medida F.
  -t TYPE_OF_FILE, --type_of_file TYPE_OF_FILE
                        Selecciona sobre los tipos de fichero sobre el que vamos a trabajar {plain,labelled}

    </code>
</pre>
