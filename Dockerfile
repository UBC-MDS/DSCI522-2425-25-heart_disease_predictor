FROM quay.io/jupyter/minimal-notebook:afe30f0c9ad8

COPY conda-linux-64.lock /tmp/conda-linux-64.lock
COPY requirements.txt /tmp/requirements.txt

USER root
# Switch to root user and install ldmodern so we can render our QMDs as PDFs
RUN sudo apt update \
    && sudo apt install -y lmodern
RUN sudo apt-get update \
    && sudo apt-get install -y make
RUN fix-permissions "/home/${NB_USER}"
USER $NB_UID
# Switch back to non-root user to install packages from conda-linux-64.lock

RUN mamba update --quiet --file /tmp/conda-linux-64.lock
RUN mamba clean --all -y -f
RUN fix-permissions "${CONDA_DIR}"
RUN pip install -r /tmp/requirements.txt