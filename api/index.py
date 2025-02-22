import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

# Cấu hình logging để hiển thị thông tin lỗi và thông báo trong quá trình chạy server
logging.basicConfig(level=logging.INFO)

# Load biến môi trường để tránh hardcode thông tin nhạy cảm trong code
SUPABASE_URL = os.getenv("SUPABASE_URL")  # URL của Supabase
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # API Key của Supabase

# Khởi tạo Supabase client để kết nối với database
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Khởi tạo ứng dụng Flask
app = Flask(__name__)
CORS(app)  # Cho phép tất cả các nguồn (origin) gửi request đến API

# Nếu muốn giới hạn chỉ cho phép một số nguồn truy cập API, có thể dùng:
# CORS(app, origins=["http://localhost:3000"])

# -------------------------
# 1. API tạo người dùng (CREATE)
# -------------------------
@app.route('/users', methods=['POST'])
def create_user():
    try:
        # Lấy dữ liệu từ request (JSON gửi từ client)
        data = request.get_json()
        # Kiểm tra xem dữ liệu có đầy đủ các trường 'name', 'email', 'age' không
        if not data or not all(k in data for k in ['name', 'email', 'age']):
            return jsonify({"error": "Missing required fields"}), 400  # Trả về lỗi nếu thiếu dữ liệu
        # Thêm dữ liệu vào bảng 'users' trong Supabase
        response = supabase.table('users').insert(data).execute()
        
        # Trả về dữ liệu vừa tạo cùng với mã trạng thái HTTP 201 (Created)
        return jsonify(response.data), 201
    except Exception as e:
        logging.error(f"Error creating user: {e}")  # Ghi log lỗi nếu có
        return jsonify({"error": "Internal server error"}), 500  # Trả về lỗi server

# -------------------------
# 2. API lấy danh sách người dùng (READ)
# -------------------------
@app.route('/users', methods=['GET'])
def get_users():
    try:
        # Lấy toàn bộ dữ liệu từ bảng 'users' trong Supabase
        response = supabase.table('users').select('*').execute()
        
        # Trả về danh sách người dùng cùng với mã trạng thái HTTP 200 (OK)
        return jsonify(response.data), 200
    except Exception as e:
        logging.error(f"Error fetching users: {e}")  # Ghi log lỗi nếu có
        return jsonify({"error": "Internal server error"}), 500  # Trả về lỗi server





# -------------------------
# 2.1. API lấy danh sách người dùng theo id(READ)
# -------------------------
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        # Lấy dữ liệu của người dùng có ID cụ thể từ bảng 'users'
        response = supabase.table('users').select('*').eq('id', user_id).execute()
     # Trả về danh sách người dùng cùng với mã trạng thái HTTP 200 (OK)
        return jsonify(response.data), 200
    except Exception as e:
        logging.error(f"Error fetching users: {e}")  # Ghi log lỗi nếu có
        return jsonify({"error": "Internal server error"}), 500  # Trả về lỗi server





# -------------------------
# 3. API cập nhật thông tin người dùng (UPDATE)
# -------------------------
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        # Lấy dữ liệu cập nhật từ request
        data = request.get_json()
        
        # Kiểm tra nếu dữ liệu cập nhật bị trống
        if not data:
            return jsonify({"error": "No update data provided"}), 400

        # Cập nhật thông tin của người dùng có id tương ứng
        response = supabase.table('users').update(data).eq('id', id).execute()
        
        # Nếu không tìm thấy người dùng, trả về lỗi 404
        if not response.data:
            return jsonify({"error": "User not found"}), 404

        # Trả về thông tin người dùng sau khi cập nhật
        return jsonify(response.data), 200
    except Exception as e:
        logging.error(f"Error updating user {id}: {e}")  # Ghi log lỗi nếu có
        return jsonify({"error": "Internal server error"}), 500  # Trả về lỗi server

# -------------------------
# 4. API xóa người dùng (DELETE)
# -------------------------
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        # Xóa người dùng có id tương ứng
        response = supabase.table('users').delete().eq('id', id).execute()
        
        # Nếu không tìm thấy người dùng, trả về lỗi 404
        if not response.data:
            return jsonify({"error": "User not found"}), 404

        # Trả về thông báo xóa thành công
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting user {id}: {e}")  # Ghi log lỗi nếu có
        return jsonify({"error": "Internal server error"}), 500  # Trả về lỗi server

## Chạy ứng dụng Flask trên cổng 5001
#if __name__ == "__main__":
#    app.run(debug=True, port=5001)














@app.route('/')
def home():
    return 'Hello, World! VY'

@app.route('/about')
def about():
    return 'About'
