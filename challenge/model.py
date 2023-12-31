import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
import warnings
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from datetime import datetime
import joblib

warnings.filterwarnings('ignore')


from typing import Tuple, Union, List

class DelayModel:

    def __init__(
        self
    ):
        self._model = None # Model should be saved in this attribute.
        self.model_weights = None
        self.scale = None

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
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
        #Add get_period column to dataset
        def get_period_day(date):
            date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
            morning_min = datetime.strptime("05:00", '%H:%M').time()
            morning_max = datetime.strptime("11:59", '%H:%M').time()
            afternoon_min = datetime.strptime("12:00", '%H:%M').time()
            afternoon_max = datetime.strptime("18:59", '%H:%M').time()
            evening_min = datetime.strptime("19:00", '%H:%M').time()
            evening_max = datetime.strptime("23:59", '%H:%M').time()
            night_min = datetime.strptime("00:00", '%H:%M').time()
            night_max = datetime.strptime("4:59", '%H:%M').time()
            
            if(date_time > morning_min and date_time < morning_max):
                return 'mañana'
            elif(date_time > afternoon_min and date_time < afternoon_max):
                return 'tarde'
            elif(
                (date_time > evening_min and date_time < evening_max) or
                (date_time > night_min and date_time < night_max)
            ):
                return 'noche'
    
        data['period_day'] = data['Fecha-I'].apply(get_period_day)

        #Add high_season column to dataset
        def is_high_season(fecha):
            fecha_año = int(fecha.split('-')[0])
            fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            range1_min = datetime.strptime('15-Dec', '%d-%b').replace(year = fecha_año)
            range1_max = datetime.strptime('31-Dec', '%d-%b').replace(year = fecha_año)
            range2_min = datetime.strptime('1-Jan', '%d-%b').replace(year = fecha_año)
            range2_max = datetime.strptime('3-Mar', '%d-%b').replace(year = fecha_año)
            range3_min = datetime.strptime('15-Jul', '%d-%b').replace(year = fecha_año)
            range3_max = datetime.strptime('31-Jul', '%d-%b').replace(year = fecha_año)
            range4_min = datetime.strptime('11-Sep', '%d-%b').replace(year = fecha_año)
            range4_max = datetime.strptime('30-Sep', '%d-%b').replace(year = fecha_año)
            
            if ((fecha >= range1_min and fecha <= range1_max) or 
                (fecha >= range2_min and fecha <= range2_max) or 
                (fecha >= range3_min and fecha <= range3_max) or
                (fecha >= range4_min and fecha <= range4_max)):
                return 1
            else:
                return 0
            
        data['high_season'] = data['Fecha-I'].apply(is_high_season)

        #Add min_diff column to dataset
        def get_min_diff(data):
            fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
            fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
            min_diff = ((fecha_o - fecha_i).total_seconds())/60
            return min_diff
        
        data['min_diff'] = data.apply(get_min_diff, axis = 1)

        #Add delay column to dataset
        threshold_in_minutes = 15
        data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)

        #Spliting the data (preparing for model training)
        training_data = shuffle(data[['OPERA', 'MES', 'TIPOVUELO', 'SIGLADES', 'DIANOM', 'delay']], random_state = 111)

        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix = 'OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix = 'TIPOVUELO'), 
            pd.get_dummies(data['MES'], prefix = 'MES')], 
            axis = 1
        )

        target = data['delay']

        x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.33, random_state=42)

        top_10_features = [
            "OPERA_Latin American Wings",
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]

        #Balancing data to improve model's performance
        n_y0 = len(y_train[y_train == 0])
        n_y1 = len(y_train[y_train == 1])
        self.model_weights = {1: n_y0/len(y_train), 0: n_y1/len(y_train)}

        #Improve the model
        x_train2, x_test2, y_train2, y_test2 = train_test_split(features[top_10_features], target, test_size = 0.33, random_state = 42)

        target = pd.DataFrame(y_train2, columns=['delay'])
        features = x_train2

        if target_column:
            return features, target
        else:
            return x_test2


    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        #Train the model using LR
        self._model = LogisticRegression(class_weight=self.model_weights)
        self._model.fit(features, target)


    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        #Make predictions
        reg_y_preds = self._model.predict(features)
        reg_y_preds_list = reg_y_preds.tolist() 
        return reg_y_preds_list
    

    def save(self, filename: str) -> None:
        """
        Save the model to a file.

        Args:
            filename (str): The path to the file where the model will be saved.
        """
        joblib.dump(self._model, filename)


    def load(self, filename: str) -> None:
        """
        Load the model from a file.

        Args:
            filename (str): The path to the file where the model is saved.
        """
        self._model = joblib.load(filename)
    

if __name__ == "__main__":
    # Carga tus datos desde un archivo CSV (reemplaza 'tu_archivo_de_datos.csv' con tu archivo real)
    data = pd.read_csv(filepath_or_buffer="./../data/data.csv")

    # Crea una instancia de la clase DelayModel
    delay_model = DelayModel()

    # Preprocesa tus datos
    features, target = delay_model.preprocess(data, target_column="delay")

    # Entrena el modelo
    delay_model.fit(features, target)

    # Guarda el modelo en un archivo
    delay_model.save(filename = "model_delay.pkl")