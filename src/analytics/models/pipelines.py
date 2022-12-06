import pandas as pd
import os
from typing import Dict, Union, Any
import numpy as np
import lightgbm as lgb
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_score
import joblib
from src.core.settings import get_settings

settings = get_settings()

model_base_path = settings.MODEL_PATH


def create_binary_classification_training_model_pipeline(
    training_dataset: pd.DataFrame, target: str, model_id: str = None
) -> Dict[str, float]:

    if os.getenv("ENV") == "test":
        model_path = model_base_path
    else:
        model_path = f"{model_base_path}/{model_id}"

    # Create directory if it doesn't exist
    os.makedirs(model_path, exist_ok=True)

    """
    We first define what will be training set and the targeted column for our prediction

    """
    Y = training_dataset[target]
    X = training_dataset.drop(columns=[target])
    """
    We split to test and training set by using a random_state of 0 in order our code to be 
    reproducible.
    WARNING: We assume that the given dataset is preprocessed. That means than no preprocessing will be performed 
    by us. We have to revisit this step in the near future.
    
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.3, random_state=0
    )
    """
    We use the default set of parameters which produce good results with our baseline dataset.
    WARNING: In the near future we have to grid-search for the optimal parameters for training datasets
    
    The train of our model took locally less than 1 seconds.
    Also we temp save the model in a pkl format.
    WARNING: We have to revisit this step for optimise the resources cost.
    
    """
    clf = LGBMClassifier()
    clf.fit(X_train, y_train)
    joblib.dump(clf, f"{model_path}/lgb_binary.pkl")

    """
    We make some predictions in the X_test and we find the class 
    there by rounding the output. After that we calculate the roc auc curve
    score.
    
    """

    y_pred_1 = clf.predict(X_test)
    y_pred_1 = y_pred_1.round(0)
    y_pred_1 = y_pred_1.astype(int)

    binary_evaluation_report = {}
    # TODO Remove Try Except (Probably find better mock data for dataset_rows)
    try:
        roc_score = roc_auc_score(y_pred_1, y_test)
        binary_evaluation_report["roc_auc_score"] = roc_score
    except ValueError:
        pass

    return clf, binary_evaluation_report


def create_multiclass_classification_training_model_pipeline(
    training_dataset: pd.DataFrame, target: str, model_id: str = None
) -> Dict[str, float]:

    if os.getenv("ENV") == "test":
        model_path = model_base_path
    else:
        model_path = f"{model_base_path}/{model_id}"

    # Create directory if it doesn't exist
    os.makedirs(model_path, exist_ok=True)

    """
    We first define what will be training set and the targeted column for our prediction

    """
    Y = training_dataset[target]
    X = training_dataset.drop(columns=[target])
    """
    We split to test and training set by using a random_state of 0 in order our code to be 
    reproducible. 
    We load the dataset to lightgbm library.
    WARNING: We assume that the given dataset is preprocessed. That means than no preprocessing will be performed 
    by us. We have to revisit this step in the near future.
    
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.3, random_state=0
    )
    d_train = lgb.Dataset(X_train, label=y_train)
    """
    We use a set of parameters which produce good results with our baseline dataset.
    WARNING: In the near future we have to grid-search for the optimal parameters for training datasets
    
    """

    params = {}
    params["verbose"] = -1  # Remove logs
    params["learning_rate"] = 0.03
    params["boosting_type"] = "gbdt"  # GradientBoostingDecisionTree
    params["objective"] = "multiclass"  # Multi-class target feature
    params["metric"] = "multi_logloss"  # metric for multi-class
    params["max_depth"] = 10
    params[
        "num_class"
    ] = 3  # no.of unique values in the target class not inclusive of the end value
    """
    We train our model in 100 epochs - locally this took less than 2 seconds.
    Also we temp save the model in a pkl format.
    WARNING: We have to revisit this step for optimise the resources cost.
    
    """
    clf = lgb.train(params, d_train, 100)  # training the model on 100 epocs
    joblib.dump(clf, f"{model_path}/lgb_multi.pkl")

    """
    We make some predictions in the X_test and we find the class with the higher 
    probability there. After that we calculate the precision_score
    
    """

    y_pred_1 = clf.predict(X_test)
    y_pred_1 = [np.argmax(line) for line in y_pred_1]
    prec_score = precision_score(y_pred_1, y_test, average=None).mean()

    multi_evaluation_report = {}
    multi_evaluation_report["precision"] = prec_score

    return clf, multi_evaluation_report
