# Cyberbullying Detection System 
# Project Overview:

The Cyberbullying Detection System is a web-based application designed to identify and classify cyberbullying content from user-input text. The system uses Machine Learning and Natural Language Processing (NLP) techniques to analyze messages and predict whether the content is bullying or non-bullying. The project aims to promote safer online communication by helping users recognize harmful content.

# Features:
User-friendly web interface
Real-time cyberbullying text prediction
Dashboard with system statistics
Prediction history tracking
Awareness and prevention tips
Emergency helpline information
Machine Learning-based text classification
Responsive design

# Technologies Used:
Frontend -
HTML5
CSS3
JavaScript
Bootstrap

Backend -
Python
Flask

Machine Learning -
Scikit-learn
Pandas
NumPy
NLTK

Database -
SQLite 

# Working Process:
1. User enters a message or text.
2. The text undergoes preprocessing:
Lowercasing
Removing special characters
Tokenization
Stop-word removal
3. The processed text is converted into numerical features using a vectorizer.
4. The trained Machine Learning model analyzes the text.
5. The system predicts whether the text contains cyberbullying content.
6. Results are displayed to the user and stored in the history section.

# Machine Learning Model:

The model is trained on a cyberbullying dataset containing labeled text samples.

Steps:
Data Collection
Data Cleaning
Text Preprocessing
Feature Extraction (TF-IDF/Count Vectorizer)
Model Training
Model Evaluation
Prediction
Possible Algorithms
Logistic Regression
Naive Bayes
Random Forest
Support Vector Machine (SVM)