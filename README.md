# crossplane-information-extraction
An [@upbound_io](https://www.github.com/upbound) hack week project applying information retrieval theory to a corpus of Crossplane documentation.

The idea is to create an inverted index with a simple Apache Beam pipeline that can serve as a data enrichment source for other ML applications, for example:

- a chatbot application using an LLM is prone to "hallucinating" non-existent documentation links, even if it summarizes the question well.
- a more finely-tuned classification model to help answer questions based on the inferred context of tokens and where they appear in the document (span).

## Quickstart

Set up your virtual environment
```(shell)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You may need to download local copies of NLTK assets like a stopword corpus and the punkt tokenization model.

Run the pipeline (DirectRunner) to see it in action:
```(shell)
python run_pipeline.py
```

## TODO
A lot of stuff

