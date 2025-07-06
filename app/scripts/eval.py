from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
from scripts.llm import llama_models
from scripts.retrieval import retrieval_model

def read_file_lines(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]
    

async def generate_answer():
    model = llama_models()
    model.generator_model_chooser()
    questions = read_file_lines("data/questions.txt")
    with open("data/llm_answers.txt", 'w', encoding='utf-8') as out_f:
        for q in tqdm(questions):
            

            results, docs = await retrieval_model(q)
    


            answer = model.prompt(results["prompt"])
            out_f.write(answer.replace("\n", " ") + "\n")  # write each answer in one line

    print(f"Answers saved to data/llm_answers.txt")
    
async def eval_rag():
    await generate_answer()

    file1_lines = read_file_lines('data/answers.txt')
    file2_lines = read_file_lines('data/llm_answers.txt')

    print(f"Comparing {len(file1_lines)} lines from answers.txt with {len(file2_lines)} lines from llm_answers.txt")
    
    model = SentenceTransformer("snowflake/snowflake-arctic-embed-s")

    # Encode all lines into embeddings (to speed up multiple comparisons)
    embeddings1 = model.encode(file1_lines, convert_to_tensor=True)
    embeddings2 = model.encode(file2_lines, convert_to_tensor=True)

    # Compare each line from file1 with each line from file2 using cosine similarity
    similarity_results = []
    for i, emb1 in enumerate(embeddings1):
        
        similarity = util.cos_sim(emb1, embeddings2[i]).item()
        print(f"Similarity between file1 and file2 in the line {i} : {similarity:.4f}")
        similarity_results.append(f"Line {i}: {similarity:.4f}")
    return similarity_results
