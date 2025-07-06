from haystack import Pipeline, Document

from milvus_haystack import MilvusDocumentStore
from milvus_haystack.milvus_embedding_retriever import MilvusEmbeddingRetriever


from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter

from pymilvus import connections, list_collections
from scripts.retrieval import retrieval_model
import json
import re


def get_paragraphs(text):
    """paragraph splitting"""
    text = re.sub('\n\n\x0c', '', text)
    return re.split('\n{2,}', text)


async def index_writer(text, user_id, document_name):

    text_list = get_paragraphs(text)
     
    document = []
    for chunks in text_list:
        document.append(Document(content=chunks,
                                 ))

    document_store = MilvusDocumentStore(
    connection_args={"uri": "tcp://standalone:19530"},
    drop_old=True,)


    spliter = DocumentSplitter(
        split_by="passage", split_length=200, split_overlap=0)
    document = spliter.run(document)

    embedder = SentenceTransformersDocumentEmbedder(
        model="Snowflake/snowflake-arctic-embed-s")
    embedder.warm_up()
    document = embedder.run(document['documents'])

    doc_id = document["documents"][0].meta["source_id"]


    document_store.write_documents(
        document['documents'])
    print("document_count", document_store.count_documents())




    return doc_id
