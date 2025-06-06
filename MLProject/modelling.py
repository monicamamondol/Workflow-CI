import mlflow
import pandas as pd
import numpy as np
import os
import sys
import warnings
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(42)

    # Ambil path folder dataset dari argumen ke-3 atau gunakan default folder
    dataset_dir = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_preprocessing")

    # Load dataset CSV dari folder tersebut
    x_train = pd.read_csv(os.path.join(dataset_dir, "x_train.csv"))
    y_train = pd.read_csv(os.path.join(dataset_dir, "y_train.csv")).values.ravel()
    x_test = pd.read_csv(os.path.join(dataset_dir, "x_test.csv"))
    y_test = pd.read_csv(os.path.join(dataset_dir, "y_test.csv")).values.ravel()

    # Ambil parameter model dari argumen
    n_estimators = int(sys.argv[1]) if len(sys.argv) > 1 else 505
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 37

    input_example = x_train.iloc[:5]

    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
        model.fit(x_train, y_train)

        # Prediksi dan evaluasi
        y_pred = model.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)

        # Logging model dan metrik
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            input_example=input_example
        )
        model.fit(x_train, y_train)
        # Log metrics
        accuracy = model.score(x_test, y_test)
        mlflow.log_metric("accuracy", accuracy)
