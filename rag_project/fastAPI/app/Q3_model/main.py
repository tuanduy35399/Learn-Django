from fastapi import FastAPI
from llms import ask_llm
import uuid
from rag import retriever

app = FastAPI()

#luu log danh gia model
RAG_LOGS = []

@app.get("/ask")
def ask(q: str):

    trace_id = str(uuid.uuid4())
    #buoc retrieval
    docs = retriever.invoke(q)
    context = "\n".join(
        d.page_content
        for d in docs
    )

    
    # if not context:
    #     return {
    #         "question": q,
    #         "answer": "Không tìm thấy dữ liệu liên quan"
    #     }
    #buoc sinh data
    answer = ask_llm(
        question=q,
        context=context
    )

    #ghi log lai de danh gia
    RAG_LOGS.append({
            "id": trace_id,
            "question": q,
            "contexts": context,
            "answer": answer
        })
    
    return {
        "question": q,
        "context": context,
        "answer": answer
    }
    
# from ragas import evaluate
# from ragas.metrics import faithfulness, answer_relevancy, context_precision
# from datasets import Dataset

# @app.get("/evaluate")
# def evaluate_rag():

#     dataset = Dataset.from_list([
#         {
#             "question": x["question"],
#             "contexts": x["contexts"],
#             "answer": x["answer"]
#         }
#         for x in RAG_LOGS
#     ])

#     result = evaluate(
#         dataset,
#         metrics=[
#             faithfulness,
#             answer_relevancy,
#             context_precision
#         ]
#     )

#     return result