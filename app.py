import streamlit as st
import requests
import time

st.set_page_config(page_title="Avonova Auto-Coach", layout="wide")

st.title("🎙️ Avonova Assist - Automatisk Live-Coach")

with st.sidebar:
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Status: Mikrofonen lyssnar via webbläsaren.")

# JavaScript för att fånga röst och skicka till Streamlit automatiskt
st.components.v1.html(
    """
    <script>
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'sv-SE';
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function(event) {
        var result = event.results[event.results.length - 1][0].transcript;
        window.parent.postMessage({type: 'streamlit:set_widget_value', key: 'transcript_input', value: result}, '*');
    };

    recognition.start();
    </script>
    """,
    height=0,
)

# En dold input som uppdateras av rösten
if 'transcript_input' not in st.session_state:
    st.session_state.transcript_input = ""

# Visar vad som hörs just nu
st.subheader("Hör just nu:")
transcript = st.text_area("Live-logg:", value=st.session_state.transcript_input, height=100)

# Plats för coachens tips
st.subheader("💡 Coachning (Uppdateras automatiskt)")
advice_area = st.empty()

# Logik för att skicka till AI automatiskt vid förändring
if len(transcript) > 20: # Vänta tills vi har en mening
    if api_key:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        prompt = f"Jag är i ett säljmöte för Avonova Assist. Här är vad som sägs: '{transcript}'. Ge mig ett extremt kort råd på nästa drag eller svar på invändning."
        
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
            data = res.json()
            if 'candidates' in data:
                tip = data['candidates'][0]['content']['parts'][0]['text']
                advice_area.success(tip)
        except:
            pass
