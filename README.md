# DSCI522-2425-25-heart_disease_predictor

Authors: Anna Nandar, Brian Chang, Celine Habashy, Yeji Sohn

## About

We built models using decision trees and logistic regression algorithms to predict the presence of heart disease based on health-related features. On an unseen dataset, our models achieved an overall accuracy of 84.4%. Logistic regression demonstrated better interpretability, with high precision and recall. Some features, such as fasting blood sugar, showed lower importance than anticipated. Moving forward, we plan to explore ensemble methods like Random Forest and Gradient Boosting to improve accuracy and consider incorporating additional clinical data for deeper insights.

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

2. Navigate to root of the project folder in your IDE where you have cloned it.

#### Running the analysis

1. At the root of the project in a terminal, enter
    ```docker-compose up```
2. In the terminal, navigate to the URL in the docker compose logs that start with the `http://127.0.0.1:PORT_NUMBER/lab?token=`

*NOTE*: You will need to replace the port number with PORT 34651 to navigate to the proper port inside docker

*NOTE 2*: If you are taken to an authentication screen, please take the token from the logs from where you saw `http://127.0.0.1:PORT_NUMBER/lab?token=...token..is..here...`, and paste it into the login screen's login with token

*NOTE 3*: If you are getting any errors with libraries or such, you may want to make sure the docker container and image are up to date. We've found deleting the image completely from your Docker Desktop the best method to ensure it has all been deleted, and the latest image will be pulled.

3. To run the analysis and regenerate the data, open a terminal (in the docker jupyter lab) and run the following commands:

*NOTE*: You may want to run the commands one at a time if your terminal disconnects.
```
python scripts/download_data.py --url="https://archive.ics.uci.edu/static/public/45/data.csv" --write-to="data/raw/"

python scripts/clean_data.py --raw-data="data/raw/raw_heart_disease_data.csv" --write-to="data/cleaned/"

python scripts/split_n_preprocess.py --raw-data data/processed/processed_heart_disease_data.csv --data-to="data/processed/" --preprocessor-to=“results/models/“ --seed 42

python scripts/eda.py --processed-data data/cleaned/cleaned_heart_disease_data.csv --plot-to results/eda_plot

python scripts/fit_heart_disease_predictor.py --x-train data/processed/X_train_transformed.csv --y-train data/processed/y_train.csv --model decision_tree --output-dir results/ --random-state 123

python scripts/fit_heart_disease_predictor.py --x-train data/processed/X_train_transformed.csv --y-train data/processed/y_train.csv --model logistic_regression --output-dir results/ --random-state 123

python scripts/evaluate_heart_disease_predictor.py --x-test data/processed/X_test_transformed.csv --y-test data/processed/y_test.csv --pipeline-from results/models/decision_tree.pkl --results-to results/tables/decision_tree

python scripts/evaluate_heart_disease_predictor.py --x-test data/processed/X_test_transformed.csv --y-test data/processed/y_test.csv --pipeline-from results/models/logistic_regression.pkl --results-to results/tables/logistic_regression
```

4. To render the PDF and HTML

    4.1 Navigate to the report folder in your terminal
    
    4.2 Run the following

      `quarto render heart_disease_predictor_report.qmd --to html`
      `quarto render heart_disease_predictor_report.qmd --to pdf`

#### Clean up
1. To make sure the docker container was properly cleaned up, after typing `ctrl` + `c` in the terminal where you launched the docker container, type `docker-compose rm`

## Dependencies
[Docker](https://www.docker.com/) is used to create reproducible instances of this project. The docker image used is based on the `quay.io/jupyter/minimal-notebook:notebook-7.0.6 image.` Additional dependencies aside from this image and the below dependencies by Conda are specified in the [Dockerfile](Dockerfile)

[Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) is also used to manage the software dependencies for this project.
All dependencies are specified in the [`environment.yml`](environment.yml).

```
Dependencies:
  - python=3.11
  - pip=24.3.1
  - pandas=2.2.2
  - ipykernel=6.29.5
  - nb_conda_kernels=2.5.1
  - scipy=1.14.1
  - matplotlib>=3.2.2
  - scikit-learn=1.5.2
  - requests>=2.24.0
  - seaborn=0.13.2
  - ucimlrepo=0.0.7
  - pandera=0.20.2
  - quarto=1.5.57
  - click=8.1.7
  - tabulate=0.9.0
  - lmodern (this is installed by the Dockerfile)
  - deepchecks=0.18.1
```
## Developer Notes
### Developer Dependencies
1. `conda` (version 24.11.0 or higher)
2. `conda-lock` (version 2.5.7 or higher)
3. [Docker](https://www.docker.com/) 
### Adding a new dependency

1. Add the dependency to the `environment.yml` file on a new branch.

2. Run `conda-lock -k explicit --file environment.yml -p linux-64` to update the `conda-linux-64.lock` file

3. Re-build the Docker image locally to ensure it still runs.

4. Test the container locally by running it and ensuring your new dependencies are working

5. Push the changes to GitHub.

6. Update your local docker-compose.yml file on your branch to use the new container image (line 3 in the docker-compose.yml file where it starts with "image:..."

*Note: Right now it will always use the latest Docker Image anyways so for Milestone 2 Step 6 is not needed*

7. Send a pull request to merge the changes into the `main` branch. 

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

<div id="ref-pandas">

team, The pandas development. 2020. “Pandas-Dev/Pandas: Pandas.” Zenodo. https://doi.org/10.5281/zenodo.3509134.
</div>

<div id="ref-pandera">

Bantilan, Niels. 2020. “Pandera: Statistical Data Validation of Pandas Dataframes.” In Proceedings of the 19th Python in Science Conference, edited by Meghann Agarwal, Chris Calloway, Dillon Niederhut, and David Shupe, 116–24. https://doi.org/ 10.25080/Majora-342d178e-010 .
</div>

</div>