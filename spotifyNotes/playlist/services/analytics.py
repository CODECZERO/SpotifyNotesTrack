from textblob import TextBlob
import pandas as pd
import plotly.express as px

def analyze_notes_sentiment(notes):
 #this function will find sentiment of notes
 
    sentiment_counts = {"postive":0 , "neutral":0, "negative":0}
    analyze_notes = []
    
    for n in notes:
        notes_text = n[0] if len(n) > 0 else ""
        analysis = TextBlob(notes_text)
        polarity = analysis.sentiment.polarity
    
    if polarity>0.1:
        sentiment = "postive"
        sentiment_counts["postive"] += 1
    elif polarity<-0.1:
        sentiment = "negative"
        sentiment_counts["negative"] += 1
    else:
        sentiment = "neutal"
        sentiment_counts["neutral"] += 1
        
    analyze_notes.append({
        "note_text": notes_text,
        "sentiment": sentiment,
        "polarity": polarity
    })
    
    return sentiment_counts, analyze_notes


def plot_sentiment_distribution(sentiment_counts):
    df = pd.DataFrame(list(sentiment_counts.items(), 
                         colums = ["Sentiment", "Count"]))
    
    fig=px.pie(df, names="Sentiment", values="Count", title="Notes Sentiment Distribution",
               color="Sentiment", color_discrete_map={"positive": "green", 
                                                      "neutral": "gray", 
                                                      "negative": "red"})
    return fig.to_html(full_html=False)