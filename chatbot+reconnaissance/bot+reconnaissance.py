import streamlit as st
import speech_recognition as sr
import nltk
import string

# Téléchargement des ressources NLTK
nltk.download('punkt', quiet=True)

# Dictionnaire de questions avec plusieurs réponses possibles
responses = {
    "qu'est-ce que la fonction de répartition": [
        "Soit X une variable aléatoire, on appelle fonction de répartition de X, que l’on note F_X, "
        "la fonction définie sur R par : F_X(x) = P(X ≤ x)."
    ],
    "qu'est-ce qu'une quantile d'ordre q": [
        """On appelle quantile d’ordre q de la variable X, où q ∈ [0, 1], la valeur xq telle que:<br>  
        P(X ≤ xq) = q<br> 
        ou, de même, FX(xq) = q."""
    ],
    "qu'est-ce que la théorie des probabilités": [
        """La théorie des probabilités a pour objet l’étude des phénomènes aléatoires ou du moins considérés comme tels par l’observateur. 
        Pour cela, on introduit le concept d’expérience aléatoire dont l’ensemble des résultats possibles constitue l’ensemble fondamental, noté habituellement Ω."""
    ],
    "qu'est-ce qu'une variable aléatoire": [
        """On parle de variable aléatoire (abréviation : v.a.) lorsque les résultats sont numériques, c’est-à-dire que Ω est identique à tout ou une partie de l’ensemble des nombres réels R.<br> 
        On distingue habituellement :<br>
        - les variables aléatoires discrètes pour lesquelles l’ensemble Ω des résultats possibles est un ensemble discret de valeurs numériques x1, x2, ..., xn,<br> 
        fini ou infini (typiquement : l’ensemble des entiers naturels) ;<br> 
        - les variables aléatoires continues pour lesquelles l’ensemble Ω est tout R (ou un intervalle de R ou, plus rarement, une union d’intervalles)."""
    ],
    "qu'est-ce qu'une espérance mathématique": [
        """On appelle espérance mathématique de X, si elle existe, la valeur notée E(X) telle que :<br> 
        E(X) = Σ (xi * pX(xi)) dans le cas discret,<br> 
        E(X) = ∫ (x * fX(x) dx) dans le cas continu.<br> 
        Du point de vue du graphe de fX (respectivement pX), cette valeur représente le centre de gravité de la distribution."""
    ],
    "qu'est-ce que l'espérance d'une fonction": [
        """Soit g(X) une fonction de la v.a. X, alors : 
        E(g(X)) = ∫ g(x) fX(x) dx dans le cas continu (si l’intégrale existe),<br> 
        E(g(X)) = Σ g(xi) pX(xi) dans le cas discret (si la somme existe).<br> 
        On voit donc que pour le calcul de E(g(X)), il suffit de remplacer la valeur de x par g(x) (ou xi par g(xi))."""
    ]
}

def preprocess_text(text):
    """Prétraiter le texte : conversion en minuscules et suppression de la ponctuation."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return nltk.sent_tokenize(text)


def chatbot(user_query):
    """Fonction principale du chatbot."""
    normalized_query = user_query.lower().strip()

    # Vérification des réponses directes
    for question in responses:
        # Utilise un ensemble de mots pour vérifier si tous les mots de la question sont présents
        question_words = set(question.lower().split())
        user_words = set(normalized_query.split())

        if question_words.issubset(user_words):
            return responses[question][0]

    return "Désolé, je ne sais pas répondre à cela."

def transcribe_speech():
    """Transcrire la parole en texte à l'aide de la reconnaissance vocale."""
    r = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("Parlez maintenant...")
        audio_text = r.listen(source)
        st.info("Transcription...")

        try:
            text = r.recognize_google(audio_text, language='fr-FR')
            st.success(f"Texte transcrit : {text}")  # Affiche le texte transcrit
            return text

        except sr.UnknownValueError:
            return "Erreur : Impossible de comprendre l'audio."
        except sr.RequestError as e:
            return f"Erreur de service : {e}"

def main():
    st.title("Chatbot Statistique et Probabilités")

    # Zone de saisie pour poser une question
    user_input = st.text_input("Posez votre question sur la statistique et la probabilité :")

    if user_input:
        response = chatbot(user_input)
        st.markdown("**Réponse du chatbot :** " + response, unsafe_allow_html=True)

    # Option pour la saisie vocale
    if st.button("Transcrire la parole"):
        speech_text = transcribe_speech()
        if speech_text and "Erreur" not in speech_text:  # Vérifie qu'il n'y a pas d'erreurs
            response = chatbot(speech_text)
            st.markdown("**Réponse du chatbot :** " + response, unsafe_allow_html=True)

if __name__ == "__main__":
    main()