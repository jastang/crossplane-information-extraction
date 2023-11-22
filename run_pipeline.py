import apache_beam as beam

import dataclasses
import json

from apache_beam.options.pipeline_options import PipelineOptions
from model.datamodels import *
from transforms.dataprep import ToTextSentimentSchema, TokenizeAndLemmatize

beam_options = PipelineOptions(runner="DirectRunner")

INPUT_FILE = "/Users/jasontang/Downloads/docs.json"

# "/Users/jasontang/Desktop/hacking/crossplane/general/2022-fall.json"


def run() -> None:
    with beam.Pipeline(options=beam_options) as pipeline:
        with open(INPUT_FILE, "rb") as f:
            page_data = (
                pipeline
                | "Read from Slack dump"
                # Note the format Slack exports with makes it difficult to use Beam's built-in ReadFromText
                >> beam.Create([record for record in json.loads(f.read())])
                | "Map to pages"
                >> beam.Map(
                    lambda row: DocsPage(
                        title=row["title"], url=row["url"], content=row["content"]
                    )
                )
            )

            # Extract topics
            _ = (
                page_data
                | "Extract topic naively"
                >> beam.Map(
                    lambda page: page.url.split("/")[-2:-1][0].replace("-", " ")
                )
                | "Write to file"
                >> beam.io.WriteToText(
                    file_path_prefix="topics", file_name_suffix=".txt", num_shards=1
                )
            )

            # Main processing
            _ = (
                page_data
                | "Extract sentences" >> beam.ParDo(TokenizeAndLemmatize())
                # | "Filter out stopwords" >> beam.ParDo(RemoveStopwords())
                # | "Generate n-grams" >> beam.ParDo(GenerateNGrams())
                | "Write index files"
                >> beam.io.WriteToText(
                    file_path_prefix="crossplane-docs",
                    file_name_suffix=".jsonl",
                    num_shards=5,
                )
            )

            # | "See what we're working with here" >> beam.Map(print)

            # | "Map to data container"
            # >> beam.Map(
            #     lambda row: CrossplaneSlackMessage(
            #         text=row["text"], ts=row["ts"], userid=row["user"]
            #     )
            # )
            # | "Convert to required jsonlines format for training"
            # >> beam.ParDo(ToTextSentimentSchema())
            # | "Coalesce into training file" >> beam.io.WriteToText(file_path_prefix="crossplane-slack-general", file_name_suffix=".jsonl", num_shards=1)


if __name__ == "__main__":
    run()
