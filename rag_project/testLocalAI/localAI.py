from langchain_ollama.llms import OllamaLLM # Cho phep su dung truc tiep mo hinh cua Ollama
from langchain_core.prompts import ChatPromptTemplate #nhap template mau vao 

model = OllamaLLM(model = 'llama3.2') #nhap vao model ma minh vua tai ve

template  =  """ 
Bạn là 1 chuyên gia về cây mai vàng ở Việt Nam, bạn có nhiều năm kinh nghiệm quan sát các
triệu chứng bệnh trên lá và chẩn đoán ra bệnh 1 cách chính xác
Đây là 1 số nội dung tham khảo : {reviews}
Đây là câu hỏi để trả lời: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
result = chain.invoke({"reviews": [], "question": "Những bệnh này biểu hiện bằng lá chuyển sang màu nâu với viền vàng, và tình trạng thường xấu đi dần từ mép lá hoặc đầu lá vào bên trong."})
print(result)