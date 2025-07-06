import os

from haystack.components.builders.prompt_builder import PromptBuilder
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack_integrations.components.embedders.fastembed import FastembedTextEmbedder


from haystack.components.readers import ExtractiveReader
from haystack.components.rankers import TransformersSimilarityRanker
from haystack.components.joiners.document_joiner import DocumentJoiner

from milvus_haystack import MilvusDocumentStore, MilvusEmbeddingRetriever

from pymilvus import connections, list_collections



async def retrieval_model(question ):
    
    prompt_template = """Answer under 20 words, Answer the following query under 20 words based on the provided context and explain but not too much no more than 20 word. If the context does
                            not include an answer, try to answer the best answer based on the provided context.\n
                            just say the answer, do not say anything else, do not say "The answer is" or "answer under 20 words:" or anything like this.\n
                            answer in the same language as the Query. answer in a concise and correct form\n
                            do not repeat the prompt rules, just answer the Query.\n
                            do not repeat the answer, just answer one time.\n 
                            Query: {{query}}
                            Documents:
                            {% for doc in documents %}
                            {{ doc.content }}
                            {% endfor %}
                            Answer: 
                        """
    model = "sentence-transformers/multi-qa-mpnet-base-dot-v1"

    document_store = MilvusDocumentStore(
    connection_args={"uri": "tcp://standalone:19530"})


    retriever = MilvusEmbeddingRetriever(
		document_store=document_store,
        )   




    # ranker = TransformersSimilarityRanker()
    # ranker.warm_up()

    text_embedder = FastembedTextEmbedder(
        model="Snowflake/snowflake-arctic-embed-s")
    text_embedder.warm_up()

    extractive_qa_pipeline = Pipeline()
    extractive_qa_pipeline.add_component(instance=retriever, name="retriever")

    extractive_qa_pipeline.add_component(
        instance=text_embedder, name="text_embedder")
 

    # extractive_qa_pipeline.add_component(instance=ranker, name="ranker")


    extractive_qa_pipeline.connect("text_embedder", "retriever")
    # extractive_qa_pipeline.connect("joiner.documents", "ranker.documents")


    doc_results = extractive_qa_pipeline.run({"text_embedder": {"text": question}})
    print("document_count", document_store.count_documents())
    print(doc_results)


    builder = PromptBuilder(template=prompt_template)
    results = builder.run(
        query=question, documents=doc_results["retriever"]["documents"])

    return results, doc_results