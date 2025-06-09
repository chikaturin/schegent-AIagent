from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from config.llm import llm


def query_rag(
    question="Lịch trình hàng ngày phù hợp với sở thích và mức độ ưu tiên của tôi",
    db_path="./faiss_index",
):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/LaBSE")

    vectorstore = FAISS.load_local(
        db_path, embedding_model, allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_type="similarity", k=4)

    relevant_docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt = PromptTemplate.from_template(
        """
            Hãy chơi tôi trả lời câu hỏi của bạn dựa trên các đoạn văn sau đây. Bạn sẽ nhận được câu trả lời ngắn gọn và súc tích, tập trung vào thông tin quan trọng nhất.
            Nếu không có thông tin nào liên quan, hãy trả lời "Không có thông tin liên quan".
            Dựa vào các đoạn văn sau đây, hãy trả lời câu hỏi:\n\n{context}\n\nCâu hỏi: {question}\nTrả lời:
        """
    )

    chain = prompt | llm
    answer = chain.invoke({"context": context, "question": question})

    return answer.content if hasattr(answer, "content") else answer
