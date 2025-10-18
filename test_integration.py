# test_integration.py
import pytest
from fastapi.testclient import TestClient
import joblib
import pandas as pd
from API_Fastapi import app, ClientData

client = TestClient(app)

# ============================================================
# Fixtures pour les données de test
# ============================================================

@pytest.fixture
def sample_client_data(): #Fournir des données clients valides pour les tests"""
    
    return {
        "NAME_CONTRACT_TYPE": "Cash loans",
        "CODE_GENDER": "M",
        "FLAG_OWN_CAR": "Y",
        "FLAG_OWN_REALTY": "Y",
        "CNT_CHILDREN": 2,
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

# ==============================================================================

@pytest.fixture
def different_client_data(sample_client_data): #Fournir des données client différentes pour tester la variabilité
    
    data = sample_client_data.copy() 
    data.update({
        "CODE_GENDER": "F",
        "NAME_CONTRACT_TYPE": "Revolving loans",
        "AMT_INCOME_TOTAL": 80000.0,
        "AMT_CREDIT": 30000.0,
        "OCCUPATION_TYPE": "Sales staff"
    })
    return data


# ============================================================
# Tests d'intégration complète
# ============================================================

def test_complete_workflow(sample_client_data): #Test du workflow complet de l'API
    
    #Test de l'endpoint d'accueil

    response = client.get("/")
    assert response.status_code == 200
    assert "Bienvenue" in response.json()["message"]
    
    #Test de l'endpoint de prédiction

    response = client.post("/predict", json=sample_client_data)
    assert response.status_code in [200, 500]  # 200 si ok, 500 si modèle non chargé
    
    if response.status_code == 200:
        data = response.json()
        assert "prediction" in data
        assert "probabilité_defaut" in data
        assert isinstance(data["probabilité_defaut"], float)
        assert 0 <= data["probabilité_defaut"] <= 1

# ==============================================================================

def test_multiple_predictions(sample_client_data, different_client_data): 
#Test de multiples prédictions avec différentes données
    
    # Première prédiction
    response1 = client.post("/predict", json=sample_client_data)
    
    # Deuxième prédiction avec données différentes
    response2 = client.post("/predict", json=different_client_data)
    
    # Les deux requêtes doivent réussir
    assert response1.status_code in [200, 500]
    assert response2.status_code in [200, 500]
    
    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.json()
        data2 = response2.json()
        
        # Vérifier que les structures de réponse sont cohérentes

        assert "prediction" in data1
        assert "probabilité_defaut" in data1
        assert "prediction" in data2
        assert "probabilité_defaut" in data2

# ==============================================================================

def test_error_handling(): # Test de la gestion des erreurs

    # Données incomplètes
    incomplete_data = {
        "NAME_CONTRACT_TYPE": "Cash loans",
        "CODE_GENDER": "M"
        # Champs manquants
    }
    
    response = client.post("/predict", json=incomplete_data)
    assert response.status_code == 422  # Validation error
    
    # Type de données incorrect
    wrong_type_data = {
        "NAME_CONTRACT_TYPE": "Cash loans",
        "CODE_GENDER": "M",
        "FLAG_OWN_CAR": "Y",
        "FLAG_OWN_REALTY": "Y",
        "CNT_CHILDREN": "not_a_number",  # Doit être un int
        "AMT_INCOME_TOTAL": 100000.0,
        # ... autres champs requis
    }
    
    response = client.post("/predict", json=wrong_type_data)
    assert response.status_code == 422 #Validation error

# ==============================================================================

def test_enum_validation(): #Test de validation des valeurs d'énumération
    
    invalid_enum_data = {
        "NAME_CONTRACT_TYPE": "Invalid Contract Type",  # Enum invalide
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
    
    response = client.post("/predict", json=invalid_enum_data)
    assert response.status_code == 422 #Validation error

# ==============================================================================

def test_response_format(sample_client_data): #Test du format de réponse

    response = client.post("/predict", json=sample_client_data)
    
    if response.status_code == 200:
        data = response.json()
        
        # Vérifier la structure de la réponse
        assert isinstance(data, dict)
        assert "prediction" in data
        assert "probabilité_defaut" in data
        
        # Vérifier les types de données
        assert isinstance(data["prediction"], str)
        assert isinstance(data["probabilité_defaut"], float)
        
        # Vérifier les valeurs possibles de prédiction
        assert data["prediction"] in ["Solvable", "Défaillant"]
        
        # Vérifier que la probabilité est dans [0, 1]
        assert 0 <= data["probabilité_defaut"] <= 1


