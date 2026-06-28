import streamlit as st
import requests
import datetime

# Configuration
API_KEY = '8583d7dc-7548-4a8d-8097-84ebdf95eae0'
STOP_ID = 'stop_area:SNCF:87781278' 
TEMPS_TRAJET_VERS_POINT = 3 

st.set_page_config(page_title="Train Tracker Agde", page_icon="🚆")
st.title("🚆 Train Tracker Agde")

def get_trains():
    url = f"https://api.navitia.io/v1/coverage/sncf/stop_areas/{STOP_ID}/departures?count=5"
    response = requests.get(url, auth=(API_KEY, ''))
    return response.json() if response.status_code == 200 else None

data = get_trains()

if data and 'departures' in data:
    st.subheader("Prochains départs à Agde")
    maintenant = datetime.datetime.now()
    
    for dep in data['departures']:
        heure_str = dep['stop_date_time']['departure_date_time']
        heure_train = datetime.datetime.strptime(heure_str, "%Y%m%dT%H%M%S")
        heure_passage_point = heure_train + datetime.timedelta(minutes=TEMPS_TRAJET_VERS_POINT)
        
        # Affichage ligne
        col1, col2 = st.columns([1, 3])
        col1.metric("Ligne", dep['display_informations']['code'])
        col2.write(f"Direction: **{dep['display_informations']['direction']}**")
        
        # Logique d'alerte
        delta = (heure_passage_point - maintenant).total_seconds() / 60
        if 0 < delta <= 5:
            st.error(f"⚠️ ALERTE : Le train passe à votre point GPS dans {round(delta)} min !")
        elif delta > 5:
            st.info(f"Passage estimé au point GPS : {heure_passage_point.strftime('%H:%M')}")
else:
    st.write("Erreur de connexion aux données SNCF.")