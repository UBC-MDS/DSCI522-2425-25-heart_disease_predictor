# DSCI522-2425-25-heart_disease_predictor

Authors: Anna Nandar, Brian Chang, Celine Habashy, Yeji Sohn

## About

We built models using decision trees and logistic regression algorithms to predict the presence of heart disease based on health-related features. On an unseen dataset, our models achieved an F1 score of 0.834 and an overall accuracy of 0.841. Logistic regression demonstrated better interpretability, with high precision and recall. Some features, such as fasting blood sugar, showed lower importance than anticipated. Moving forward, we plan to explore ensemble methods like Random Forest and Gradient Boosting to improve accuracy and consider incorporating additional clinical data for deeper insights.


The data set that was used in this project is from Cleveland database. It was sourced from the UCI Machine
Learning Repository (R. Detrano, et al. 1989) and can be found
[here](https://archive.ics.uci.edu/dataset/45/heart+disease). This dataset includes features such as age, chest pain type, blood pressure, cholesterol, and more, alongside a binary diagnosis label (presence or absence of heart disease). 

## Report

The final report can be found rendered in HTML
[here](https://ubc-mds.github.io/DSCI522-2425-25-heart_disease_predictor/).

## Usage

Follow the instructions below to reproduce the analysis.

#### Setup

1. Clone this GitHub repository. `git clone https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor.git`

2. Navigate to the repo folder in your IDE

3. Run `conda env create --file environment.yml` to create the heart_disease_522 kernel needed

4. Or if you have conda-lock installed, run `conda-lock install --name heart_disease_522 conda-lock.yml`

5. *Note*: If you have an issue installing the environment, please make sure to have conda-lock and mamba installed:


    `conda install -c conda-forge conda-lock`


    `conda install -c conda-forge mamba`

#### Running the analysis

1. Run heart_disease_predictor_report using the heart_disease_522 kernel. 

## Dependencies

[Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) is
used to manage the software dependencies for this project.
All dependencies are specified int the [`yml`](environment.yml).

Dependencies:
  - python>=3.11,<3.13
  - pip
  - ipykernel
  - nb_conda_kernels
  - scipy
  - matplotlib>=3.2.2
  - scikit-learn
  - requests>=2.24.0
  - seaborn

### Adding a new dependency

1. Add the dependency to the `environment.yml` file on a new branch.

2. Update the `environment.yml` file on your branch.

3. Push the changes to GitHub.

4. Send a pull request to merge the changes into the `main` branch. 

## License

This project was created with the [`MIT License`](LICENSE.md)

## References

<div id="refs" class="references hanging-indent">

<div id="ref-UCI">

Heart disease. UCI Machine Learning Repository. (n.d.). https://archive.ics.uci.edu/dataset/45/heart+disease 

</div>

<div id="ref-Detrano1989">

Detrano, R.C., Jánosi, A., Steinbrunn, W., Pfisterer, M.E., Schmid, J., Sandhu, S., Guppy, K., Lee, S., & Froelicher, V. (1989). International application of a new probability algorithm for the diagnosis of coronary artery disease. The American journal of cardiology, 64 5, 304-10 .

</div>

<div id="ref-Python">

Van Rossum, G., & Drake, F. (2009). Python 3 Reference Manual. CreateSpace.

</div>


<div id="ref-SciLearn">

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825–2830.
</div>


<div id="ref-Deshmukh">

Deshmukh, H. (2020, July 16). Heart disease UCI Diagnosis & Prediction. Medium. https://towardsdatascience.com/heart-disease-uci-diagnosis-prediction-b1943ee835a7 

</div>

<div id="ref-Fahadrehman">

Fahadrehman. (2024, April 28). Heart disease prediction using 9 models. Kaggle. https://www.kaggle.com/code/fahadrehman07/heart-disease-prediction-using-9-models#Evaluation-of-Models

</div>

</div>