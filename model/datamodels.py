from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


@dataclass(slots=True)
class CrossplaneSlackMessage:
    """Data container for a Slack message"""

    text: str
    ts: float
    userid: str


class Usage(Enum):
    TRAIN = "training"
    TEST = "test"
    VAL = "validation"


class Sentiment(Enum):
    """Strawman classes. Did not do any exploratory data analysis on distributions etc."""

    NEGATIVE = 0
    NEUTRAL = 1
    POSITIVE = 2


@dataclass
class SentimentAnnotation:
    sentiment: Sentiment
    sentimentMax: Sentiment = Sentiment.POSITIVE.value


@dataclass
class DataAnnotations:
    ml_use: Optional[Usage] = None


@dataclass
class TextSentimentSchema:
    """Data container for our NLP training dataset"""

    sentimentAnnotation: SentimentAnnotation
    textContent: str
    # dataItemResourceLabels: Optional[DataAnnotations] = None

@dataclass
class DocsPage:
    """Data container for a page of the Crossplane docs"""

    title: str
    url: str
    content: str

@dataclass
class TokenizedSentence:
    """Data container for a sentence on a page"""

    title: str
    url: str
    content: str
    tokens: List[str]


@dataclass
class NGramSentence:
    """Data container for ngrams generated from a sentence's tokens"""

    title: str
    url: str
    content: str
    one_grams: List[tuple]
    two_grams: List[tuple]
    three_grams: List[tuple]
    # four_grams: List[tuple]
    # five_grams: List[tuple]
    # six_grams: List[tuple]