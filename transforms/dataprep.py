import apache_beam as beam
import dataclasses

from model.datamodels import *
from nltk import ngrams, word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords


class ToTextSentimentSchema(beam.DoFn):
    def process(self, msg: CrossplaneSlackMessage):
        sentiment = TextSentimentSchema(
            sentimentAnnotation=SentimentAnnotation(0),
            textContent=msg.text,
            # dataItemResourceLabels=DataAnnotations(),
        )

        jsonl = dataclasses.asdict(sentiment)
        # jsonl["dataItemResourceLabels"][
        #     "aiplatform.googleapis.com/ml_use"
        # ] = Usage.TRAIN.value

        yield jsonl


class Tokenize(beam.DoFn):
    # TODO(jastang): maybe use a sentence tokenizer instead.
    # Picking line break over a period since it gives us some contextual grouping for free.
    def __init__(self, delimiter="\n"):
        self.delimiter = delimiter

    def process(self, page: DocsPage):
        for sentence in page.content.split(self.delimiter):
            tokens = word_tokenize(sentence)

            result = TokenizedSentence(
                title=page.title, url=page.url, content=sentence, tokens=tokens
            )

            yield result


class Lemmatize(beam.DoFn):
    def __init__(self, lemmatizer=WordNetLemmatizer()):
        self.lemmatizer = lemmatizer

    def process(self, sentence: TokenizedSentence):
        result = TokenizedSentence(
            title=sentence.title,
            url=sentence.url,
            content=sentence.content,
            tokens=[self.lemmatizer.lemmatize(token) for token in sentence.tokens],
        )

        yield result


class RemoveStopWords(beam.DoFn):
    def __init__(self, language="english"):
        self.corpus = stopwords.words(language)

    def process(self, sentence: TokenizedSentence):
        result = TokenizedSentence(
            title=sentence.title,
            url=sentence.url,
            content=sentence.content,
            tokens=[token for token in sentence.tokens if token not in self.corpus],
        )

        yield result


class GenerateNGrams(beam.DoFn):
    def process(self, sentence: TokenizedSentence):
        result = NGramSentence(
            title=sentence.title,
            url=sentence.url,
            content=sentence.content,
            one_grams=[list(gram) for gram in ngrams(sentence.tokens, 1)],
            two_grams=[list(gram) for gram in ngrams(sentence.tokens, 2)],
            three_grams=[list(gram) for gram in ngrams(sentence.tokens, 3)],
        )

        # TODO(jastang): factor this out to the final transform before writing
        jsonl = dataclasses.asdict(result)

        yield jsonl
