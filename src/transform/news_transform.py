# src/transform/news_transform.py

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

summarizer = LsaSummarizer()
analyzer = SentimentIntensityAnalyzer()

def summarize_text(text, sentences_count=2):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summary = summarizer(parser.document, sentences_count)
    return " ".join(str(s) for s in summary)

def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    return scores["compound"]
