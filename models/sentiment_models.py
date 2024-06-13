import joblib

# Load the trained model and vectorizer
model = joblib.load('models/sentiment_model.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

def analyze_emotion(text):
    vect_text = vectorizer.transform([text])
    sentiment = model.predict(vect_text)[0]
    return sentiment

# Test the emotion analysis
if __name__ == "__main__":
    text = "I'm so frustrated."
    print(analyze_emotion(text))
