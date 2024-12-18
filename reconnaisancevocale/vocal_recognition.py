import streamlit as st
import speech_recognition as sr
from deepgram import Deepgram
import wave

# Remplacez par votre clé API valide
DEEPGRAM_API_KEY = 'e6fe622578c8a839238aba96b06f59d58ba72b5a'
deepgram = Deepgram(DEEPGRAM_API_KEY)


def transcribe_with_deepgram(audio_data):
    response = deepgram.transcription.sync_prerecorded(
        {'buffer': audio_data, 'mimetype': 'audio/wav'},  # Spécifiez le type MIME
        {'punctuate': True}
    )
    return response['channel']['alternatives'][0]['transcript']


def transcribe_with_google(audio_data, language):
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_data)
    with audio_file as source:
        audio = r.record(source)  # Lire le fichier audio
    return r.recognize_google(audio, language=language)


def transcribe_with_sphinx(audio_data):
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_data)
    with audio_file as source:
        audio = r.record(source)  # Lire le fichier audio
    return r.recognize_sphinx(audio)


def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Parlez maintenant...")
        audio_text = r.listen(source)
        st.info("Enregistrement terminé. Traitement...")

        # Sauvegarder l'audio dans un fichier WAV
        with wave.open("enregistrement.wav", 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16 bits
            wf.setframerate(44100)  # Fréquence d'échantillonnage
            wf.writeframes(audio_text.get_wav_data())

        return "enregistrement.wav"


def main():
    st.title("Speech Recognition App")

    if st.button("Démarrer l'enregistrement"):
        audio_file_path = record_audio()
        st.success("Enregistrement sauvegardé : " + audio_file_path)

        # Lecture du fichier audio enregistré
        audio_data = audio_file_path

        # Sélection de l'API de transcription
        api_choice = st.selectbox("Choisissez l'API de reconnaissance vocale :", ["Google", "Sphinx", "Deepgram"])
        language = st.selectbox("Choisissez la langue :", ["fr-FR", "en-US", "es-ES", "de-DE"])

        try:
            if api_choice == "Deepgram":
                with open(audio_data, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                text = transcribe_with_deepgram(audio_bytes)
            elif api_choice == "Google":
                text = transcribe_with_google(audio_data, language)
            elif api_choice == "Sphinx":
                text = transcribe_with_sphinx(audio_data)
            else:
                text = "Erreur : API non reconnue."

            st.write("Transcription :", text)
        except Exception as e:
            st.error(f"Erreur lors de la transcription : {e}")


if __name__ == "__main__":
    main()