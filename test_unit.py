# test_unitaires.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pandas as pd
from API_Fastapi import app, ClientData, NAME_CONTRACT_TYPE,CODE_GENDER
from enum import Enum

client = TestClient(app)

# ============================================================
# Tests des modèles Pydantic
# ============================================================

def test_client_data_valid(): #Tester la création d'un objet ClientData valide
   
    valid_data = {
        "NAME_CONTRACT_TYPE": "Cash loans",
        "CODE_GENDER": "M",
        "FLAG_OWN_CAR": "Y",
        "FLAG_OWN_REALTY": "Y",
        "CNT_CHILDREN": 0,
        "AMT_INCOME_TOTAL": 100000.0,
        "AMT_CREDIT": 50000.0,
        "AMT_ANNUITY": 2000.0,
        "AMT_GOODS_PRICE": 45000.0,
        "NAME_TYPE_SUITE": "Unaccompanied",
        "NAME_INCOME_TYPE": "Working",
        "NAME_EDUCATION_TYPE": "Higher education",
        "NAME_FAMILY_STATUS": "Married",
        "NAME_HOUSING_TYPE": "House / apartment",
        "REGION_POPULATION_RELATIVE": 0.01,
        "DAYS_BIRTH": -10000,
        "DAYS_EMPLOYED": -2000,
        "DAYS_REGISTRATION": -1500,
        "DAYS_ID_PUBLISH": -500,
        "FLAG_EMP_PHONE": 1,
        "FLAG_WORK_PHONE": 1,
        "FLAG_PHONE": 1,
        "FLAG_EMAIL": 0,
        "OCCUPATION_TYPE": "Managers",
        "CNT_FAM_MEMBERS": 2.0,
        "REGION_RATING_CLIENT": 2,
        "REGION_RATING_CLIENT_W_CITY": 2,
        "WEEKDAY_APPR_PROCESS_START": "MONDAY",
        "HOUR_APPR_PROCESS_START": 10,
        "REG_REGION_NOT_LIVE_REGION": 0,
        "REG_REGION_NOT_WORK_REGION": 0,
        "LIVE_REGION_NOT_WORK_REGION": 0,
        "REG_CITY_NOT_LIVE_CITY": 0,
        "REG_CITY_NOT_WORK_CITY": 0,
        "LIVE_CITY_NOT_WORK_CITY": 0,
        "ORGANIZATION_TYPE": "Business Entity Type 3",
        "FLOORSMAX_AVG": 5.0,
        "LIVINGAREA_AVG": 50.0,
        "YEARS_BEGINEXPLUATATION_MODE": 15.0,
        "OBS_30_CNT_SOCIAL_CIRCLE": 2.0,
        "DEF_30_CNT_SOCIAL_CIRCLE": 0.0,
        "DAYS_LAST_PHONE_CHANGE": -300.0,
        "PREVIOUS_LOANS_COUNT": 1.0,
        "CREDIT_INCOME_PERCENT": 0.5,
        "ANNUITY_INCOME_PERCENT": 0.02,
        "CREDIT_TERM": 20.0,
        "DAYS_EMPLOYED_PERCENT": 0.2
    }
    
    client_data = ClientData(**valid_data)
    assert client_data.CODE_GENDER == "M"
    assert client_data.AMT_INCOME_TOTAL == 100000.0

# ==============================================================================================

def test_client_data_invalid_values(): #Tester la validation des contraintes sur les champs

    invalid_data = {
        "NAME_CONTRACT_TYPE": "Cash loans",
        "CODE_GENDER": "M",
        "FLAG_OWN_CAR": "Y",
        "FLAG_OWN_REALTY": "Y",
        "CNT_CHILDREN": -1,  # Invalide : doit être >= 0
        "AMT_INCOME_TOTAL": 100000.0,
        "AMT_CREDIT": 50000.0,
        "AMT_ANNUITY": 2000.0,
        "AMT_GOODS_PRICE": 45000.0,
        "NAME_TYPE_SUITE": 5, #Invalide : doit être un texte et non un chiffre
        "NAME_INCOME_TYPE": "Working",
        "NAME_EDUCATION_TYPE": "Higher education",
        "NAME_FAMILY_STATUS": "Married",
        "NAME_HOUSING_TYPE": "House / apartment",
        "REGION_POPULATION_RELATIVE": 0.01,
        "DAYS_BIRTH": -10000,
        "DAYS_EMPLOYED": -2000,
        "DAYS_REGISTRATION": -1500,
        "DAYS_ID_PUBLISH": -500,
        "FLAG_EMP_PHONE": 2,  # Invalide : doit être 0 ou 1
        "FLAG_WORK_PHONE": 1,
        "FLAG_PHONE": 1,
        "FLAG_EMAIL": 0,
        "OCCUPATION_TYPE": "Managers",
        "CNT_FAM_MEMBERS": 2.0,
        "REGION_RATING_CLIENT": 2,
        "REGION_RATING_CLIENT_W_CITY": 2,
        "WEEKDAY_APPR_PROCESS_START": "MONDAY",
        "HOUR_APPR_PROCESS_START": 10,
        "REG_REGION_NOT_LIVE_REGION": 0,
        "REG_REGION_NOT_WORK_REGION": 0,
        "LIVE_REGION_NOT_WORK_REGION": 0,
        "REG_CITY_NOT_LIVE_CITY": 0,
        "REG_CITY_NOT_WORK_CITY": 0,
        "LIVE_CITY_NOT_WORK_CITY": 0,
        "ORGANIZATION_TYPE": "Business Entity Type 3",
        "FLOORSMAX_AVG": 5.0,
        "LIVINGAREA_AVG": 50.0,
        "YEARS_BEGINEXPLUATATION_MODE": 15.0,
        "OBS_30_CNT_SOCIAL_CIRCLE": 2.0,
        "DEF_30_CNT_SOCIAL_CIRCLE": 0.0,
        "DAYS_LAST_PHONE_CHANGE": -300.0,
        "PREVIOUS_LOANS_COUNT": 1.0,
        "CREDIT_INCOME_PERCENT": 0.5,
        "ANNUITY_INCOME_PERCENT": 0.02,
        "CREDIT_TERM": 20.0,
        "DAYS_EMPLOYED_PERCENT": 0.2
    }
    
    with pytest.raises(ValueError):
        ClientData(**invalid_data)

# ==============================================================================================

def test_enum_values(): #Test que les valeurs d'énumération sont correctes

    assert "Cash loans" in [e.value for e in NAME_CONTRACT_TYPE]
    assert "Revolving loans" in [e.value for e in NAME_CONTRACT_TYPE]
    assert "F" in [e.value for e in CODE_GENDER]
    assert "M" in [e.value for e in CODE_GENDER]
    assert "XNA" in [e.value for e in CODE_GENDER]


# ============================================================
# Tests des endpoints
# ============================================================

def test_home_endpoint(): # Test de l'endpoint d'accueil
   
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    assert "documentation" in data["endpoints"]

# ==============================================================================================

@patch('API_Fastapi.model') # Test de l'endpoint de prédiction avec succès avec un mock au lieu de notre modèle
def test_predict_endpoint_success(mock_model):
   
    # Mock du modèle
    mock_model.predict.return_value = [0]
    mock_model.predict_proba.return_value = [[0.8, 0.2]]
    
    test_data = {
        "NAME_CONTRACT_TYPE": "Cash loans",
        "CODE_GENDER": "M",
        "FLAG_OWN_CAR": "Y",
        "FLAG_OWN_REALTY": "Y",
        "CNT_CHILDREN": 0,
        "AMT_INCOME_TOTAL": 100000.0,
        "AMT_CREDIT": 50000.0,
        "AMT_ANNUITY": 2000.0,
        "AMT_GOODS_PRICE": 45000.0,
        "NAME_TYPE_SUITE": "Unaccompanied",
        "NAME_INCOME_TYPE": "Working",
        "NAME_EDUCATION_TYPE": "Higher education",
        "NAME_FAMILY_STATUS": "Married",
        "NAME_HOUSING_TYPE": "House / apartment",
        "REGION_POPULATION_RELATIVE": 0.01,
        "DAYS_BIRTH": -10000,
        "DAYS_EMPLOYED": -2000,
        "DAYS_REGISTRATION": -1500,
        "DAYS_ID_PUBLISH": -500,
        "FLAG_EMP_PHONE": 1,
        "FLAG_WORK_PHONE": 1,
        "FLAG_PHONE": 1,
        "FLAG_EMAIL": 0,
        "OCCUPATION_TYPE": "Managers",
        "CNT_FAM_MEMBERS": 2.0,
        "REGION_RATING_CLIENT": 2,
        "REGION_RATING_CLIENT_W_CITY": 2,
        "WEEKDAY_APPR_PROCESS_START": "MONDAY",
        "HOUR_APPR_PROCESS_START": 10,
        "REG_REGION_NOT_LIVE_REGION": 0,
        "REG_REGION_NOT_WORK_REGION": 0,
        "LIVE_REGION_NOT_WORK_REGION": 0,
        "REG_CITY_NOT_LIVE_CITY": 0,
        "REG_CITY_NOT_WORK_CITY": 0,
        "LIVE_CITY_NOT_WORK_CITY": 0,
        "ORGANIZATION_TYPE": "Business Entity Type 3",
        "FLOORSMAX_AVG": 5.0,
        "LIVINGAREA_AVG": 50.0,
        "YEARS_BEGINEXPLUATATION_MODE": 15.0,
        "OBS_30_CNT_SOCIAL_CIRCLE": 2.0,
        "DEF_30_CNT_SOCIAL_CIRCLE": 0.0,
        "DAYS_LAST_PHONE_CHANGE": -300.0,
        "PREVIOUS_LOANS_COUNT": 1.0,
        "CREDIT_INCOME_PERCENT": 0.5,
        "ANNUITY_INCOME_PERCENT": 0.02,
        "CREDIT_TERM": 20.0,
        "DAYS_EMPLOYED_PERCENT": 0.2
    }
    
    response = client.post("/predict", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probabilité_defaut" in data
    assert data["prediction"] in ["Solvable", "Défaillant"]

# ==============================================================================================

@patch('API_Fastapi.model')
def test_predict_endpoint_defaillant(mock_model): #Test de prédiction pour un client défaillant
    
    mock_model.predict.return_value = [1]
    mock_model.predict_proba.return_value = [[0.3, 0.7]]
    
    test_data = {
        "NAME_CONTRACT_TYPE": "Cash loans",
        "CODE_GENDER": "M",
        "FLAG_OWN_CAR": "Y",
        "FLAG_OWN_REALTY": "Y",
        "CNT_CHILDREN": 0,
        "AMT_INCOME_TOTAL": 100000.0,
        "AMT_CREDIT": 50000.0,
        "AMT_ANNUITY": 2000.0,
        "AMT_GOODS_PRICE": 45000.0,
        "NAME_TYPE_SUITE": "Unaccompanied",
        "NAME_INCOME_TYPE": "Working",
        "NAME_EDUCATION_TYPE": "Higher education",
        "NAME_FAMILY_STATUS": "Married",
        "NAME_HOUSING_TYPE": "House / apartment",
        "REGION_POPULATION_RELATIVE": 0.01,
        "DAYS_BIRTH": -10000,
        "DAYS_EMPLOYED": -2000,
        "DAYS_REGISTRATION": -1500,
        "DAYS_ID_PUBLISH": -500,
        "FLAG_EMP_PHONE": 1,
        "FLAG_WORK_PHONE": 1,
        "FLAG_PHONE": 1,
        "FLAG_EMAIL": 0,
        "OCCUPATION_TYPE": "Managers",
        "CNT_FAM_MEMBERS": 2.0,
        "REGION_RATING_CLIENT": 2,
        "REGION_RATING_CLIENT_W_CITY": 2,
        "WEEKDAY_APPR_PROCESS_START": "MONDAY",
        "HOUR_APPR_PROCESS_START": 10,
        "REG_REGION_NOT_LIVE_REGION": 0,
        "REG_REGION_NOT_WORK_REGION": 0,
        "LIVE_REGION_NOT_WORK_REGION": 0,
        "REG_CITY_NOT_LIVE_CITY": 0,
        "REG_CITY_NOT_WORK_CITY": 0,
        "LIVE_CITY_NOT_WORK_CITY": 0,
        "ORGANIZATION_TYPE": "Business Entity Type 3",
        "FLOORSMAX_AVG": 5.0,
        "LIVINGAREA_AVG": 50.0,
        "YEARS_BEGINEXPLUATATION_MODE": 15.0,
        "OBS_30_CNT_SOCIAL_CIRCLE": 2.0,
        "DEF_30_CNT_SOCIAL_CIRCLE": 0.0,
        "DAYS_LAST_PHONE_CHANGE": -300.0,
        "PREVIOUS_LOANS_COUNT": 1.0,
        "CREDIT_INCOME_PERCENT": 0.5,
        "ANNUITY_INCOME_PERCENT": 0.02,
        "CREDIT_TERM": 20.0,
        "DAYS_EMPLOYED_PERCENT": 0.2
    }
    
    response = client.post("/predict", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "Défaillant"
    assert data["probabilité_defaut"] == 0.7

# ==============================================================================================

def test_predict_endpoint_invalid_data(): #Test de l'endpoint de prédiction avec des données invalides

    invalid_data = {
        "NAME_CONTRACT_TYPE": "Invalid Type",  # Valeur d'enum invalide
        "CODE_GENDER": "M",
        "FLAG_OWN_CAR": "Y",
        "CNT_CHILDREN": -1,  # Valeur négative invalide
        # ... autres champs requis manquants
    }
    
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity

# ==============================================================================================

@patch('API_Fastapi.model', None) #Test quand le modèle n'est pas chargé
def test_predict_endpoint_model_not_loaded():
    
    test_data = {
        "NAME_CONTRACT_TYPE": "Cash loans",
        "CODE_GENDER": "M",
        "FLAG_OWN_CAR": "Y",
        "FLAG_OWN_REALTY": "Y",
        "CNT_CHILDREN": 0,
        "AMT_INCOME_TOTAL": 100000.0,
        "AMT_CREDIT": 50000.0,
        "AMT_ANNUITY": 2000.0,
        "AMT_GOODS_PRICE": 45000.0,
        "NAME_TYPE_SUITE": "Unaccompanied",
        "NAME_INCOME_TYPE": "Working",
        "NAME_EDUCATION_TYPE": "Higher education",
        "NAME_FAMILY_STATUS": "Married",
        "NAME_HOUSING_TYPE": "House / apartment",
        "REGION_POPULATION_RELATIVE": 0.01,
        "DAYS_BIRTH": -10000,
        "DAYS_EMPLOYED": -2000,
        "DAYS_REGISTRATION": -1500,
        "DAYS_ID_PUBLISH": -500,
        "FLAG_EMP_PHONE": 1,
        "FLAG_WORK_PHONE": 1,
        "FLAG_PHONE": 1,
        "FLAG_EMAIL": 0,
        "OCCUPATION_TYPE": "Managers",
        "CNT_FAM_MEMBERS": 2.0,
        "REGION_RATING_CLIENT": 2,
        "REGION_RATING_CLIENT_W_CITY": 2,
        "WEEKDAY_APPR_PROCESS_START": "MONDAY",
        "HOUR_APPR_PROCESS_START": 10,
        "REG_REGION_NOT_LIVE_REGION": 0,
        "REG_REGION_NOT_WORK_REGION": 0,
        "LIVE_REGION_NOT_WORK_REGION": 0,
        "REG_CITY_NOT_LIVE_CITY": 0,
        "REG_CITY_NOT_WORK_CITY": 0,
        "LIVE_CITY_NOT_WORK_CITY": 0,
        "ORGANIZATION_TYPE": "Business Entity Type 3",
        "FLOORSMAX_AVG": 5.0,
        "LIVINGAREA_AVG": 50.0,
        "YEARS_BEGINEXPLUATATION_MODE": 15.0,
        "OBS_30_CNT_SOCIAL_CIRCLE": 2.0,
        "DEF_30_CNT_SOCIAL_CIRCLE": 0.0,
        "DAYS_LAST_PHONE_CHANGE": -300.0,
        "PREVIOUS_LOANS_COUNT": 1.0,
        "CREDIT_INCOME_PERCENT": 0.5,
        "ANNUITY_INCOME_PERCENT": 0.02,
        "CREDIT_TERM": 20.0,
        "DAYS_EMPLOYED_PERCENT": 0.2
    }
    
    response = client.post("/predict", json=test_data)
    assert response.status_code == 500
    assert "Modèle non chargé" in response.json()["detail"]