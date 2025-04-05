# Multi-Agent Pathfinding Using CBS & ICTS

## Giới thiệu
Dự án này triển khai các thuật toán **Conflict-Based Search (CBS)** và **Increasing Cost Tree Search (ICTS)** để tìm đường đi tối ưu cho nhiều tác nhân trên bản đồ lưới ô vuông. Chương trình hỗ trợ trực quan hóa kết quả bằng giao diện `Tkinter`.
Ngôn ngữ: Python.
Thuật toán sử dụng: CBS, ICTS, A*, ...
Phương pháp: Hướng đối tượng (OOP).

## Cấu trúc thư mục
your-repo/
│──[test]             # Các thư mục chứa file input.
│── CBS.py            # Cài đặt thuật toán CBS.
│── ICTS.py           # Cài đặt thuật toán ICTS.
│── LowLevel.py       # Bộ giải A* cấp thấp.
│── CBSData.py        # Định nghĩa lớp dữ liệu (Vertex, Path, Agent, Constraint).
│── visualizer.py     # Hiển thị và trực quan hóa đường đi.
│── mapf.py           # Đưa ra giải pháp để giải quyết nốt các xung đột có thế xảy ra sau khi sử dụng CBS hoặc ICTS (đang phát triển).
│── main.py           # Chương trình chính để chạy CBS hoặc ICTS.
│── README.md         # Tài liệu hướng dẫn sử dụng.

## Cách chạy chương trình
### Yêu cầu:
- Python 3.x
- Các thư viện cần thiết (`tkinter` đã có sẵn trong Python).

### Hướng dẫn chạy:
1. **Clone dự án:**
  ```bash
  git clone https://github.com/Hoangday2k4/Conflict-based-search-for-multi-agent-pathfinding.git

2. **Công cụ:**
- VS Code
- PyCharm
- Terminal
- ...

3. **Chạy chương trình:**
- python main.py hoặc python3 main.py
- Bạn có thể chạy chương trình qua phần mềm hỗ trợ.

### Chú ý:
_Trong khi chạy, nếu thay đổi file input thì có thể dẫn tới chút lỗi nhỏ, cần chọn lại thuật toán để khắc phục.
Code vẫn đang trong quá trình debug nên vẫn còn nhiều thiếu sót._
