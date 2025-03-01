import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
from data_loader import load_data_from_folder
import torch

def initialize_faiss(folder_path):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2', device= device)

    documents = load_data_from_folder(folder_path)
    embeddings = normalize(model.encode(documents), axis=1)
    dimension = embeddings.shape[1]
    
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings, dtype=np.float32))
    
    return model, index, documents

def search_similar_documents(query, model, index, documents, top_k=20):
    query_embedding = normalize(model.encode([query]), axis=1)
    _, indices = index.search(np.array(query_embedding, dtype=np.float32), top_k)
    
    return [documents[idx] for idx in indices[0]]


# def initialize_faiss(folder_path):
#     # Xác định thiết bị (GPU hoặc CPU)
#     device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
#     # Tải mô hình SentenceTransformer
#     model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2', device=device)

#     # Tải tài liệu từ thư mục
#     documents = load_data_from_folder(folder_path)
    
#     # Tạo embeddings cho các tài liệu và chuẩn hóa
#     embeddings = normalize(model.encode(documents), axis=1)
#     dimension = embeddings.shape[1]

#     # Tạo IndexHNSW
#     M = 32  # Số kết nối tối đa
#     index = faiss.IndexHNSWFlat(dimension, M)
    
#     # Thêm embeddings vào index
#     index.add(np.array(embeddings, dtype=np.float32))

#     # Thiết lập các tham số efSearch và efConstruction
#     index.hnsw.efConstruction = 40  # Tham số xây dựng đồ thị
#     index.hnsw.efSearch = 50  # Tham số tìm kiếm

#     return model, index, documents

# def search_similar_documents(query, model, index, documents, top_k=5):
#     # Tạo embedding cho truy vấn và chuẩn hóa
#     query_embedding = normalize(model.encode([query]), axis=1)
    
#     # Tìm kiếm k láng giềng gần nhất
#     _, indices = index.search(np.array(query_embedding, dtype=np.float32), top_k)
    
#     # Trả về các tài liệu tương tự
#     return [documents[idx] for idx in indices[0]]