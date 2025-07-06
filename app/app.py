from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


from scripts.api import rag_router
from scripts.prepare_data import index_writer
import io
from pdfminer.high_level import extract_text



@asynccontextmanager
async def lifespan(app: FastAPI):



    text = extract_text("data/dr_voss_diary.pdf")
    filename = "dr_voss_diary.pdf"
    


    user_id = '1'


    doc = await index_writer(text, user_id, filename)
    print("Document indexed complated")
    yield
app = FastAPI(lifespan=lifespan)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


app.include_router(rag_router, prefix="", tags=["rag"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
