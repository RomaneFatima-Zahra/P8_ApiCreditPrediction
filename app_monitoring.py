import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os
import streamlit.components.v1 as components

# Configuration de la page
st.set_page_config(
    page_title="Prédiction de Solvabilité",
    page_icon="💰",
    layout="wide"
)

# Configuration des chemins
API_URL = "http://localhost:8000"
LOG_PATH = "logs/api_logger.log"
INPUT_DATA_PATH = "data/input_reference.csv"
OUTPUT_DATA_PATH = "data/output_reference.csv"
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# ==================== FONCTIONS UTILITAIRES ====================

def check_api_connection():
    try:
        response = requests.get(f"{API_URL}/", timeout=2)
        return response.status_code == 200
    except:
        return False

def load_api_logs():
    """Charge les logs structurés de l'API"""
    if not os.path.exists(LOG_PATH):
        return pd.DataFrame()
    
    entries = []
    with open(LOG_PATH, "r") as f:
        for line in f:
            try:
                msg = line.strip().split(" - ", 2)[-1]
                log_json = json.loads(msg)
                if isinstance(log_json, dict):
                    entries.append(log_json)
            except:
                continue
    return pd.DataFrame(entries)

def analyze_predictions(logs_df):
    """Analyse les prédictions à partir des logs"""
    pred_logs = logs_df[logs_df["event"] == "prediction"].copy()
    
    if pred_logs.empty:
        return None, None, None
    
    # Extraire les inputs
    input_df = pd.json_normalize(pred_logs["input_data"])
    input_df.reset_index(drop=True, inplace=True)
    
    # Extraire les outputs
    output_df = pd.DataFrame()
    output_df["prediction"] = pred_logs["prediction"].values
    output_df["probabilité_defaut"] = pred_logs["probabilité_defaut"].values
    output_df["TARGET"] = pred_logs["prediction"].map({"Solvable": 0, "Défaillant": 1})
    output_df.reset_index(drop=True, inplace=True)
    
    return input_df, output_df, pred_logs

def analyze_http_metrics(logs_df):
    """Analyse les métriques HTTP"""
    http_logs = logs_df[logs_df["event"] == "http_request"].copy()
    
    if http_logs.empty:
        return None
    
    http_logs["timestamp"] = pd.to_datetime(http_logs["timestamp"])
    http_logs["date"] = http_logs["timestamp"].dt.date
    http_logs["duration_ms"] = http_logs["duration"] * 1000
    
    return http_logs

def detect_latency_anomalies(http_logs):
    """Détecte les anomalies de latence"""
    mean_dur = http_logs["duration_ms"].mean()
    std_dur = http_logs["duration_ms"].std()
    http_logs["latency_anomaly"] = http_logs["duration_ms"] > (mean_dur + 3 * std_dur)
    return http_logs[http_logs["latency_anomaly"]]

# ==================== HEADER ====================
st.title("🏦 Système de Prédiction de Solvabilité Client")
st.markdown("---")

# Vérification de la connexion à l'API
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if check_api_connection():
        st.success("✅ API connectée")
    else:
        st.error("❌ API non disponible")

# Création des onglets
tab1, tab2, tab3= st.tabs([
    "📝 Faire une prédiction", 
    "📊 Distribution des Prédictions",
    "📈 Métriques Opérationnelles", 
])

# ==================== ONGLET 1 : PRÉDICTION ====================
with tab1:
    st.header("Saisir les informations du client")
    
    with st.form("prediction_form"):
        # Section 1 : Informations générales
        st.subheader("1️⃣ Informations générales")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            NAME_CONTRACT_TYPE = st.selectbox("Type de contrat", ["Cash loans", "Revolving loans"])
            CODE_GENDER = st.selectbox("Genre", ["M", "F", "XNA"])
            FLAG_OWN_CAR = st.selectbox("Possède une voiture", ["N", "Y"])
            
        with col2:
            FLAG_OWN_REALTY = st.selectbox("Possède un bien immobilier", ["N", "Y"])
            CNT_CHILDREN = st.number_input("Nombre d'enfants", min_value=0, value=0)
            CNT_FAM_MEMBERS = st.number_input("Membres de la famille", min_value=1.0, value=2.0, step=0.5)
            
        with col3:
            NAME_FAMILY_STATUS = st.selectbox("Statut familial", 
                ["Married", "Single / not married", "Civil marriage", "Separated", "Widow", "Unknown"])
            NAME_HOUSING_TYPE = st.selectbox("Type de logement",
                ["House / apartment", "With parents", "Municipal apartment", "Rented apartment", 
                 "Office apartment", "Co-op apartment"])
        
        st.markdown("---")
        
        # Section 2 : Informations financières
        st.subheader("2️⃣ Informations financières")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            AMT_INCOME_TOTAL = st.number_input("Revenu total annuel", min_value=1000.0, value=150000.0, step=1000.0)
            AMT_CREDIT = st.number_input("Montant du crédit", min_value=1000.0, value=500000.0, step=1000.0)
            
        with col2:
            AMT_ANNUITY = st.number_input("Annuité", min_value=1000.0, value=25000.0, step=1000.0)
            AMT_GOODS_PRICE = st.number_input("Prix du bien", min_value=1000.0, value=450000.0, step=1000.0)
            
        with col3:
            CREDIT_INCOME_PERCENT = st.number_input("Crédit / Revenu (%)", value=0.33, step=0.01)
            ANNUITY_INCOME_PERCENT = st.number_input("Annuité / Revenu (%)", value=0.17, step=0.01)
            CREDIT_TERM = st.number_input("Durée du crédit (mois)", min_value=1.0, value=36.0, step=1.0)
        
        st.markdown("---")
        
        # Section 3 : Informations professionnelles
        st.subheader("3️⃣ Informations professionnelles")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            NAME_INCOME_TYPE = st.selectbox("Type de revenu",
                ["Working", "Commercial associate", "Pensioner", "State servant", 
                 "Unemployed", "Student", "Businessman", "Maternity leave"])
            NAME_EDUCATION_TYPE = st.selectbox("Niveau d'éducation",
                ["Secondary / secondary special", "Higher education", "Incomplete higher", 
                 "Lower secondary", "Academic degree"])
            
        with col2:
            OCCUPATION_TYPE = st.selectbox("Type d'occupation",
                ["Laborers", "Sales staff", "Core staff", "Managers", "Drivers", 
                 "High skill tech staff", "Accountants", "Medicine staff", "Security staff",
                 "Cooking staff", "Cleaning staff", "Private service staff", "Low-skill Laborers",
                 "Waiters/barmen staff", "Secretaries", "Realty agents", "HR staff", "IT staff"])
            ORGANIZATION_TYPE = st.selectbox("Type d'organisation",
                ["Business Entity Type 3", "XNA", "Self-employed", "Other", "Medicine",
                 "Business Entity Type 2", "Government", "School", "Trade: type 7",
                 "Kindergarten", "Construction", "Business Entity Type 1", "Transport: type 4",
                 "Trade: type 3", "Industry: type 9", "Industry: type 3", "Security",
                 "Housing", "Industry: type 11", "Military", "Bank", "Agriculture", "Police"])
            
        with col3:
            DAYS_EMPLOYED = st.number_input("Jours d'emploi (négatif)", max_value=0, value=-1000)
            DAYS_EMPLOYED_PERCENT = st.number_input("% Emploi / Âge", value=0.3, step=0.01)
        
        st.markdown("---")
        
        # Section 4 : Informations personnelles
        st.subheader("4️⃣ Informations personnelles et dates")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            DAYS_BIRTH = st.number_input("Jours de naissance (négatif)", max_value=0, value=-15000)
            DAYS_REGISTRATION = st.number_input("Jours d'enregistrement", value=-3000)
            DAYS_ID_PUBLISH = st.number_input("Jours de publication ID", value=-2000)
            DAYS_LAST_PHONE_CHANGE = st.number_input("Jours dernier changement téléphone", value=-1000.0)
            
        with col2:
            NAME_TYPE_SUITE = st.selectbox("Accompagnement",
                ["Unaccompanied", "Family", "Spouse, partner", "Children", "Other_B", "Other_A", "Group of people"])
            WEEKDAY_APPR_PROCESS_START = st.selectbox("Jour de la semaine",
                ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"])
            HOUR_APPR_PROCESS_START = st.slider("Heure de début du processus", 0, 23, 12)
            
        with col3:
            FLAG_EMP_PHONE = st.selectbox("Téléphone employeur", [0, 1])
            FLAG_WORK_PHONE = st.selectbox("Téléphone travail", [0, 1])
            FLAG_PHONE = st.selectbox("Téléphone", [0, 1])
            FLAG_EMAIL = st.selectbox("Email", [0, 1])
        
        st.markdown("---")
        
        # Section 5 : Informations régionales
        st.subheader("5️⃣ Informations régionales et immobilières")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            REGION_POPULATION_RELATIVE = st.number_input("Population relative région", value=0.02, step=0.001)
            REGION_RATING_CLIENT = st.number_input("Rating région client", value=2)
            REGION_RATING_CLIENT_W_CITY = st.number_input("Rating région avec ville", value=2)
            
        with col2:
            REG_REGION_NOT_LIVE_REGION = st.selectbox("Région enregistrement ≠ résidence", [0, 1])
            REG_REGION_NOT_WORK_REGION = st.selectbox("Région enregistrement ≠ travail", [0, 1])
            LIVE_REGION_NOT_WORK_REGION = st.selectbox("Région résidence ≠ travail", [0, 1])
            
        with col3:
            REG_CITY_NOT_LIVE_CITY = st.selectbox("Ville enregistrement ≠ résidence", [0, 1])
            REG_CITY_NOT_WORK_CITY = st.selectbox("Ville enregistrement ≠ travail", [0, 1])
            LIVE_CITY_NOT_WORK_CITY = st.selectbox("Ville résidence ≠ travail", [0, 1])
        
        st.markdown("---")
        
        # Section 6 : Autres informations
        st.subheader("6️⃣ Autres informations")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            FLOORSMAX_AVG = st.number_input("Étages max moyen", value=0.5, step=0.1)
            LIVINGAREA_AVG = st.number_input("Surface habitable moyenne", value=0.3, step=0.01)
            YEARS_BEGINEXPLUATATION_MODE = st.number_input("Années début exploitation", value=0.9, step=0.1)
            
        with col2:
            OBS_30_CNT_SOCIAL_CIRCLE = st.number_input("Observations cercle social 30j", value=2.0, step=0.5)
            DEF_30_CNT_SOCIAL_CIRCLE = st.number_input("Défauts cercle social 30j", value=0.0, step=0.5)
            
        with col3:
            PREVIOUS_LOANS_COUNT = st.number_input("Nombre de prêts précédents", value=1.0, step=0.5)
        
        # Bouton de soumission
        st.markdown("---")
        submitted = st.form_submit_button("🔮 Faire la prédiction", use_container_width=True)
        
        if submitted:
            data = {
                "NAME_CONTRACT_TYPE": NAME_CONTRACT_TYPE,
                "CODE_GENDER": CODE_GENDER,
                "FLAG_OWN_CAR": FLAG_OWN_CAR,
                "FLAG_OWN_REALTY": FLAG_OWN_REALTY,
                "CNT_CHILDREN": CNT_CHILDREN,
                "AMT_INCOME_TOTAL": AMT_INCOME_TOTAL,
                "AMT_CREDIT": AMT_CREDIT,
                "AMT_ANNUITY": AMT_ANNUITY,
                "AMT_GOODS_PRICE": AMT_GOODS_PRICE,
                "NAME_TYPE_SUITE": NAME_TYPE_SUITE,
                "NAME_INCOME_TYPE": NAME_INCOME_TYPE,
                "NAME_EDUCATION_TYPE": NAME_EDUCATION_TYPE,
                "NAME_FAMILY_STATUS": NAME_FAMILY_STATUS,
                "NAME_HOUSING_TYPE": NAME_HOUSING_TYPE,
                "REGION_POPULATION_RELATIVE": REGION_POPULATION_RELATIVE,
                "DAYS_BIRTH": DAYS_BIRTH,
                "DAYS_EMPLOYED": DAYS_EMPLOYED,
                "DAYS_REGISTRATION": DAYS_REGISTRATION,
                "DAYS_ID_PUBLISH": DAYS_ID_PUBLISH,
                "FLAG_EMP_PHONE": FLAG_EMP_PHONE,
                "FLAG_WORK_PHONE": FLAG_WORK_PHONE,
                "FLAG_PHONE": FLAG_PHONE,
                "FLAG_EMAIL": FLAG_EMAIL,
                "OCCUPATION_TYPE": OCCUPATION_TYPE,
                "CNT_FAM_MEMBERS": CNT_FAM_MEMBERS,
                "REGION_RATING_CLIENT": REGION_RATING_CLIENT,
                "REGION_RATING_CLIENT_W_CITY": REGION_RATING_CLIENT_W_CITY,
                "WEEKDAY_APPR_PROCESS_START": WEEKDAY_APPR_PROCESS_START,
                "HOUR_APPR_PROCESS_START": HOUR_APPR_PROCESS_START,
                "REG_REGION_NOT_LIVE_REGION": REG_REGION_NOT_LIVE_REGION,
                "REG_REGION_NOT_WORK_REGION": REG_REGION_NOT_WORK_REGION,
                "LIVE_REGION_NOT_WORK_REGION": LIVE_REGION_NOT_WORK_REGION,
                "REG_CITY_NOT_LIVE_CITY": REG_CITY_NOT_LIVE_CITY,
                "REG_CITY_NOT_WORK_CITY": REG_CITY_NOT_WORK_CITY,
                "LIVE_CITY_NOT_WORK_CITY": LIVE_CITY_NOT_WORK_CITY,
                "ORGANIZATION_TYPE": ORGANIZATION_TYPE,
                "FLOORSMAX_AVG": FLOORSMAX_AVG,
                "LIVINGAREA_AVG": LIVINGAREA_AVG,
                "YEARS_BEGINEXPLUATATION_MODE": YEARS_BEGINEXPLUATATION_MODE,
                "OBS_30_CNT_SOCIAL_CIRCLE": OBS_30_CNT_SOCIAL_CIRCLE,
                "DEF_30_CNT_SOCIAL_CIRCLE": DEF_30_CNT_SOCIAL_CIRCLE,
                "DAYS_LAST_PHONE_CHANGE": DAYS_LAST_PHONE_CHANGE,
                "PREVIOUS_LOANS_COUNT": PREVIOUS_LOANS_COUNT,
                "CREDIT_INCOME_PERCENT": CREDIT_INCOME_PERCENT,
                "ANNUITY_INCOME_PERCENT": ANNUITY_INCOME_PERCENT,
                "CREDIT_TERM": CREDIT_TERM,
                "DAYS_EMPLOYED_PERCENT": DAYS_EMPLOYED_PERCENT
            }
            
            try:
                with st.spinner("Analyse en cours..."):
                    response = requests.post(f"{API_URL}/predict", json=data)
                    
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Prédiction effectuée avec succès !")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if result["prediction"] == "Solvable":
                            st.success(f"### ✅ Client {result['prediction']}")
                        else:
                            st.error(f"### ❌ Client {result['prediction']}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Impossible de se connecter à l'API. Vérifiez qu'elle est bien lancée sur http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")

# ==================== ONGLET 2 : DISTRIBUTION DES PRÉDICTIONS ====================
with tab2:
    st.header("📊 Distribution des Prédictions")
    
    if st.button("🔄 Rafraîchir les données", key="refresh_dist"):
        st.rerun()
    
    logs_df = load_api_logs()
    
    if not logs_df.empty:
        input_df, output_df, pred_logs = analyze_predictions(logs_df)
        
        if output_df is not None and not output_df.empty:
            # Statistiques globales
            total_predictions = len(output_df)
            nb_solvable = (output_df["prediction"] == "Solvable").sum()
            nb_defaillant = (output_df["prediction"] == "Défaillant").sum()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total de prédictions", total_predictions)
            with col2:
                st.metric("✅ Solvables", nb_solvable, 
                         delta=f"{(nb_solvable/total_predictions*100):.1f}%")
            with col3:
                st.metric("❌ Défaillants", nb_defaillant,
                         delta=f"{(nb_defaillant/total_predictions*100):.1f}%")
            
            st.markdown("---")
            
            # Graphiques
            col1, col2 = st.columns(2)
            
            with col1:
                # Diagramme circulaire
                fig_pie = px.pie(
                    values=[nb_solvable, nb_defaillant],
                    names=["Solvable", "Défaillant"],
                    title="Répartition des prédictions",
                    color_discrete_sequence=["#00cc96", "#ef553b"]
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Diagramme en barres
                fig_bar = go.Figure(data=[
                    go.Bar(name='Prédictions', x=['Solvable', 'Défaillant'], 
                           y=[nb_solvable, nb_defaillant],
                           marker_color=['#00cc96', '#ef553b'])
                ])
                fig_bar.update_layout(title="Nombre de prédictions par catégorie")
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Distribution des probabilités
            st.markdown("---")
            st.subheader("Distribution des probabilités de défaut")
            
            fig_hist = px.histogram(
                output_df, 
                x="probabilité_defaut",
                nbins=50,
                title="Distribution des probabilités de défaut",
                labels={"probabilité_defaut": "Probabilité de défaut"},
                color_discrete_sequence=["#636efa"]
            )
            fig_hist.add_vline(x=0.5, line_dash="dash", line_color="red", 
                              annotation_text="Seuil de décision")
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Tableau des dernières prédictions
            st.markdown("---")
            st.subheader("Dernières prédictions")
            display_df = output_df[["prediction", "probabilité_defaut"]].tail(10).copy()
            display_df.index = range(len(display_df), 0, -1)
            st.dataframe(display_df, use_container_width=True)
            
        else:
            st.info("📊 Aucune prédiction trouvée dans les logs. Effectuez des prédictions pour voir les statistiques.")
    else:
        st.warning("⚠️ Aucun log disponible. Vérifiez que l'API est lancée et que des prédictions ont été faites.")




# ==================== ONGLET 4 : MÉTRIQUES OPÉRATIONNELLES ====================
with tab3:
    st.header("📈 Métriques Opérationnelles")
    
    if st.button("🔄 Rafraîchir les métriques", key="refresh_metrics"):
        st.rerun()
    
    logs_df = load_api_logs()
    
    if not logs_df.empty:
        http_logs = analyze_http_metrics(logs_df)
        
        if http_logs is not None and not http_logs.empty:
            # Métriques globales
            st.subheader("📊 Métriques Globales")
            
            total_requests = len(http_logs)
            error_rate = (http_logs["status_code"] >= 400).mean() * 100
            avg_latency = http_logs["duration_ms"].mean()
            p95_latency = http_logs["duration_ms"].quantile(0.95)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total requêtes", total_requests)
            with col2:
                st.metric("Taux d'erreur", f"{error_rate:.2f}%",
                         delta="Normal" if error_rate < 5 else "⚠️ Élevé")
            with col3:
                st.metric("Latence moyenne", f"{avg_latency:.2f} ms")
            with col4:
                st.metric("Latence P95", f"{p95_latency:.2f} ms")
            
            st.markdown("---")
            
            # Graphiques de latence
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution de la latence
                fig_latency = px.line(
                    http_logs, 
                    x="timestamp", 
                    y="duration_ms",
                    title="Évolution de la latence",
                    labels={"duration_ms": "Latence (ms)", "timestamp": "Temps"}
                )
                fig_latency.add_hline(y=avg_latency, line_dash="dash", 
                                     line_color="green", annotation_text="Moyenne")
                fig_latency.add_hline(y=p95_latency, line_dash="dash", 
                                     line_color="orange", annotation_text="P95")
                st.plotly_chart(fig_latency, use_container_width=True)
            
            with col2:
                # Distribution de la latence
                fig_hist_latency = px.histogram(
                    http_logs,
                    x="duration_ms",
                    nbins=30,
                    title="Distribution de la latence",
                    labels={"duration_ms": "Latence (ms)"}
                )
                st.plotly_chart(fig_hist_latency, use_container_width=True)
            
            st.markdown("---")
            
            # Taux d'erreur par endpoint
            st.subheader("🎯 Taux d'erreur par endpoint")
            
            error_by_path = (
                http_logs.groupby("path")["status_code"]
                .apply(lambda x: (x >= 400).mean() * 100)
                .reset_index(name="error_rate_%")
            )
            
            fig_error = px.bar(
                error_by_path,
                x="path",
                y="error_rate_%",
                title="Taux d'erreur par endpoint",
                labels={"error_rate_%": "Taux d'erreur (%)", "path": "Endpoint"},
                color="error_rate_%",
                color_continuous_scale="Reds"
            )
            st.plotly_chart(fig_error, use_container_width=True)

