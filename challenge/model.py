import pandas as pd
import numpy as np

from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from typing import List


class DelayModel:
    TOP_FEATURES = [
        "OPERA_Latin American Wings",
        "MES_7",
        "MES_10",
        "OPERA_Grupo LATAM",
        "MES_12",
        "TIPOVUELO_I",
        "MES_4",
        "MES_11",
        "OPERA_Sky Airline",
        "OPERA_Copa Air",
    ]

    def __init__(self):
        self._model = None  # Model should be saved in this attribute.
        self._threshold_in_minutes = 15
        self.columns = None

    def preprocess(self, data: pd.DataFrame, target_column: str = None):
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        data["min_diff"] = data.apply(self.__get_min_diff, axis=1)

        features = pd.concat(
            [
                pd.get_dummies(data["OPERA"], prefix="OPERA"),
                pd.get_dummies(data["TIPOVUELO"], prefix="TIPOVUELO"),
                pd.get_dummies(data["MES"], prefix="MES"),
            ],
            axis=1,
        )
        self.columns = features.columns
        features = features[self.TOP_FEATURES]

        if target_column:
            target = pd.DataFrame(
                np.where(data["min_diff"] > self._threshold_in_minutes, 1, 0),
                columns=[target_column],
            )
            return features, target
        else:
            return features

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        x_train, x_test, y_train, y_test = train_test_split(
            features, target, test_size=0.33, random_state=42
        )
        n_y0 = len(y_train[y_train["delay"] == 0])
        n_y1 = len(y_train[y_train["delay"] == 1])
        self._model = LogisticRegression(
            class_weight={1: n_y0 / len(y_train), 0: n_y1 / len(y_train)}
        )
        self._model.fit(x_train, y_train)

        y_preds = self._model.predict(x_test)
        print(classification_report(y_test, y_preds))

        return

    def predict(self, features: pd.DataFrame) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """
        predictions = self._model.predict(features.values)

        return predictions.tolist()

    def __get_min_diff(self, data: pd.DataFrame):
        fecha_o = datetime.strptime(data["Fecha-O"], "%Y-%m-%d %H:%M:%S")
        fecha_i = datetime.strptime(data["Fecha-I"], "%Y-%m-%d %H:%M:%S")
        min_diff = ((fecha_o - fecha_i).total_seconds()) / 60
        return min_diff
