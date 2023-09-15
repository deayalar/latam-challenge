import fastapi
from fastapi import Response, status
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from challenge.model import DelayModel

model = DelayModel()
data = pd.read_csv(filepath_or_buffer="./data/data.csv")

features, target = model.preprocess(data=data, target_column="delay")
model.fit(features=features, target=target)

app = fastapi.FastAPI()


class Flight(BaseModel):
    operator: str = Field(None, alias="OPERA")
    flight_type: str = Field(None, alias="TIPOVUELO")
    month: str = Field(None, alias="MES")

    class Config:
        allow_population_by_field_name = True


class FlightsWrapper(BaseModel):
    flights: list[Flight]


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}


@app.post("/predict", status_code=200)
async def post_predict(json: FlightsWrapper, response: Response) -> dict:
    feature = np.zeros((len(json.flights), len(model.TOP_FEATURES)))
    for idx, flight in enumerate(json.flights):
        operator = "OPERA_" + flight.operator
        flight_type = "TIPOVUELO_" + flight.flight_type
        month = "MES_" + str(flight.month)
        if (
            operator not in model.columns
            or flight_type not in model.columns
            or month not in model.columns
        ):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {}
        else:
            if operator in model.TOP_FEATURES:
                feature[idx][model.TOP_FEATURES.index(operator)] = 1
            if flight_type in model.TOP_FEATURES:
                feature[idx][model.TOP_FEATURES.index(flight_type)] = 1
            if month in model.TOP_FEATURES:
                feature[idx][model.TOP_FEATURES.index(month)] = 1
    input_df = pd.DataFrame(feature, columns=model.TOP_FEATURES)
    return {"predict": model.predict(input_df)}
