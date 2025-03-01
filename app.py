import gradio as gr
import time
from gemini_api import generate_query_with_gemini
from faiss_search import initialize_faiss, search_similar_documents
from data_loader import load_data_from_folder

folder_path = 'Data'
api_key = 'AIzaSyD3Hu747dbztC-jogggDfZudh_zYg40PJg'

model, index, documents = initialize_faiss(folder_path)

def generate_response_stream(chat_history, user_input):
    try:
        sql_query = generate_query_with_gemini(user_input, api_key, model, index, documents)
        chat_history.append((user_input, sql_query))
        yield gr.update(value=chat_history)
    except Exception as e:
        chat_history.append(("Error", f"Error: {str(e)}"))
        yield gr.update(value=chat_history)

def clear_textbox():
    return ""

with gr.Blocks() as iface:
    gr.Markdown("<h1 id='title'>Hệ Thống Hỏi Đáp Y Tế VSS AI</h1>")
    chatbot = gr.Chatbot(label="Trò chuyện", show_copy_button=True)
    user_input = gr.Textbox(label="Nhập câu hỏi của bạn")
    submit_button = gr.Button("Gửi câu hỏi")

    # user_input.submit(generate_response_stream, [chatbot, user_input], [chatbot])
    # submit_button.click(generate_response_stream, [chatbot, user_input], [chatbot])

    user_input.submit(generate_response_stream, [chatbot, user_input], [chatbot]).then(clear_textbox, None, user_input)
    submit_button.click(generate_response_stream, [chatbot, user_input], [chatbot]).then(clear_textbox, None, user_input)

iface.launch(share=True)
