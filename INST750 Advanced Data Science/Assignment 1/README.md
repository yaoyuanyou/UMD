## Spam Message Classifier
This assignment is based on a dataset found on [Kaggle](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset). 

# Introduction
The dataset contains 5,572 English SMS messages, which are tagged ham (legitimate, not spam) or spam. The chosen dataset meets three key criteria that make it well-suited for this study.
- Its moderate size ensures that computational demands remain manageable, allowing the SVM model (which not originally supports CUDA) to process the data eﬀiciently.
- As a Kaggle dataset, it is well-structured and comprehensive, facilitating reliable analysis.
- Its use enables comparisons with models developed by machine learning professionals worldwide, providing opportunities for further optimization and improvement.

# Methods
After data preprocessing and cleaning, the data is highly **IMBALANCED** and will deal this issue.
![Label Distribution](https://github.com/yaoyuanyou/UMD/blob/288660b71bdf08501fb8f2fa54120f0478a065d4/INST750%20Advanced%20Data%20Science/Assignment%201/img/label-dist.png)
In the evaluation phase, I prioritize **recall** because spam message contains links that will steal personal information. If fraudulent text messages are not detected, there is an additional risk of personal information being leaked. Therefore, recall is used as the metrics to evaluate and tune models performances.

# RoBERTa Model
To deal with the imbalanced issue. I weighted the sample using the inverse of frequency. In the loss function, class weights are taken into account. Below is a runtime screenshot:
![Model Training Performance](https://github.com/yaoyuanyou/UMD/blob/288660b71bdf08501fb8f2fa54120f0478a065d4/INST750%20Advanced%20Data%20Science/Assignment%201/img/RoBERTa-perf.png)

# Evaluation
I also built **LSTM** and **SVM** as baselines to compare with the state-of-art language model. The Transformer-based model performs **10%** better than traditional ML/DL models. Here is a comparison chart:
|  Metrics  |  SVM | RoBERTa | LSTM |
|:---------:|:----:|:-------:|:----:|
| precision | 0.95 |   0.99  | 0.98 |
|   recall  |  090 |   0.98  | 0.85 |
| f1 score  | 0.93 | 0.99    | 0.91 |
| roc_auc   | 0.98 | 1.00    | 0.97 |
Here is a visualized **ROC Curve**:
![ROC Curve Comparison](https://github.com/yaoyuanyou/UMD/blob/288660b71bdf08501fb8f2fa54120f0478a065d4/INST750%20Advanced%20Data%20Science/Assignment%201/img/models-eval.png)

# Result
These models represent different levels of complexity and are chosen to evaluate their suitability for classifying the dataset. Overall, RoBERTa outperforms other two models. LSTM has good precision, meaning it won’t misclassify legitimate messages. However, its ability of identifying actual positives(spam) messages is worse than SVM. Comparing to advanced models, SVM performance is not enough.

The training speed and the evaluation results surprise me as well. On the one hand, the small dataset makes it easy to train. On the other hand, the dataset may have similar pattern, which means the model may be overfitted. When the size goes larger, the prediction ability decreases. So for further study, I would like to use other sources to test models robustness.
