from fastapi import FastAPI, Request
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run

from typing import Optional

# Importing constants and pipeline modules from the project
from src.constants import APP_HOST, APP_PORT
from src.pipline.prediction_pipeline import VehicleData, VehicleDataClassifier
from src.entity.estimator import TargetValueMapping
from src.pipline.training_pipeline import TrainPipeline
from src.entity.s3_estimator import Proj1Estimator
from src.entity.config_entity import VehiclePredictorConfig

# Initialize FastAPI application
app = FastAPI()

# Mount the 'static' directory for serving static files (like CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 template engine for rendering HTML templates
templates = Jinja2Templates(directory='templates')

# Allow all origins for Cross-Origin Resource Sharing (CORS)
origins = ["*"]

# Configure middleware to handle CORS, allowing requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:
    """
    DataForm class to handle and process incoming form data.
    This class defines the vehicle-related attributes expected from the form.
    """
    def __init__(self, request: Request):
        self.request: Request = request
        self.Gender: Optional[int] = None
        self.Age: Optional[int] = None
        self.Driving_License: Optional[int] = None
        self.Region_Code: Optional[float] = None
        self.Previously_Insured: Optional[int] = None
        self.Annual_Premium: Optional[float] = None
        self.Policy_Sales_Channel: Optional[float] = None
        self.Vintage: Optional[int] = None
        self.Vehicle_Age_lt_1_Year: Optional[int] = None
        self.Vehicle_Age_gt_2_Years: Optional[int] = None
        self.Vehicle_Damage_Yes: Optional[int] = None
                

    async def get_vehicle_data(self):
        """
        Method to retrieve and assign form data to class attributes.
        This method is asynchronous to handle form data fetching without blocking.
        """
        form = await self.request.form()
        self.Gender = form.get("Gender")
        self.Age = form.get("Age")
        self.Driving_License = form.get("Driving_License")
        self.Region_Code = form.get("Region_Code")
        self.Previously_Insured = form.get("Previously_Insured")
        self.Annual_Premium = form.get("Annual_Premium")
        self.Policy_Sales_Channel = form.get("Policy_Sales_Channel")
        self.Vintage = form.get("Vintage")
        self.Vehicle_Age_lt_1_Year = form.get("Vehicle_Age_lt_1_Year")
        self.Vehicle_Age_gt_2_Years = form.get("Vehicle_Age_gt_2_Years")
        self.Vehicle_Damage_Yes = form.get("Vehicle_Damage_Yes")

# Route to render the main page with the form
@app.get("/", tags=["authentication"])
async def index(request: Request):
    """
    Renders the main HTML form page for vehicle data input.
    """
    return templates.TemplateResponse(
            "vehicledata.html",{"request": request, "context": "Rendering"})

# Route to trigger the model training process
@app.get("/train")
async def trainRouteClient():
    """
    Endpoint to initiate the model training pipeline.
    """
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful!!!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")

# Route to handle form submission and make predictions
@app.post("/")
async def predictRouteClient(request: Request):
    """
    Endpoint to receive form data, process it, and make a prediction.
    """
    try:
        form = DataForm(request)
        await form.get_vehicle_data()
        
        vehicle_data = VehicleData(
                                Gender= form.Gender,
                                Age = form.Age,
                                Driving_License = form.Driving_License,
                                Region_Code = form.Region_Code,
                                Previously_Insured = form.Previously_Insured,
                                Annual_Premium = form.Annual_Premium,
                                Policy_Sales_Channel = form.Policy_Sales_Channel,
                                Vintage = form.Vintage,
                                Vehicle_Age_lt_1_Year = form.Vehicle_Age_lt_1_Year,
                                Vehicle_Age_gt_2_Years = form.Vehicle_Age_gt_2_Years,
                                Vehicle_Damage_Yes = form.Vehicle_Damage_Yes
                                )

        # Convert form data into a DataFrame for the model
        vehicle_df = vehicle_data.get_vehicle_input_data_frame()

        # Initialize the prediction pipeline
        model_predictor = VehicleDataClassifier()

        # Make a prediction and retrieve the result
        value = model_predictor.predict(dataframe=vehicle_df)[0]

        # Interpret the prediction result using TargetValueMapping
        mapping = TargetValueMapping().reverse_mapping()
        try:
            label = mapping.get(int(value), 'no')
        except Exception:
            label = 'no'
        status = "Response-Yes" if str(label).lower() == 'yes' else "Response-No"

        # Render the same HTML page with the prediction result
        return templates.TemplateResponse(
            "vehicledata.html",
            {"request": request, "context": status},
        )
        
    except Exception as e:
        return {"status": False, "error": f"{e}"}

@app.post("/predict")
async def predict_api(request: Request):
    try:
        form = DataForm(request)
        await form.get_vehicle_data()
        
        vehicle_data = VehicleData(
                                Gender= form.Gender,
                                Age = form.Age,
                                Driving_License = form.Driving_License,
                                Region_Code = form.Region_Code,
                                Previously_Insured = form.Previously_Insured,
                                Annual_Premium = form.Annual_Premium,
                                Policy_Sales_Channel = form.Policy_Sales_Channel,
                                Vintage = form.Vintage,
                                Vehicle_Age_lt_1_Year = form.Vehicle_Age_lt_1_Year,
                                Vehicle_Age_gt_2_Years = form.Vehicle_Age_gt_2_Years,
                                Vehicle_Damage_Yes = form.Vehicle_Damage_Yes
                                )

        vehicle_df = vehicle_data.get_vehicle_input_data_frame()

        model_predictor = VehicleDataClassifier()

        value = model_predictor.predict(dataframe=vehicle_df)[0]

        mapping = TargetValueMapping().reverse_mapping()
        try:
            label = mapping.get(int(value), 'no')
        except Exception:
            label = 'no'
        status = "Response-Yes" if str(label).lower() == 'yes' else "Response-No"

        return {"prediction": status}
        
    except Exception as e:
        return {"error": str(e)}


@app.post("/predict_batch")
async def predict_batch(request: Request):
    """Accepts JSON with `rows`: list of objects (columns -> values).
    Returns predictions for each row as a list.
    """
    try:
        body = await request.json()
        rows = body.get("rows")
        if not rows or not isinstance(rows, list):
            return {"error": "Provide 'rows' as a list of objects"}

        # Build DataFrame from provided rows
        df = pd.DataFrame(rows)

        # Normalize column names: strip, replace spaces with underscores, remove special chars
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace(r'[^0-9A-Za-z_]', '', regex=True)

        # If pasted format uses 'Vehicle_Age' and 'Vehicle_Damage' convert to model expected columns
        # Parse Vehicle_Age into two dummy columns
        if 'Vehicle_Age' in df.columns:
            def parse_vehicle_age(v):
                try:
                    if pd.isna(v):
                        return 0, 0
                    s = str(v).lower()
                    if '<' in s or 'lt' in s or 'less' in s or '<1' in s or '< 1' in s:
                        return 1, 0
                    if '>' in s or 'gt' in s or '>2' in s or '> 2' in s or 'greater' in s:
                        return 0, 1
                    if '1-2' in s or '1 to 2' in s or '1 – 2' in s or '1 2' in s:
                        return 0, 0
                    # fallback: if contains '1' and not '2'
                    if '1' in s and '2' not in s:
                        return 0, 0
                    return 0, 0
                except Exception:
                    return 0, 0

            parsed = df['Vehicle_Age'].apply(lambda x: pd.Series(parse_vehicle_age(x), index=['Vehicle_Age_lt_1_Year', 'Vehicle_Age_gt_2_Years']))
            df = pd.concat([df, parsed], axis=1)

        # Map Vehicle_Damage strings to Vehicle_Damage_Yes binary
        if 'Vehicle_Damage' in df.columns:
            df['Vehicle_Damage_Yes'] = df['Vehicle_Damage'].astype(str).str.lower().map({'yes': 1, 'no': 0})

        # Map Gender strings to binary when needed
        if 'Gender' in df.columns and df['Gender'].dtype == object:
            df['Gender'] = df['Gender'].str.strip().map({'Female': 0, 'Male': 1}).fillna(0).astype(int)

        # Coerce numeric columns to numeric types where applicable
        numeric_cols = ['Age', 'Driving_License', 'Region_Code', 'Previously_Insured', 'Annual_Premium', 'Policy_Sales_Channel', 'Vintage']
        for c in numeric_cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        # Ensure expected columns exist for the model
        expected_cols = [
            "Gender","Age","Driving_License","Region_Code",
            "Previously_Insured","Annual_Premium","Policy_Sales_Channel",
            "Vintage","Vehicle_Age_lt_1_Year","Vehicle_Age_gt_2_Years",
            "Vehicle_Damage_Yes"
        ]
        for c in expected_cols:
            if c not in df.columns:
                df[c] = 0

        # Drop identifier columns if present
        for col in ['id', '_id']:
            if col in df.columns:
                df = df.drop(columns=[col])

        # Reorder columns to expected order (model may not require exact order but keep tidy)
        df = df[expected_cols]

        # Call model predictor (but load underlying MyModel to optionally inspect transformed features)
        estimator = Proj1Estimator(
            bucket_name=VehiclePredictorConfig().model_bucket_name,
            model_path=VehiclePredictorConfig().model_file_path,
        )
        loaded = estimator.load_model()

        # Attempt a safe transform only for debug info (do not use result for prediction)
        sample = None
        try:
            transformed = loaded.preprocessing_object.transform(df)
            try:
                first_row = transformed[0].tolist() if hasattr(transformed[0], 'tolist') else None
            except Exception:
                first_row = None
            sample = {"transformed_shape": getattr(transformed, 'shape', None), "transformed_first_row": first_row}
        except Exception:
            sample = None

        # Use estimator.predict which runs MyModel.predict and handles missing columns gracefully
        raw_preds = estimator.predict(dataframe=df)

        # Map raw numeric outputs to labels using TargetValueMapping
        mapping = TargetValueMapping().reverse_mapping()
        statuses = []
        for v in raw_preds:
            try:
                lab = mapping.get(int(v), 'no')
            except Exception:
                lab = 'no'
            statuses.append("Response-Yes" if str(lab).lower() == 'yes' else "Response-No")

        if body.get("debug", False):
            return {"predictions": statuses, "debug": sample}

        return {"predictions": statuses}

    except Exception as e:
        return {"error": str(e)}

# Main entry point to start the FastAPI server
if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)