# DoAnNganh
Sau khi tải project về và mở lên trước tiên phải tạo môi trường ảo venv
Bước 1: Vào file > Settings > Python Interpreter
Bước 2: Tại Python Interpreter ấn vào biểu tượng cài đặt (hình bánh răng) > Add 
Bước 3: Chọn New environment > OK
Cài đặt xong môi trường ảo tiếp theo sẽ cài requirements.txt
Bước 1: Vào terminal
Bước 2: Gõ lệnh pip install -r requirements.txt và chờ cài đặt
Sau khi cài đặt hoàn tất cuối cùng sẽ là chạy MySQL để kết nối dữ liệu
Bước 1: Mở MySQL và tiến hành đăng nhập (nếu chưa có tài khoản có thể đăng ký tài khoản mới)
Bước 2: Tạo new schema đặt tên là "ThongTinTour" chọn charset là utf8mb4 > Apply
Bước 3: Vào file _init_.py sửa mục quote ban đầu là Admin@123 thành mật khẩu MySQL vừa tạo (Nếu mật khẩu MySQL là Admin@123 luôn thì không cần sửa)
Bước 3: Vào file models.py bấm run models 
Sau khi hoàn thành các bước trên là hoàn thành các bước chuẩn bị tiến hành run index và bấm vào link để xem trang web
