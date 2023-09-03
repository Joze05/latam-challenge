from fastapi import FastAPI , HTTPException
import pandas as pd
from pydantic import BaseModel, validator
from model import DelayModel
from typing import List

app = FastAPI()

# Crea una instancia de la clase DelayModel y carga el modelo entrenado
delay_model = DelayModel()
modelo_guardado = "./model_delay.pkl"

class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int

    @validator('OPERA')
    def opera_must_be_valid(cls, v):
        opera_values = ['Aerolineas Argentinas', 'Aeromexico', 'Air Canada',
            'Air France', 'Alitalia', 'American Airlines',
            'Austral', 'Avianca', 'British Airways', 'Copa Air',
            'Delta Air', 'Gol Trans', 'Grupo LATAM', 'Iberia',
            'JetSmart SPA', 'K.L.M.', 'Lacsa',
            'Latin American Wings', 'Oceanair Linhas Aereas',
            'Plus Ultra Lineas Aereas', 'Qantas Airways',
            'Sky Airline', 'United Airlines']
        if v not in opera_values:
            raise HTTPException(status_code=400, detail="Invalid value for OPERA")
        return v
    
    @validator('TIPOVUELO')
    def tipovuelo_must_be_valid(cls, v):
        tipovuelo_values = ['I','N']
        if v not in tipovuelo_values:
            raise HTTPException(status_code=400, detail="Invalid value for TIPOVUELO")
        return v
    
    @validator('MES')
    def mes_must_be_valid(cls, v):
        if v not in range(1, 13):
            raise HTTPException(status_code=400, detail="Invalid value for MES")
        return v
    

class PredictRequest(BaseModel):
    flights: List[Flight]


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(request: PredictRequest) -> dict:
    # Accedemos a los valores de los atributos OPERA, TIPOVUELO y MES
    opera = request.flights[0].OPERA
    tipovuelo = request.flights[0].TIPOVUELO
    mes = request.flights[0].MES

    # Creamos un DataFrame con los datos
    df = pd.DataFrame({"OPERA": [opera], "TIPOVUELO": [tipovuelo], "MES": [mes]})

    # Aplicamos la codificación one-hot a las columnas
    df_encoded = pd.get_dummies(df, columns=["OPERA", "TIPOVUELO", "MES"])

    model_columns = ['OPERA_Aerolineas Argentinas', 'OPERA_Aeromexico', 'OPERA_Air Canada',
        'OPERA_Air France', 'OPERA_Alitalia', 'OPERA_American Airlines',
        'OPERA_Austral', 'OPERA_Avianca', 'OPERA_British Airways', 'OPERA_Copa Air',
        'OPERA_Delta Air', 'OPERA_Gol Trans', 'OPERA_Grupo LATAM', 'OPERA_Iberia',
        'OPERA_JetSmart SPA', 'OPERA_K.L.M.', 'OPERA_Lacsa',
        'OPERA_Latin American Wings', 'OPERA_Oceanair Linhas Aereas',
        'OPERA_Plus Ultra Lineas Aereas', 'OPERA_Qantas Airways',
        'OPERA_Sky Airline', 'OPERA_United Airlines', 'TIPOVUELO_I', 'TIPOVUELO_N',
        'MES_1', 'MES_2', 'MES_3', 'MES_4', 'MES_5', 'MES_6', 'MES_7', 'MES_8', 'MES_9',
        'MES_10', 'MES_11', 'MES_12']

    for col in model_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    # Reordenamos las columnas para que coincidan con el orden del modelo
    df_encoded = df_encoded[model_columns]

    # Se carga el modelo para hacer una predicción
    delay_model.load("./model_delay.pkl")

    # Utilizamos el modelo para hacer una predicción
    prediction = delay_model.predict(df_encoded)

    #Devuelve la predicción como respuesta
    return {"predict": prediction}