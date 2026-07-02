

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate 

llm = OllamaLLM(model ='qwen2.5:7b')

template = """
        Bạn là chuyên gia quan sát bệnh trên cây mai vàng. Bạn có khả năng đối chiếu rất tốt từ kiến thức 
        đã học bạn nhận được câu hỏi mô tả bệnh là bạn dễ dàng đoán được bệnh ngay.
        
        Hãy trả lời bằng cách:
        - tóm tắt ý chính
        - giải thích dễ hiểu
        - không chép nguyên văn
        
        Chỉ sử dụng context.

        CONTEXT:
        {context}
        CÂU HỎI:
        {question}


Trả lời:
"""
prompt = ChatPromptTemplate.from_template(template)  
#tạo 1 prompt mà LangChain được được, nó hiểu chỉ cần truyền vào 2 biến context và question
#lúc này kq là 1 obj với 2 khóa có gtri đang rỗng là context và question (ta sẽ truyền ở hàm ask_llm)
chain= prompt | llm # dấu | có ý nghĩa là nối các bước xử lý thành 1 pipeline

def ask_llm(question, context):
    

    res = chain.invoke( {
        "context": context,
        "question": question,
    }
    )
    return res