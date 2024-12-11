# Makefile
# Brian Chang

#Input Variables
DATA_URL = https://archive.ics.uci.edu/static/public/45/data.csv
PRE_SEED = 42
MDL_FIT_SEED = 123
EDA_FIG_DIR = results/eda_plot
PROC_DIR = data/processed
TBL_DIR = results/tables
MODEL_DIR = results/models

.PHONY: all data figures fits evals clean

all: data figures fits evals report/heart_disease_predictor_report.html report/heart_disease_predictor_report.pdf

# All Data Generation ------------------------------------------------------------------
data : data/raw/raw_heart_disease_data.csv \
data/cleaned/cleaned_heart_disease_data.csv \
${PROC_DIR}/X_test_transformed.csv \
${PROC_DIR}/X_test.csv \
${PROC_DIR}/X_train_transformed.csv \
${PROC_DIR}/X_train.csv \
${PROC_DIR}/y_test.csv

# Raw Data Generation
data/raw/raw_heart_disease_data.csv : scripts/download_data.py
	python scripts/download_data.py --url=${DATA_URL} --write-to=data/raw/

# Cleaned Data Generation
data/cleaned/cleaned_heart_disease_data.csv : scripts/clean_data.py
	python scripts/clean_data.py --raw-data=data/raw/raw_heart_disease_data.csv --write-to=data/cleaned

# Data Preprocessing and Split
# This will generate the train and test split files as well
${MODEL_DIR}/preprocessor.pickle \
${PROC_DIR}/X_test_transformed.csv \
${PROC_DIR}/X_test.csv \
${PROC_DIR}/X_train_transformed.csv \
${PROC_DIR}/X_train.csv \
${PROC_DIR}/y_test.csv \
${PROC_DIR}/y_train.csv : scripts/split_n_preprocess.py
	python scripts/split_n_preprocess.py \
	--raw-data=data/cleaned/cleaned_heart_disease_data.csv \
	--data-to=${PROC_DIR}/ \
	--preprocessor-to=${MODEL_DIR}/ \
	--seed=${PRE_SEED}

# EDA Plot Generations
figures : ${EDA_FIG_DIR}/correlation_heatmap.png ${EDA_FIG_DIR}/diagnosis_distribution.png ${EDA_FIG_DIR}/feature_densities_by_diagnosis.png

# Generate three output EDA plots from 1 script
${EDA_FIG_DIR}/correlation_heatmap.png ${EDA_FIG_DIR}/diagnosis_distribution.png ${EDA_FIG_DIR}/feature_densities_by_diagnosis.png : scripts/eda.py
	python scripts/eda.py --processed-data data/cleaned/cleaned_heart_disease_data.csv --plot-to=${EDA_FIG_DIR}

# Model Fitting ----------------------------------------------------------------------------------
# Generates all model fits and associated images and results
fits: data ${MODEL_DIR}/logistic_regression.pkl \
${TBL_DIR}/logistic_regression/logistic_regression_confusion_matrix.png \
${TBL_DIR}/logistic_regression/logistic_regression_cv_results.csv \
${TBL_DIR}/logistic_regression/logreg_coefficients.csv \
${TBL_DIR}/logistic_regression/logreg_coefficients.png \
${MODEL_DIR}/decision_tree.pkl \
${TBL_DIR}/decision_tree/decision_tree_confusion_matrix.png \
${TBL_DIR}/decision_tree/decision_tree_cv_results.csv


# Fit the logistic regression model and generate data and figures
${MODEL_DIR}/logistic_regression.pkl \
${TBL_DIR}/logistic_regression/logistic_regression_confusion_matrix.png \
${TBL_DIR}/logistic_regression/logistic_regression_cv_results.csv \
${TBL_DIR}/logistic_regression/logreg_coefficients.csv \
${TBL_DIR}/logistic_regression/logreg_coefficients.png : scripts/fit_heart_disease_predictor.py
	python scripts/fit_heart_disease_predictor.py \
	--x-train=${PROC_DIR}/X_train_transformed.csv \
	--y-train=${PROC_DIR}/y_train.csv \
	--model=logistic_regression \
	--output-dir=results \
	--random-state=${MDL_FIT_SEED}

# Fit the decision tree model and generate data and figures
${MODEL_DIR}/decision_tree.pkl \
${TBL_DIR}/decision_tree/decision_tree_confusion_matrix.png \
${TBL_DIR}/decision_tree/decision_tree_cv_results.csv : scripts/fit_heart_disease_predictor.py
	python scripts/fit_heart_disease_predictor.py \
	--x-train=${PROC_DIR}/X_train_transformed.csv \
	--y-train=${PROC_DIR}/y_train.csv \
	--model=decision_tree \
	--output-dir=results \
	--random-state=${MDL_FIT_SEED}

# Model Evaluation (Scoring)
# Generate all classification reports
evals: ${TBL_DIR}/decision_tree/classification_report.csv ${TBL_DIR}/logistic_regression/classification_report.csv

# Generate classification report for Decision Tree
${TBL_DIR}/decision_tree/classification_report.csv : scripts/evaluate_heart_disease_predictor.py
	python scripts/evaluate_heart_disease_predictor.py \
	--x-test=${PROC_DIR}/X_test_transformed.csv \
	--y-test=${PROC_DIR}/y_test.csv \
	--pipeline-from=${MODEL_DIR}/decision_tree.pkl \
	--results-to=${TBL_DIR}/decision_tree

# Generate classification report for Logistic Regression
${TBL_DIR}/logistic_regression/classification_report.csv : scripts/evaluate_heart_disease_predictor.py
	python scripts/evaluate_heart_disease_predictor.py \
	--x-test=${PROC_DIR}/X_test_transformed.csv \
	--y-test=${PROC_DIR}/y_test.csv \
	--pipeline-from=${MODEL_DIR}/logistic_regression.pkl \
	--results-to=${TBL_DIR}/logistic_regression

# Report Generation
report/heart_disease_predictor_report.html report/heart_disease_predictor_report.pdf : report/heart_disease_predictor_report.qmd
	quarto render report/heart_disease_predictor_report.qmd --to html
	quarto render report/heart_disease_predictor_report.qmd --to pdf

# Remove folder/files generated by this Makefile
clean :
	rm -rf data/*
	rm -rf results/*
	rm -f report/heart_disease_predictor_report.html
	rm -f report/heart_disease_predictor_report.pdf