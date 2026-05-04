# Install first:
# pip install textblob nltk

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

nltk.download('punkt')
nltk.download('stopwords')

# Input
text = input("Enter a sentence: ")

# Tokenization
words = word_tokenize(text)
print("\nTokens:", words)

# Remove Stopwords
filtered_words = [w for w in words if w.lower() not in stopwords.words('english')]
print("After Stopword Removal:", filtered_words)

# Sentiment Analysis
blob = TextBlob(text)
sentiment = blob.sentiment

print("\nPolarity:", sentiment.polarity)
print("Subjectivity:", sentiment.subjectivity)

if sentiment.polarity > 0:
    print("Sentiment: Positive 😊")
elif sentiment.polarity < 0:
    print("Sentiment: Negative 😠")
else:
    print("Sentiment: Neutral 😐")