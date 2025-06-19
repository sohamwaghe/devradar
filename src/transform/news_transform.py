# src/transform/news_transform.py

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def summarize_text(text):
    if not text:
        return ""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 1)  # just 1 sentence
    result = " ".join(str(sentence) for sentence in summary)
    return result[:200] + "..." if len(result) > 200 else result

def get_sentiment_label(text):
    if not text:
        return "Neutral"
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.2:
        return "Positive"
    elif score <= -0.2:
        return "Negative"
    else:
        return "Neutral"

