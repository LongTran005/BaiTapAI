- Báo cáo đồ án cá nhân Trí tuệ nhân tạo và các bài tập hàng tuần
- Đề tài: Áp dụng các thuật toán tìm kiếm đã học vào bài toán đặt 8 con hậu lên bàn cờ mà không ăn được lẫn nhau
- Giảng viên hướng dẫn: Phan Thị Huyền Trang
- Sinh viên thực hiện: Trần Cẩm Long - MSSV: 23110122

1. Mục tiêu của đề tài:
- Sử dụng các thuật toán tìm kiếm để tìm ra trạng thái các quân hậu không ăn lẫn nhau với trạng thái đích cho trước
- Thể hiện trực quan lên giao diện và bảng trace quá trình để người dùng hiểu được cách thức hoạt động
2. Nội dung thực hiện:
  
  2.1. Mô tả bài toán
  
    - Trạng thái ban đầu (Initial State): Bàn cờ 8x8 rỗng, gồm 64 ô được đánh số theo hàng và cột.
    - Trạng thái mục tiêu (Goal State): 8 quân hậu được đặt trên bàn sao cho không quân nào đứng cùng hàng hoặc cùng cột – đảm bảo điều kiện “không ăn nhau”.
    - Tập hành động (Actions): Lần lượt đặt từng quân hậu lên bàn theo quy tắc xác định vị trí hợp lệ.
    - Không gian trạng thái (State Space): Tất cả các trạng thái có thể sinh ra trong quá trình đặt quân.
    - Lời giải (Solution): Một ma trận 8x8 biểu diễn vị trí của 8 quân hậu thỏa mãn điều kiện bài toán.

   2.2. Nhóm thuật toán tìm kiếm không có thông tin (Uninformed Search): Nhóm này bao gồm các thuật toán không sử dụng thông tin bổ sung về trạng thái đích mà chỉ dựa trên cấu trúc tìm kiếm.
  
      2.2.1. Breadth-First Search (BFS):
  ![BFS](https://github.com/user-attachments/assets/5d3a2117-b9d7-45b0-af6f-a74b0554ad99)
  
      - Dựa trên hàng đợi (Queue), BFS mở rộng tất cả các nút ở cùng một mức trước khi sang mức kế tiếp.
      - Ưu điểm: Đảm bảo tìm được lời giải nếu có, và lời giải là ngắn nhất.
      - Nhược điểm: Tiêu tốn bộ nhớ lớn do phải lưu tất cả các nút trong cùng một tầng.

      2.2.2. Depth-First Search (DFS):
  ![DFS](https://github.com/user-attachments/assets/3a41b06b-e134-4ff9-bb30-d8e8bd8104e8)
  
      - Sử dụng ngăn xếp (Stack) để lưu trữ các trạng thái, thuật toán sẽ mở rộng nhánh sâu nhất trước khi quay lại.
      - Ưu điểm: Tiết kiệm bộ nhớ, có thể tìm lời giải nhanh nếu đích ở độ sâu nhỏ.
      - Nhược điểm: Dễ rơi vào vòng lặp vô hạn.
  
      2.2.3. Uniform Cost Search (UCS):
  ![UCS](https://github.com/user-attachments/assets/fd5f1cdb-e0aa-40c8-a764-48df51efebbe)
  
      - Sử dụng hàng đợi ưu tiên (Priority Queue) để chọn nút có chi phí thấp nhất để mở rộng.
      - Ưu điểm: Đảm bảo tìm được đường đi có tổng chi phí nhỏ nhất.
      - Nhược điểm: Thời gian và bộ nhớ tiêu tốn lớn nếu có nhiều trạng thái có chi phí tương đương.
  
      2.2.4. Depth Limit Search (DLS)
  ![DLS](https://github.com/user-attachments/assets/0d3cb54c-dfeb-4481-a3d0-f544f39302e2)
  
      - Sử dụng thuật toán DFS để tìm kiếm nhưng có giới hạn độ sâu
      - Ưu điểm: Tránh được vòng lặp vô hạn của DFS, giảm bớt không gian tìm kiếm.
      - Nhược điểm: Không hoàn chỉnh nếu giới hạn nhỏ hơn độ sâu lời giải.
  
      2.2.5. Iterative Deepening Search (IDS)
  ![IDS](https://github.com/user-attachments/assets/809f69c0-b0f8-4f88-a7a2-a85da6f6545b)
  
      - Kết hợp ưu điểm của DFS và BFS, thuật toán lặp lại quá trình DLS với giới hạn độ sâu tăng dần (limit = 0, 1, 2, …).
      - Ưu điểm: Tiết kiệm bộ nhớ như DFS nhưng đảm bảo tìm thấy lời giải.
      - Nhược điểm: Tốn thời gian do phải lặp lại nhiều cấp độ.
  
    2.3. Nhóm thuật toán tìm kiếm có thông tin: Các thuật toán này sử dụng hàm heuristic để ước lượng khoảng cách hoặc chi phí từ trạng thái hiện tại đến trạng thái đích.
      2.3.1. Greedy Search
  ![Greedy](https://github.com/user-attachments/assets/c6ce948c-4db5-4d5d-b5a0-0149445b4b9a)
  
      - Lựa chọn mở rộng trạng thái có giá trị heuristic tốt nhất.
      - Ưu điểm: tìm được lời giải nhanh chóng
      - Nhược điểm: hiệu suất thuật toán phụ thuộc nhiều vào các hàm tính toán chi phí
  
      2.3.2. A* Search
  ![Astar](https://github.com/user-attachments/assets/6c1a7cb0-5c4e-4f30-8b15-b31dcedd7cee)
  
      - Kết hợp chi phí thực tế g(n) và ước lượng h(n) theo công thức: f(n) = g(n) + h(n).
      - Ưu điểm: Đảm bảo tính tối ưu và đầy đủ nếu h(n) là heuristic chấp nhận được.
      - Nhược điểm: Tốn bộ nhớ và khó xác định hàm heuristic phù hợp.

    2.4. Nhóm thuật toán tìm kiếm cục bộ (Local Search)
      2.4.1. Hill Climbing
  ![HillClimbing](https://github.com/user-attachments/assets/d790f1e9-9e43-4369-9d01-b4b316a8ab85)
  
      - Chọn trạng thái lân cận tốt nhất để tiến tới.
      - Ưu điểm: Đơn giản, sử dụng ít bộ nhớ.
      - Nhược điểm: Dễ dừng ở cực trị địa phương.
  
      2.4.2. Simulated Annealing
  ![SA](https://github.com/user-attachments/assets/82ea590e-0758-44dc-98f1-7d3d20930b7e)
  
      - Lấy cảm hứng từ quá trình nung chảy kim loại và làm nguội dần, cho phép di chuyển đến trạng thái xấu hơn với xác suất giảm dần theo
      - Ưu điểm: Có thể thoát khỏi cực trị địa phương.
      - Nhược điểm: Cần chọn hàm xác suất và tốc độ giảm nhiệt độ hợp lý.
  
      2.4.3. Genetic Algorithms
  ![GA](https://github.com/user-attachments/assets/6383e5d2-aefa-4ec2-9035-f14121ee5b5b)
  
      - Dựa trên các cơ chế chọn lọc – lai ghép – đột biến để tạo ra thế hệ trạng thái mới.
      - Ưu điểm: Tìm kiếm hiệu quả trong không gian lớn.
      - Nhược điểm: Thiết kế hàm thích nghi và các toán tử lai ghép phức tạp
  
      2.4.4. Beam Search
  ![Beam](https://github.com/user-attachments/assets/3894ad01-7341-405c-a257-b96f109c3a44)
  
      - Giữ lại K trạng thái tốt nhất ở mỗi mức thay vì toàn bộ như BFS.
      - Ưu điểm: Giảm đáng kể bộ nhớ cần dùng.
      - Nhược điểm: Có thể bỏ qua lời giải tối ưu.

    2.5. Nhóm thuật toán tìm kiếm trong môi trường phức tạp (Complex Search): Nhóm này xử lý các bài toán trong môi trường không chắc chắn hoặc quan sát một phần.
      2.5.1. And-Or Search
  ![AndOr](https://github.com/user-attachments/assets/e9c39ac7-c67f-400f-8ff5-d12a0bc9b979)
  
      - Phân biệt giữa nút lựa chọn (OR) và nút bắt buộc (AND) trong quá trình tìm kiếm.
      - Ưu điểm: Mô phỏng tốt các bài toán có điều kiện phức tạp.
      - Nhược điểm: Không thích hợp với không gian tìm kiếm lớn.
  
      2.5.2. Belief State Search
  ![SSless](https://github.com/user-attachments/assets/218c8580-b8ab-4f6a-8289-ca9d3d64a748)
  
      - Áp dụng khi không quan sát được trạng thái thật, chỉ biết tập hợp các khả năng có thể xảy ra.
      - Ưu điểm: Giải quyết được bài toán trong môi trường không chắc chắn.
      - Nhược điểm: Dễ bị rơi vào trạng thái suy luận sai hoặc cực trị địa phương.
  
      2.5.3. Partial Observation Search
  ![PartialOb](https://github.com/user-attachments/assets/fad24e30-b2b2-4c9c-a1e6-0f6c8b14011e)
  
      - Tìm kiếm dựa trên thông tin quan sát được một phần.
      - Ưu điểm: Kết hợp giữa tìm kiếm và suy luận.
      - Nhược điểm: Khó xác định trạng thái chính xác, dễ lặp hoặc sai hướng.

    2.6. Nhóm thuật toán tìm kiếm dựa trên ràng buộc (CSP): Những thuật toán này tìm kiếm lời giải thỏa mãn các ràng buộc nhất định, chẳng hạn trong bài toán 8 quân xe là điều kiện không hai xe nào cùng hàng hoặc cùng cột
      2.6.1. Backtracking
  
  ![BackTr](https://github.com/user-attachments/assets/d616f9ac-a705-4b50-9cb7-7b461cf99e6d)
  
      - Thực hiện tìm kiếm theo chiều sâu, quay lui khi gặp mâu thuẫn.
      - Ưu điểm: Dễ hiểu, dễ triển khai, tiết kiệm bộ nhớ.
      - Nhược điểm: Tốc độ chậm, không tận dụng được thông tin ràng buộc sớm.

      2.6.2. Forward Checking
  ![Forward](https://github.com/user-attachments/assets/db80c0fe-4d20-4d21-a971-c2e7930baa73)
  
      - Sau mỗi lần gán giá trị, loại bỏ trước các giá trị không hợp lệ cho các biến còn lại.
      - Ưu điểm: Phát hiện xung đột sớm, giảm số lần quay lui.
      - Nhược điểm: Tốn bộ nhớ hơn Backtracking
  
  
  
      
      
      
