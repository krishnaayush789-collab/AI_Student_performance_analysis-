import pandas as pd
from textblob import TextBlob
import os

# Load feedback dataset
df = pd.read_csv("data/feedback.csv")

# Function for sentiment analysis
def analyze_sentiment(text):

    analysis = TextBlob(str(text))
    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        return "Positive"

    elif polarity < -0.1:
        return "Negative"

    else:
        return "Neutral"


# Apply NLP sentiment analysis
df["Sentiment"] = df["Feedback"].apply(analyze_sentiment)

# Add polarity score
df["Polarity"] = df["Feedback"].apply(
    lambda x: TextBlob(str(x)).sentiment.polarity
)

# Save results
os.makedirs("data", exist_ok=True)

df.to_csv(
    "data/sentiment_results.csv",
    index=False
)

# Display results
print("NLP Analysis Completed Successfully!")

print("\nSentiment Distribution:")

print(df["Sentiment"].value_counts())

print("\nSample Analysis:")

print(
    df[["Student_ID", "Feedback", "Sentiment"]].head(10)
)

print("\nResults saved to data/sentiment_results.csv")
