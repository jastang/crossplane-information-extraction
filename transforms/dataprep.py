import apache_beam as beam
import dataclasses

from model.datamodels import *
from nltk import ngrams, word_tokenize


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


class TokenizeAndLemmatize(beam.DoFn):
    # TODO(jastang): maybe use a sentence tokenizer instead.
    # Picking line break over a period since it gives us some contextual grouping for free.
    def __init__(self, delimiter="\n"):
        self.delimiter = delimiter

    def process(self, page: DocsPage):
        for sentence in page.content.split(self.delimiter):
            tokens = word_tokenize(sentence)

            result = TokenizedSentence(
                title=page.title,
                url=page.url,
                content=sentence,
                tokens=tokens
                # one_grams=[list(gram) for gram in ngrams(tokens, 1)],
                # two_grams=[list(gram) for gram in ngrams(tokens, 2)],
                # three_grams=[list(gram) for gram in ngrams(tokens, 3)],
                # four_grams=[],  # [list(gram) for gram in ngrams(tokens, 4)],
                # five_grams=[],  # [list(gram) for gram in ngrams(tokens, 5)],
                # six_grams=[],  # [list(gram) for gram in ngrams(tokens, 6)],
            )

            jsonl = dataclasses.asdict(result)

            yield jsonl
