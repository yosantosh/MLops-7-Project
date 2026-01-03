from fastapi.testclient import TestClient
import json

from app import app

client = TestClient(app)

rows = [
    {"Gender":"Male","Age":61,"Driving_License":1,"Region_Code":15,"Previously_Insured":0,"Vehicle_Age":"1-2 Year","Vehicle_Damage":"Yes","Annual_Premium":49616,"Policy_Sales_Channel":124,"Vintage":89},
    {"Gender":"Female","Age":24,"Driving_License":1,"Region_Code":9,"Previously_Insured":1,"Vehicle_Age":"< 1 Year","Vehicle_Damage":"No","Annual_Premium":33515,"Policy_Sales_Channel":163,"Vintage":35},
    {"Gender":"Male","Age":46,"Driving_License":1,"Region_Code":28,"Previously_Insured":1,"Vehicle_Age":"1-2 Year","Vehicle_Damage":"No","Annual_Premium":45353,"Policy_Sales_Channel":124,"Vintage":12},
    {"Gender":"Female","Age":34,"Driving_License":1,"Region_Code":13,"Previously_Insured":0,"Vehicle_Age":"1-2 Year","Vehicle_Damage":"Yes","Annual_Premium":29345,"Policy_Sales_Channel":152,"Vintage":117},
    {"Gender":"Female","Age":31,"Driving_License":1,"Region_Code":11,"Previously_Insured":0,"Vehicle_Age":"1-2 Year","Vehicle_Damage":"Yes","Annual_Premium":22086,"Policy_Sales_Channel":156,"Vintage":92}
]

resp = client.post('/predict_batch', json={"debug": True, "rows": rows})
print('status_code:', resp.status_code)
try:
    print(json.dumps(resp.json(), indent=2))
except Exception as e:
    print('response content:', resp.content)
