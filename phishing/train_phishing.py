# optional: train a simple TFIDF + LogisticRegression on SMS Spam dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# prepare dataset: use SMS Spam Collection or other phishing dataset
# df = pd.read_csv("phishing/data/sms_spam.csv")  # columns: label,text
# df['y'] = df['label'].map({'ham':0,'spam':1})
# X_train, X_test, y_train, y_test = train_test_split(df['text'], df['y'], test_size=0.2, random_state=42)

# pipeline = Pipeline([
#     ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=20000)),
#     ("clf", LogisticRegression(max_iter=1000))
# ])
# pipeline.fit(X_train, y_train)
# print("Train done")
# joblib.dump(pipeline, "phishing/phishing_model.pkl")
