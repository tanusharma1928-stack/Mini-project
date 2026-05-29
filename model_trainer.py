import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

# Sample Dataset for Training
data = {
    'text': [
        'I love your work!', 'You are a loser and I hate you', 
        'Have a great day!', 'Kill yourself, nobody likes you',
        'This is a wonderful post', 'You are so ugly and stupid',
        'Let’s go for a walk', 'Shut up you idiot',
        'I appreciate your help', 'Get lost, you are worthless',
        'You are the best', 'I will find you and hurt you',
        'Amazing project!', 'Stop breathing, you fail at life'
    ],
    'label': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['text'])
y = df['label']

# SVM Classifier
model = SVC(probability=True, kernel='linear')
model.fit(X, y)

with open('model.pkl', 'wb') as f: pickle.dump(model, f)
with open('vectorizer.pkl', 'wb') as f: pickle.dump(vectorizer, f)

print("Model Trained and Saved successfully!")