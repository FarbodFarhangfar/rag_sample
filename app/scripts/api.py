from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

from scripts.llm import llama_models
from scripts.retrieval import retrieval_model
from scripts.prepare_data import index_writer

from scripts.eval import eval_rag


from pdfminer.high_level import extract_text

import io


rag_router = APIRouter()


class QueryScheme(BaseModel):
    question: str

@rag_router.post("/query")
async def process_rag_query(query: QueryScheme):
    prompt = query.question

    model = llama_models()
    model.generator_model_chooser()

    results, docs = await retrieval_model(prompt)
    


    response = model.prompt(results["prompt"])
    




    return response


    

@rag_router.post("/uploadpdf")
async def upload_pdf( file: UploadFile = File(...)):

    filename = file.filename


    contents = await file.read()
    pdf_file = io.BytesIO(contents)
    text = extract_text(pdf_file)
    
    pdf_file.close()

    user_id = '1'


    doc = await index_writer(text, user_id, filename)



    return doc

@rag_router.get("/eval")
async def eval_rag_api():
    response = await eval_rag()
    return {"message": "Evaluation completed successfully.", "results": response}