import requests
from faiss_search import search_similar_documents

def call_gemini_api(question, api_key):
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": question}]}]
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        try:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        except KeyError:
            return "Không tìm thấy câu trả lời hợp lệ."
    else:
        return f"Lỗi {response.status_code}: {response.text}"

def generate_query_with_gemini(query, api_key, model, index, documents):
    similar_documents = search_similar_documents(query, model, index, documents, top_k=2)
    combined_context = "\n".join([f"Document {i+1}: {doc}" for i, doc in enumerate(similar_documents)])
    combined_question = (
        f"Với các thông tin sau đây:\n{combined_context}\n"
        f"Dựa vào đơn thuốc được chỉ định của các bệnh nhân trên hãy trả lời \nCâu hỏi: {query}\n và phân tích tại sao bạn lại lựa chọn đơn thuốc này"
    )
    return call_gemini_api(combined_question, api_key)
