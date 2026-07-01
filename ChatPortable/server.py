from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import sys

# Danh sách lưu tin nhắn tạm thời trong bộ nhớ
messages = []

class ChatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # Trang chủ: Gửi file index.html cho trình duyệt
        if parsed.path == '/':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open('index.html', 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, "Khong tim thay file index.html!")

        # API lấy tin nhắn
        elif parsed.path == '/get':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("\n".join(messages).encode('utf-8'))

        # API gửi tin nhắn
        elif parsed.path == '/send':
            query = urllib.parse.parse_qs(parsed.query)
            if 'm' in query:
                messages.append(query['m'][0])
            self.send_response(200)
            self.end_headers()

if __name__ == '__main__':
    # Mặc định dùng cổng 9999 để tránh đụng hàng Postgres
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
    print(f"--- Server dang khoi dong tai cong {port} ---")
    print(f"Bam Ctrl+C de dung server.")
    try:
        HTTPServer(('0.0.0.0', port), ChatHandler).serve_forever()
    except Exception as e:
        print(f"Loi: {e}")