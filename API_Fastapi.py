from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from enum import Enum
import joblib
import pandas as pd
import traceback
import logging
import os
import time 
import uuid 
from logging.handlers import RotatingFileHandler
from datetime import datetime
import json
from fastapi.responses import PlainTextResponse

# ============================================================
# Définition des Enums pour les champs à choix limités
# ============================================================

class NAME_CONTRACT_TYPE(str, Enum):
    Cash_loans = "Cash loans"
    Revolving_loans = "Revolving loans"

class CODE_GENDER(str, Enum):
    F = "F"
    M = "M"
    XNA = "XNA"

class FLAG_OWN_CAR(str, Enum):
    N = "N"
    Y = "Y"

class FLAG_OWN_REALTY(str, Enum):
    N = "N"
    Y = "Y"

class NAME_TYPE_SUITE(str, Enum):
    Unaccompanied = "Unaccompanied"
    Family = "Family"
    Spouse_partner = "Spouse, partner"
    Children = "Children"
    Other_B = "Other_B"
    Other_A = "Other_A"
    Group_of_people = "Group of people"

class NAME_INCOME_TYPE(str, Enum):
    Working = "Working"
    Commercial_associate = "Commercial associate"
    Pensioner = "Pensioner"
    State_servant = "State servant"
    Unemployed = "Unemployed"
    Student = "Student"
    Businessman = "Businessman"
    Maternity_leave = "Maternity leave"

class NAME_EDUCATION_TYPE(str, Enum):
    Secondary = "Secondary / secondary special"
    Higher = "Higher education"
    Incomplete_higher = "Incomplete higher"
    Lower_secondary = "Lower secondary"
    Academic_degree = "Academic degree"

class NAME_FAMILY_STATUS(str, Enum):
    Married = "Married"
    Single = "Single / not married"
    Civil_marriage = "Civil marriage"
    Separated = "Separated"
    Widow = "Widow"
    Unknown = "Unknown"

class NAME_HOUSING_TYPE(str, Enum):
    House_apartment = "House / apartment"
    With_parents = "With parents"
    Municipal_apartment = "Municipal apartment"
    Rented_apartment = "Rented apartment"
    Office_apartment = "Office apartment"
    Coop_apartment = "Co-op apartment"

class OCCUPATION_TYPE(str, Enum):
    Laborers = "Laborers"
    Sales_staff = "Sales staff"
    Core_staff = "Core staff"
    Managers = "Managers"
    Drivers = "Drivers"
    High_skill_tech_staff = "High skill tech staff"
    Accountants = "Accountants"
    Medicine_staff = "Medicine staff"
    Security_staff = "Security staff"
    Cooking_staff = "Cooking staff"
    Cleaning_staff = "Cleaning staff"
    Private_service_staff = "Private service staff"
    Low_skill_Laborers = "Low-skill Laborers"
    Waiters_barmen_staff = "Waiters/barmen staff"
    Secretaries = "Secretaries"
    Realty_agents = "Realty agents"
    HR_staff = "HR staff"
    IT_staff = "IT staff"

class WEEKDAY_APPR_PROCESS_START(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

class ORGANIZATION_TYPE(str, Enum):
    Business_Entity_Type_3 = "Business Entity Type 3"
    XNA = "XNA"
    Self_employed = "Self-employed"
    Other = "Other"
    Medicine = "Medicine"
    Business_Entity_Type_2 = "Business Entity Type 2"
    Government = "Government"
    School = "School"
    Trade_type_7 = "Trade: type 7"
    Kindergarten = "Kindergarten"
    Construction = "Construction"
    Business_Entity_Type_1 = "Business Entity Type 1"
    Transport_type_4 = "Transport: type 4"
    Trade_type_3 = "Trade: type 3"
    Industry_type_9 = "Industry: type 9"
    Industry_type_3 = "Industry: type 3"
    Security = "Security"
    Housing = "Housing"
    Industry_type_11 = "Industry: type 11"
    Military = "Military"
    Bank = "Bank"
    Agriculture = "Agriculture"
    Police = "Police"
    Transport_type_2 = "Transport: type 2"
    Postal = "Postal"
    Security_Ministries = "Security Ministries"
    Trade_type_2 = "Trade: type 2"
    Restaurant = "Restaurant"
    Services = "Services"
    University = "University"
    Industry_type_7 = "Industry: type 7"
    Transport_type_3 = "Transport: type 3"
    Industry_type_1 = "Industry: type 1"
    Hotel = "Hotel"
    Electricity = "Electricity"
    Industry_type_4 = "Industry: type 4"
    Trade_type_6 = "Trade: type 6"
    Industry_type_5 = "Industry: type 5"
    Insurance = "Insurance"
    Telecom = "Telecom"
    Emergency = "Emergency"
    Industry_type_2 = "Industry: type 2"
    Advertising = "Advertising"
    Realtor = "Realtor"
    Culture = "Culture"
    Industry_type_12 = "Industry: type 12"
    Trade_type_1 = "Trade: type 1"
    Mobile = "Mobile"
    Legal_Services = "Legal Services"
    Cleaning = "Cleaning"
    Transport_type_1 = "Transport: type 1"
    Industry_type_6 = "Industry: type 6"
    Industry_type_10 = "Industry: type 10"
    Religion = "Religion"
    Industry_type_13 = "Industry: type 13"
    Trade_type_4 = "Trade: type 4"
    Trade_type_5 = "Trade: type 5"
    Industry_type_8 = "Industry: type 8"


# ============================================================
# Modèle de données (inputs)
# ============================================================

class ClientData(BaseModel):
    NAME_CONTRACT_TYPE: NAME_CONTRACT_TYPE
    CODE_GENDER: CODE_GENDER
    FLAG_OWN_CAR: FLAG_OWN_CAR
    FLAG_OWN_REALTY: FLAG_OWN_REALTY
    CNT_CHILDREN: int = Field(ge=0)
    AMT_INCOME_TOTAL: float = Field(gt=0)
    AMT_CREDIT: float = Field(gt=0)
    AMT_ANNUITY: float = Field(gt=0)
    AMT_GOODS_PRICE: float = Field(gt=0)
    NAME_TYPE_SUITE: NAME_TYPE_SUITE
    NAME_INCOME_TYPE: NAME_INCOME_TYPE
    NAME_EDUCATION_TYPE: NAME_EDUCATION_TYPE
    NAME_FAMILY_STATUS: NAME_FAMILY_STATUS
    NAME_HOUSING_TYPE: NAME_HOUSING_TYPE
    REGION_POPULATION_RELATIVE: float
    DAYS_BIRTH: int = Field(le=0)
    DAYS_EMPLOYED: int = Field(le=0)
    DAYS_REGISTRATION: int
    DAYS_ID_PUBLISH: int
    FLAG_EMP_PHONE: int = Field(ge=0, le=1)
    FLAG_WORK_PHONE: int = Field(ge=0, le=1)
    FLAG_PHONE: int = Field(ge=0, le=1)
    FLAG_EMAIL: int = Field(ge=0, le=1)
    OCCUPATION_TYPE: OCCUPATION_TYPE
    CNT_FAM_MEMBERS: float
    REGION_RATING_CLIENT: int
    REGION_RATING_CLIENT_W_CITY: int
    WEEKDAY_APPR_PROCESS_START: WEEKDAY_APPR_PROCESS_START
    HOUR_APPR_PROCESS_START: int
    REG_REGION_NOT_LIVE_REGION: int = Field(ge=0, le=1)
    REG_REGION_NOT_WORK_REGION: int = Field(ge=0, le=1)
    LIVE_REGION_NOT_WORK_REGION: int = Field(ge=0, le=1)
    REG_CITY_NOT_LIVE_CITY: int = Field(ge=0, le=1)
    REG_CITY_NOT_WORK_CITY: int = Field(ge=0, le=1)
    LIVE_CITY_NOT_WORK_CITY: int = Field(ge=0, le=1)
    ORGANIZATION_TYPE: ORGANIZATION_TYPE
    FLOORSMAX_AVG: float
    LIVINGAREA_AVG: float
    YEARS_BEGINEXPLUATATION_MODE: float
    OBS_30_CNT_SOCIAL_CIRCLE: float
    DEF_30_CNT_SOCIAL_CIRCLE: float
    DAYS_LAST_PHONE_CHANGE: float
    PREVIOUS_LOANS_COUNT: float
    CREDIT_INCOME_PERCENT: float
    ANNUITY_INCOME_PERCENT: float
    CREDIT_TERM: float
    DAYS_EMPLOYED_PERCENT: float

# ============================================================
# Configuration du logger
# ============================================================

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "api_logger.log")


logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=10_000_000, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
if not logger.handlers:
    logger.addHandler(handler)

logger.info("Logs écrits dans logs/api_logger.log dans le dossier du projet.")

#Fonction pour écrire des logs structurés au format JSONL

def write_log(entry: dict):
    try:
        logger.info(json.dumps(entry, ensure_ascii=False))
    except Exception as e : 
        logger.error(f"Erreur lors de l'écriture du log structuré{e}")

#-----------------------------------------------------------------------------------------------------
# Création de l'application FastAPI et chargement du modèle
#-----------------------------------------------------------------------------------------------------

app = FastAPI(
    title="API de prédiction de solvabilité Client", 
    description="Cette API permet de prédire si un client est solvable ou défaillant, dans le cadre de l'étude de sa demande de prêt, et aide à prendre la décision d'octroi ou de refus de prêt.",
    version="3.0",
    )

# Middleware de logging

@app.middleware("http")
async def log_request_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()
    logger.info(f"Début requête {request_id} : {request.method} {request.url.path}")
    response = await call_next(request)
    duration = time.time() - start_time
    status_code = response.status_code
    logger.info(f"Fin requête {request_id} : {request.method} {request.url.path} - "
            f"Status {response.status_code} - Durée {duration:.3f}s")
    write_log({
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": status_code,
        "duration": duration,
        "client_ip": request.client.host if request.client else "unknown",
        "event": "http_request"
    })

    return response 

# Chargement du modèle

try:
    model = joblib.load("model.pkl")
    logger.info("Modèle chargé avec succès.")
except Exception as e:
    logger.critical(f"Erreur lors du chargement du modèle : {e}", exc_info=True)
    print(f" Erreur de chargement du modèle : {e}")
    model = None


#-----------------------------------------------------------------------------------------------------
# 1er Endpoint : Route d'accueil qui fournit un message de bienvenue, et oriente vers les endpoints.
#-----------------------------------------------------------------------------------------------------

@app.get("/", tags=["Accueil"], summary="Page d'accueil", description=" un message de bienvenue et les principaux endpoints de l’API.")
def home():
    logger.info("Accès à l'endpoint d'accueil")
    return {
    "message": "Bienvenue dans l’API de prédiction de solvabilité des clients",
    "description" : "Cette API utilise un modèle de Machine Learning pour prédire si un client est solvable ou défaillant",
    "endpoints": {
    "documentation": "/docs",
    "faire une prédiction": "/predict" }
    
    }

#------------------------------------------------------------------------------------------------------------------
# 2eme Endpoint : Route de prédiction pour faire une prédiction avec les données saisies. attend une requete POST 
#------------------------------------------------------------------------------------------------------------------

@app.post("/predict", tags=["Prédiction"], summary="Faire une prédiction", description="Prédit si un client est solvable ou défaillant.")

def predict(request: Request, client: ClientData):
    "Endpoint de prédiction principale"
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(f"Requête de prédiction reçue - Request ID: {request_id}")

    if model is None:
        logger.critical(f"Modèle non chargé au moment de la prédiction- Request ID: {request_id}")
        write_log({
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request.state.request_id if hasattr(request.state, "request_id") else "unknown",
            "event": "prediction_error",
            "error": "Modèle non chargé"
        })
        raise HTTPException(status_code=500, detail="Modèle non chargé")

    try:
        df = pd.DataFrame([client.dict()])
        logger.info(f"DataFrame créé avec succès - Shape: {df.shape} - Request ID : {request_id}")
        y_pred = model.predict(df)[0]
        y_proba = model.predict_proba(df)[0][1]
        prediction = "Défaillant" if y_pred == 1 else "Solvable"
        probabilité_defaut = round(float(y_proba), 4)

        logger.info(f"Prédiction calculée : {prediction} - Probabilité de défaut : {probabilité_defaut}")
        write_log({
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request.state.request_id,
            "event": "prediction",
            "input_data": client.dict(),
            "prediction": prediction,
            "probabilité_defaut": probabilité_defaut
        })
        return {
            "prediction": prediction,
            "probabilité_defaut": probabilité_defaut
        }
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction - Request ID : {request_id}", exc_info=True)
        print(traceback.format_exc())
        write_log({
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request.state.request_id if hasattr(request.state, "request_id") else "unknown",
            "event": "prediction_error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })
        raise HTTPException(status_code=400, detail="Erreur lors de la prédiction. Vérifiez les données d'entrée.")

#------------------------------------------------------------------------------------------------------------------
# 3eme Endpoint : Gestion des loggs
#------------------------------------------------------------------------------------------------------------------

@app.get("/logs", tags=["Logg"])
def get_logs():
    try:
        with open("logs/api_logger.log", "r") as f:
            return PlainTextResponse(f.read())
    except Exception as e:
        return PlainTextResponse(f"Erreur : {e}", status_code=500)


#------------------------------------------------------------------------------------------------------------------
# Endpoint pour ignorer l'erreur générée par /favicon
#------------------------------------------------------------------------------------------------------------------

@app.get("/favicon.ico")
async def favicon():
    # ignorer l'erreur /favicon.ico:
    return {}

#------------------------------------------------------------------------------------------------------------------
# Fin du script
#------------------------------------------------------------------------------------------------------------------