# Changelog
*Modified from our original combined [issue](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/issues/64)*
## Feedback Sources

### [Peer Review Feedback](https://github.com/UBC-MDS/data-analysis-review-2024/issues/12#issuecomment-2537520503)

### [Milestone 1 Feedback](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/issues/35)

### Milestone 2 Feedback:

- Feedback from Milestone 2 was to change the docker-compose file to not specify latest. This was addressed in more details in this [Issue](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/issues/88)

---

In general, all feedback from Milestones and most from peer review were addressed in fixes. A minority few from peer reviews were addressed by explaining our rationale for we didn't follow their suggestions. These specific explanations each have their own GitHub Issues and are linked to within their respective bullet point below. 

*Note: Some fixes may have been addressed together in one big PR*

## Feedback Fixes, Commits, and Pull Requests

### **Report**

- Ensure EDA is conducted exclusively on the training dataset to prevent data leakage.
  - Addressed by:
    - [This commit](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/79/commits/53de6cb46fa01639ee9fe745a43c6669ea679050)
    - [This commit](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/79/commits/15cf4c5586995dd7154f4ee238a08d10b5813d93)

- [Expand the "Methods & Results" section with more explanatory notes and keep the "Discussion" focused on providing additional details. Discuss the motivation behind your scoring metrics in the context of "Heart Disease Prediction".](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/89)

- [Provide more detail in the "Methods" section on how the dataset was split for training and testing (e.g., 70-30 split or cross-validation)](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/89)

- [The rendered reports in the repository are different from those created by make all. They are not up-to-date.](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/90)

- [References: Please ensure all softwares used in generating the analysis and report are properly attributed.](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/89)

---

### **Documentation**

- [Pin `requests` version to `==2.24.0` instead of `>=2.24.0`.](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/commit/92e9e74bc2b7b78f7fcb1cf1958d242d9187b836)

- [In the dockerfile, the port is mapped to 34651. However, the message in terminal still shows 8888. This may confuse people who do not carefully read instructions. Is there any way to resolve it?](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/issues/75)

- [Split the quarto render commands into separate lines for clarity:](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/issues/74)

  ```bash
  quarto render heart_disease_predictor_report.qmd --to html
  quarto render heart_disease_predictor_report.qmd --to pdf
  ```

---

### **Code**

- [Ensure consistent script naming (e.g., some scripts use `_heart_disease_predictor`, others do not).](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/commit/c1df4330520f8f65728530e5e9b12ed9b8465860)

- [Implement more specific exceptions (e.g., `InvalidColumnTypeError`, `MissingValueError`) instead of generic ones like `ValueError`.](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/commit/d1e3849dfffb0aa2e32b599f7ac7f58c42afb12d)

- Move helper functions into separate modules for better organization.
  - Addressed by:
    - [This commit](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/commit/fc240272756a1cde597eacd3924520ff1713c34f)
    - [This commit](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/commit/be9ba5c8b969124a002e793d4f22840f44945650)

- Modularize functions to improve code clarity and reusability & Abstract code from the `main()` function into separate functions to improve structure and readability.
  - Addressed by:
    - [This PR](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/66)
    - [This PR](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/79)
    - [This PR](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/84)
    - [This PR](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/83)

- Unit Testing: Adding unit tests for each validation function would ensure the correctness of the logic when applied to different datasets. It can help catch edge cases and confirm that each function works as expected.
  - Addressed by:
    - [This PR](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/66)
    - [This PR](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/79)
    - [This PR](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/84)
    - [This PR](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/83)

---

### Milestone 1 Specific Feedback:

#### The below 6 are all addressed in [this PR](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/51)

- Add proper email to code of conduct
- Remove .ds_store file
- Discuss importance/limitation of findings in Abstract/summary
- Clearly identify question in introduction
- Add all references to the dataset in Introduction
- More clearly define target/response variable in Introduction

#### The below 3 are all addressed in [this PR](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/pull/89)

- Important methodology descriptions missing (e.g., did not explain in narrative what metric was being used for model parameter optimization)
- Some important results not displayed
- Findings from project need to be linked back to application domain and questions

---

### **Organization**

- [Move all environment files into a separate folder to tidy up the repository. #72](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/issues/72)
- [Remove redundant lock files](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/issues/71)
- [Organize files in the `report` folder into subfolders for better structure.](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/commit/704fb0f46221944bcf70efff16d43fae6b21e9d5)

---

### **Warnings**

- [Address and resolve the warning messages that appear when running `make all`. Follow the instructions provided in the messages to eliminate them.](https://github.com/UBC-MDS/DSCI522-2425-25-heart_disease_predictor/commit/ecf10b313713e36ddaed93f853acd98397680faa)

---
