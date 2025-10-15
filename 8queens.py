import tkinter as tk
import random
import math
from collections import deque
import heapq

class NQueensGUI:
    def __init__(self, root, n=8):
        self.root = root
        self.n = n
        self.size = 60
        self.delay = 30
        self.goal = self.random_goal_state()
        self.job = None
        self.running = False  # flag chung
        self.paused = False
        self.root.title("8 Queens")
        self.canvas1 = tk.Canvas(root, width=n*self.size, height=n*self.size)
        self.canvas1.pack(side="left", padx=5, pady=5)
        self.canvas2 = tk.Canvas(root, width=n*self.size, height=n*self.size)
        self.canvas2.pack(side="right", padx=5, pady=5)

        # tạo 3 dòng nút
        frame_top = tk.Frame(root)
        frame_top.pack(side="bottom", pady=2)

        frame_bottom = tk.Frame(root)
        frame_bottom.pack(side="bottom", pady=2)

        frame_middle = tk.Frame(root)
        frame_middle.pack(side="bottom", pady=5)

        # ====== Dòng trên ======
        tk.Button(frame_bottom, text="Greedy", command=self.run_greedy).pack(side="left", padx=5)
        tk.Button(frame_bottom, text="A*", command=self.run_astar).pack(side="left", padx=5)
        tk.Button(frame_bottom, text="Hill Climbing", command=self.run_hill_climbing).pack(side="left", padx=5)
        tk.Button(frame_bottom, text="SA", command=self.run_simulated_annealing).pack(side="left", padx=5)
        tk.Button(frame_bottom, text="GA", command=self.run_genetic).pack(side="left", padx=5)
        tk.Button(frame_bottom, text="Beam", command=self.beam_search).pack(side="left", padx=5)

        # ====== Dòng dưới  ======
        self.dls_limit_var = tk.IntVar(value=self.n)
        tk.Button(frame_top, text="Random Goal", command=self.new_goal).pack(side="left", padx=5)
        tk.Button(frame_top, text="BFS", command=self.run_bfs).pack(side="left", padx=5)
        tk.Button(frame_top, text="DFS", command=self.run_dfs).pack(side="left", padx=5)
        tk.Button(frame_top, text="UCS", command=self.run_ucs).pack(side="left", padx=5)
        tk.Button(frame_top, text="IDS", command=self.run_ids).pack(side="left", padx=5)
        tk.Button(frame_top, text="DLS", command=self.run_dls).pack(side="left", padx=5)
        tk.Label(frame_top, text="DLS limit:").pack(side="left", padx=(12, 2))
        tk.Entry(frame_top, width=3, textvariable=self.dls_limit_var).pack(side="left", padx=(0, 8))
        tk.Button(frame_top, text="Stop", command=self.stop).pack(side="left", padx=5)
        tk.Button(frame_top, text="Continue", command=self.continue_run).pack(side="left", padx=5)

        # ====== Dòng giữa ======
        tk.Button(frame_middle, text="AND-OR", command=self.run_and_or_search).pack(side="left", padx=5)
        tk.Button(frame_middle, text="Belief(SSless)", command=self.run_belief_search).pack(side="left", padx=5)
        tk.Button(frame_middle, text="PartialOb", command=self.run_partial_search).pack(side="left", padx=5)
        tk.Button(frame_middle, text="BackTr", command=self.run_backtracking).pack(side="left", padx=5)
        tk.Button(frame_middle, text="Forward", command=self.run_forwardchecking).pack(side="left", padx=5)

        self.status = tk.Label(root, text="Ready", relief="sunken", anchor="w")
        self.status.pack(side="bottom", fill="x")

        # Khung textbox để hiển thị bảng sensorless
        self.text = tk.Text(root, height=20, width=100, font=("Consolas", 11))
        self.text.pack(pady=5)

        self.draw_board(self.canvas1)
        self.draw_board(self.canvas2)
        self.show(self.canvas2, self.goal, "purple")

    # ======= Vẽ bàn cờ =========
    def draw_board(self, cv):
        cv.delete("all")
        for r in range(self.n):
            for c in range(self.n):
                x0, y0 = c*self.size, r*self.size
                x1, y1 = x0+self.size, y0+self.size
                color = "#eeeed2" if (r+c)%2==0 else "#769656"
                cv.create_rectangle(x0,y0,x1,y1,fill=color,outline=color)

    def show(self, cv, state, color="red"):
        cv.delete("all")
        # vẽ ô nền lại (giữ cùng kiểu màu)
        for r in range(self.n):
            for c in range(self.n):
                x0, y0 = c*self.size, r*self.size
                x1, y1 = x0+self.size, y0+self.size
                color_bg = "#eeeed2" if (r+c)%2==0 else "#769656"
                cv.create_rectangle(x0,y0,x1,y1,fill=color_bg,outline=color_bg)
        # vẽ hậu của state (state có thể là tuple ngắn)
        for r, c in enumerate(state):
            x = c*self.size + self.size//2
            y = r*self.size + self.size//2
            cv.create_text(x,y,text="♛",font=("Segoe UI Symbol",int(self.size*0.6)),fill=color)

    def random_goal_state(self):
        sols = [
            (0,4,7,5,2,6,1,3),
            (0,5,7,2,6,3,1,4),
            (1,3,5,7,2,0,6,4),
            (2,4,6,0,3,1,7,5),
            (3,0,4,7,1,6,2,5),
        ]
        return random.choice(sols)

    def new_goal(self):
        self.stop()
        self.goal = self.random_goal_state()
        self.show(self.canvas2, self.goal, "purple")
        self.draw_board(self.canvas1)
        self.status.config(text="New goal!")

    def stop(self):
        self.running = False
        self.paused = True
        if self.job:
            self.root.after_cancel(self.job)
            self.job = None
            self.status.config(text="Đã tạm dừng, bấm Continue để chạy tiếp")

    def continue_run(self):
        if self.paused:
            self.paused = False
            self.running = True
            self.status.config(text="Tiếp tục chạy...")
            if hasattr(self, 'resume_func') and callable(self.resume_func):
                self.resume_func()
        else:
            self.status.config(text="Không thể tiếp tục (chưa có tiến trình bị tạm dừng).")

    # Hàm paused và continue_2 để sử dụng cho Stop và Continue cho BackTracking và Forward Checking
    def paused(self):
        if not self.running:
            self.status.config(text="Backtracking chưa chạy, không thể tạm dừng.")
            return
        self.paused = True
        if self.job:
            self.root.after_cancel(self.job)
            self.job = None
        self.status.config(text="Backtracking đã tạm dừng. Bấm Continue Backtracking để chạy tiếp.")

    def continue_2(self):
        if self.paused:
            self.paused = False
            # self.running đã là True, không cần đặt lại
            self.status.config(text="Tiếp tục chạy Backtracking...")
            # Gọi lại hàm step đã được lưu trong self.resume_func
            if hasattr(self, 'resume_func') and callable(self.resume_func):
                self.resume_func()
        else:
            self.status.config(text="Backtracking không bị tạm dừng nên không thể tiếp tục.")

    def print_solution(self, s):
        print("Nghiệm tìm được:", tuple(s))

    def attacked_count(self, state):
        board = [[0]*self.n for _ in range(self.n)]
        for r, c in enumerate(state):
            # hàng, cột
            for i in range(self.n):
                board[r][i] = 1
                board[i][c] = 1
            # chéo
            for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
                nr, nc = r+dr, c+dc
                while 0<=nr<self.n and 0<=nc<self.n:
                    board[nr][nc] = 1
                    nr += dr; nc += dc
            board[r][c] = 1
        return sum(sum(row) for row in board)

    def attacked_positions(self, state):
        attacked = set()
        for r, c in enumerate(state):
            # hàng và cột
            for i in range(self.n):
                attacked.add((r, i))
                attacked.add((i, c))
            # chéo
            for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
                nr, nc = r+dr, c+dc
                while 0 <= nr < self.n and 0 <= nc < self.n:
                    attacked.add((nr, nc))
                    nr += dr; nc += dc
            attacked.add((r,c))
        return attacked

    def is_safe(self, row, col, state):
        for r, c in enumerate(state):
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def is_goal(self, state):
        # Phải đặt đủ n hậu
        if len(state) != self.n:
            return False
        # Kiểm tra tất cả các cặp hậu xem có ăn nhau không
        for r1 in range(self.n):
            for r2 in range(r1 + 1, self.n):
                c1, c2 = state[r1], state[r2]
                # Cùng cột hoặc cùng đường chéo -> không phải goal
                if c1 == c2 or abs(c1 - c2) == abs(r1 - r2):
                    return False
        return True

    # Hàm heuristic: đếm số cặp hậu tấn công nhau (dùng cho Hill Climbing, SA, GA, Beam)
    def heuristic_conflicts(self, state):
        conflicts = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    # Hàm heuristic: số hậu còn thiếu để đạt 8 (dùng cho Greedy và A*)
    def heuristic_to_goal(self, state):
        return self.n - len(state)

    # ================= BFS ==================
    def run_bfs(self):
        self.stop()  # dừng bất kỳ animation trước đó
        q = deque([()])
        step_count = 0
        # Clear text và in header bảng
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"{'Bước':<6}{'Trạng thái':<30}{'Độ sâu':<10}{'Goal':<6}\n")
        self.text.insert(tk.END, "-" * 60 + "\n")
        # Vẽ lại board rỗng
        self.draw_board(self.canvas1)
        def step():
            nonlocal q, step_count
            if not q:
                self.status.config(text="BFS tìm kiếm thất bại")
                return
            s = q.popleft()
            step_count += 1
            # Ghi bảng vào textbox
            goal_flag = (len(s) == self.n and s == self.goal)
            self.text.insert(tk.END, f"{step_count:<6}{str(s):<30}{len(s):<10}{str(goal_flag):<6}\n")
            self.text.see(tk.END)
            # Hiển thị trạng thái trên board
            self.show(self.canvas1, s, "blue")
            # Kiểm tra goal
            if len(s) == self.n:
                if self.is_goal(s):
                    self.show(self.canvas1, s, "green")
                    self.status.config(text=f"BFS tìm thấy Goal ở bước {step_count}")
                    self.print_solution(s)
                    return
            # Mở rộng các con
            r = len(s)
            if r < self.n:
                for c in range(self.n):
                    if all(cc != c and abs(rr - r) != abs(cc - c) for rr, cc in enumerate(s)):
                        q.append(s + (c,))
            # tiếp tục sau delay
            self.resume_func = step  # lưu lại để Continue gọi tiếp
            self.job = self.root.after(self.delay, step)
        step()

    # ================= DFS ==================
    def run_dfs(self):
        self.stop()  # dừng bất kỳ animation trước đó
        st = [()]
        visited = set()
        step_count = 0
        # Clear text và in header bảng
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"{'Bước':<6}{'Trạng thái':<30}{'Độ sâu':<10}{'Goal':<6}\n")
        self.text.insert(tk.END, "-" * 60 + "\n")
        # Vẽ lại board rỗng
        self.draw_board(self.canvas1)
        def step():
            nonlocal st, step_count
            if not st:
                self.status.config(text="DFS tìm kiếm thất bại")
                return
            s = st.pop()
            # tránh hiển thị trùng lặp nhiều lần nếu muốn:
            if s in visited:
                self.job = self.root.after(self.delay, step)
                return
            visited.add(s)
            step_count += 1
            is_goal = (len(s) == self.n and s == self.goal)
            # Ghi bảng vào textbox
            self.text.insert(tk.END, f"{step_count:<6}{str(s):<30}{len(s):<10}{str(is_goal):<6}\n")
            self.text.see(tk.END)
            # Hiển thị trạng thái
            self.show(self.canvas1, s, "blue")
            if is_goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text=f"DFS tìm thấy Goal ở bước {step_count}")
                self.print_solution(s)
                return
            r = len(s)
            if r < self.n:
                # duyệt ngược để giữ đúng thứ tự DFS tương tự code gốc
                for c in reversed(range(self.n)):
                    if all(cc != c and abs(rr - r) != abs(cc - c) for rr, cc in enumerate(s)):
                        if (s + (c,)) not in visited:
                            st.append(s + (c,))
            # tiếp tục sau delay
            self.resume_func = step  # lưu lại để Continue gọi tiếp
            self.job = self.root.after(self.delay, step)
        step()

    # ================= DLS ==================
    def run_dls(self):
        self.stop()
        # Lấy limit từ ô DLS limit
        try:
            limit = int(self.dls_limit_var.get())
            if limit < 0:
                limit = 0
        except Exception:
            limit = self.n
        stack = [()]
        step_count = 0
        # Chuẩn bị bảng hiển thị
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"{'Bước':<6}{'Trạng thái':<30}{'Depth':<10}{'Goal':<10}\n")
        self.text.insert(tk.END, "-" * 70 + "\n")
        def step():
            nonlocal step_count
            if not stack:
                self.status.config(text=f"DLS thất bại (limit={limit})")
                return
            s = stack.pop()
            self.show(self.canvas1, s, "blue")
            step_count += 1
            depth = len(s)
            is_goal = (len(s) == self.n and all(self.is_safe(r, s[r], s[:r]) for r in range(self.n)))
            # Ghi vào bảng trace
            self.text.insert(tk.END, f"{step_count:<6}{str(s):<30}{depth:<10}{str(is_goal):<10}\n")
            self.text.see(tk.END)
            if is_goal and s == self.goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text=f"DLS: Tìm thấy Goal ở bước {step_count} với limit={limit}")
                self.print_solution(s)
                return
            # Mở rộng khi chưa đạt limit
            if depth < limit:
                for c in reversed(range(self.n)):  # đảo ngược để giữ thứ tự duyệt đúng
                    if all(cc != c and abs(rr - depth) != abs(cc - c) for rr, cc in enumerate(s)):
                        stack.append(s + (c,))
            self.resume_func = step  # lưu lại để Continue gọi tiếp
            self.job = self.root.after(self.delay, step)
        step()

    # ================= UCS ================== (chi phí được tính là các ô đã bị chiếm đóng)
    def run_ucs(self):
        self.stop()
        pq = [(0, ())]
        visited = set()
        step_count = 0
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"{'Step':<6}{'State':<30}{'Cost':<10}{'Goal':<10}\n")
        self.text.insert(tk.END, "-" * 70 + "\n")
        def step():
            nonlocal pq, step_count
            if not pq:
                self.status.config(text="UCS thất bại")
                return
            cost, s = heapq.heappop(pq)
            if s in visited:
                self.job = self.root.after(self.delay, step)
                return
            visited.add(s)
            self.show(self.canvas1, s, "blue")
            step_count += 1
            is_goal = (len(s) == self.n and all(self.is_safe(r, s[r], s[:r]) for r in range(self.n)))
            self.text.insert(tk.END, f"{step_count:<6}{str(s):<30}{cost:<10}{str(is_goal):<10}\n")
            self.text.see(tk.END)
            if is_goal and s == self.goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text=f"UCS: Đã tìm thấy Goal ở bước {step_count}")
                return
            r = len(s)
            if r < self.n:
                for c in range(self.n):
                    if all(cc != c and abs(rr - r) != abs(cc - c) for rr, cc in enumerate(s)):
                        new_state = s + (c,)
                        # Tính cost = số ô hiện bị tấn công
                        attacked = self.attacked_positions(new_state)
                        queens = {(i, new_state[i]) for i in range(len(new_state))}
                        forbidden = attacked
                        step_cost = len(forbidden)
                        # KHÔNG cộng dồn
                        heapq.heappush(pq, (step_cost, new_state))
            self.resume_func = step  # lưu lại để Continue gọi tiếp
            self.job = self.root.after(self.delay, step)
        step()

    # ================= IDS ==================
    def run_ids(self):
        self.stop()
        max_depth = self.n
        current_limit = 0
        stack = [()]
        step_count = 0
        # Chuẩn bị bảng hiển thị
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"{'Bước':<6}{'Trạng thái':<30}{'Depth':<8}{'Limit':<8}{'Goal':<10}\n")
        self.text.insert(tk.END, "-" * 75 + "\n")
        def step():
            nonlocal current_limit, stack, step_count
            # Hết stack, tăng limit
            if not stack:
                current_limit += 1
                if current_limit > max_depth:
                    self.status.config(text="IDS thất bại (đã đạt max_depth)")
                    return
                stack = [()]
                self.status.config(text=f"IDS: tăng limit lên {current_limit}")
                self.job = self.root.after(self.delay, step)
                return
            s = stack.pop()
            self.show(self.canvas1, s, "blue")
            step_count += 1
            depth = len(s)
            is_goal = (depth == self.n and all(self.is_safe(r, s[r], s[:r]) for r in range(self.n)))
            # Ghi vào bảng trace
            self.text.insert(tk.END, f"{step_count:<6}{str(s):<30}{depth:<8}{current_limit:<8}{str(is_goal):<10}\n")
            self.text.see(tk.END)
            # Nếu là goal
            if is_goal and s == self.goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text=f"IDS: Tìm thấy Goal ở depth={depth}, limit={current_limit}")
                self.print_solution(s)
                return
            # Nếu chưa đạt giới hạn thì mở rộng
            if depth < current_limit:
                for c in reversed(range(self.n)):  # đảo ngược để mô phỏng DFS đệ quy
                    if all(cc != c and abs(rr - depth) != abs(cc - c) for rr, cc in enumerate(s)):
                        stack.append(s + (c,))
            self.resume_func = step  # lưu lại để Continue gọi tiếp
            self.job = self.root.after(self.delay, step)
        self.status.config(text=f"IDS: bắt đầu với limit = {current_limit}")
        step()

    # ================= Greedy ==================
    def run_greedy(self):
        self.stop()
        pq = []
        start = ()
        heapq.heappush(pq, (self.heuristic_to_goal(start), start))
        visited = set()
        # Khởi tạo bảng trace
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"{'Bước':<6}{'Trạng thái':<35}{'h(n)':<10}{'Depth':<10}{'Goal':<8}\n")
        self.text.insert(tk.END, "-" * 75 + "\n")
        step_count = 0
        def step():
            nonlocal step_count
            if not pq:
                self.status.config(text="Greedy tìm kiếm thất bại")
                return
            h, s = heapq.heappop(pq)
            if s in visited:
                self.job = self.root.after(self.delay, step)
                return
            visited.add(s)
            step_count += 1
            # Hiển thị bước hiện tại
            self.show(self.canvas1, s, "blue")
            depth = len(s)
            is_goal = (s == self.goal)
            # Ghi vào bảng trace
            self.text.insert(tk.END, f"{step_count:<6}{str(s):<35}{h:<10}{depth:<10}{str(is_goal):<8}\n")
            self.text.see(tk.END)
            # Kiểm tra Goal
            if is_goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text=f"Greedy tìm thấy Goal sau {step_count} bước!")
                self.print_solution(s)
                return
            # Mở rộng node
            r = len(s)
            if r < self.n:
                for c in range(self.n):
                    # Nếu hợp lệ (không xung đột với hậu trước)
                    if all(cc != c and abs(rr - r) != abs(cc - c) for rr, cc in enumerate(s)):
                        new_state = s + (c,)
                        hn = self.heuristic_to_goal(new_state)
                        heapq.heappush(pq, (hn, new_state))
            # Tiếp tục
            self.status.config(text=f"Greedy: Bước={step_count}, h={h}, depth={depth}")
            self.resume_func = step  # lưu lại để Continue gọi tiếp
            self.job = self.root.after(self.delay, step)
        step()

    # ================= A* ==================
    def run_astar(self):
        self.stop()
        start = ()
        pq = []
        heapq.heappush(pq, (self.heuristic_to_goal(start), 0, start, []))  # (f, g, state, cost_list)
        visited = set()
        # Khởi tạo bảng trace
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END,f"{'Bước':<6}{'Trạng thái':<25}{'g(n)':<10}{'h(n)':<10}{'f(n)':<10}{'Depth':<10}{'Goal':<8}\n")
        self.text.insert(tk.END, "-" * 80 + "\n")
        step_count = 0
        def step():
            nonlocal step_count
            if not pq:
                self.status.config(text="A* tìm kiếm thất bại")
                return
            f, g, s, costs = heapq.heappop(pq)
            if s in visited:
                self.job = self.root.after(self.delay, step)
                return
            visited.add(s)
            step_count += 1
            # Tính giá trị heuristic
            h = f - g
            depth = len(s)
            is_goal = (s == self.goal)
            # Hiển thị trạng thái hiện tại
            self.show(self.canvas1, s, "blue")
            # Ghi vào bảng trace
            self.text.insert(tk.END, f"{step_count:<6}{str(s):<25}{g:<10}{h:<10}{f:<10}{depth:<10}{str(is_goal):<8}\n")
            self.text.see(tk.END)
            # Cập nhật trạng thái
            self.status.config(text=f"A*: Bước={step_count}, g(n)={g}, h(n)={h}, f(n)={f}, depth={depth}")
            # Kiểm tra Goal
            if is_goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text=f"A* tìm thấy Goal ở bước {step_count}")
                self.print_solution(s)
                return
            # Mở rộng node
            r = len(s)
            if r < self.n:
                for c in range(self.n):
                    if all(cc != c and abs(rr - r) != abs(cc - c) for rr, cc in enumerate(s)):
                        new_state = s + (c,)
                        step_cost = self.attacked_count(new_state)  # chi phí của bước này
                        new_g = g + step_cost
                        new_h = self.heuristic_to_goal(new_state)
                        new_f = new_g + new_h
                        heapq.heappush(pq, (new_f, new_g, new_state, costs + [step_cost]))
            # Tiếp tục vòng lặp
            self.resume_func = step  # lưu lại để Continue gọi tiếp
            self.job = self.root.after(self.delay, step)
        step()

    # ================= Hill Climbing ==================
    def run_hill_climbing(self):
        self.stop()
        self.text.delete("1.0", tk.END)  # Xóa bảng trace cũ
        self.text.insert(tk.END, f"{'Bước':<6}{'Trạng thái hậu':<30}{'h':<10}{'Best_h':<10}{'Trạng thái':<20}\n")
        self.text.insert(tk.END, "-" * 76 + "\n")
        # Khởi tạo: mỗi hàng một hậu ngẫu nhiên
        current = tuple(random.randint(0, self.n - 1) for _ in range(self.n))
        current_h = self.heuristic_conflicts(current)
        self.status.config(text=f"Hill Climbing bắt đầu: h={current_h}")
        self.show(self.canvas1, current, "blue")
        step_count = 0  # để đánh số bước
        def step(state, h):
            nonlocal step_count
            step_count += 1
            if h == 0:
                if state == self.goal:
                    self.show(self.canvas1, state, "green")
                    self.status.config(text=f"Hill climbing đã tìm thấy GOAL ở bước {step_count}")
                else:
                    self.show(self.canvas1, state, "orange")
                    self.status.config(text=f"Hill climbing đã tìm thấy một GOAL khác")
                self.print_solution(state)
                self.text.insert(tk.END, f"{step_count:<6}{str(state):<30}{h:<10}{'-':<10}{'GOAL':<20}\n")
                return
            neighbors = []
            for r in range(self.n):
                for c in range(self.n):
                    if c != state[r]:
                        new_state = list(state)
                        new_state[r] = c
                        new_state = tuple(new_state)
                        hn = self.heuristic_conflicts(new_state)
                        neighbors.append((hn, new_state))
            if not neighbors:
                self.status.config(text="Hill climbing bị kẹt (không còn neighbors)")
                self.text.insert(tk.END, f"{step_count:<6}{str(state):<30}{h:<10}{'-':<10}{'No neighbors':<20}\n")
                return
            neighbors.sort(key=lambda x: x[0])
            best_h, best_state = neighbors[0]
            # Ghi vào bảng trace
            if best_h < h:
                status = "Move to better"
            else:
                status = "Stuck"
            self.text.insert(tk.END, f"{step_count:<6}{str(state):<30}{h:<10}{best_h:<10}{status:<20}\n")
            self.text.see(tk.END)
            if best_h < h:
                self.show(self.canvas1, best_state, "blue")
                self.status.config(text=f"Hill climbing: h={best_h}")
                self.job = self.root.after(self.delay, step, best_state, best_h)
            else:
                self.show(self.canvas1, state, "red")
                self.status.config(text="Hill climbing bị kẹt (không có neighbors nào tốt hơn)")
        self.resume_func = step  # lưu lại để Continue gọi tiếp
        self.job = self.root.after(self.delay, step, current, current_h)

    # =============== Simulated Annealing ================
    def run_simulated_annealing(self):
        self.stop()
        # Hàm tính nhiệt độ giảm dần theo bước
        def temperature(t):
            return max(0.01, min(1, 1 - t / 500))
        # Khởi tạo trạng thái ngẫu nhiên
        current = tuple(random.randint(0, self.n - 1) for _ in range(self.n))
        current_h = self.heuristic_conflicts(current)
        t = 0
        # Tạo bảng trace
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END,f"{'Bước':<6}{'Trạng thái':<30}{'T':<10}{'h':<8}{'Δ':<8}{'Cải thiện':<12}{'Goal':<8}\n")
        self.text.insert(tk.END, "-" * 80 + "\n")
        def step(state, h, t):
            T = temperature(t)
            if T <= 0.01:
                self.show(self.canvas1, state, "yellow")
                self.status.config(text="SA dừng lại: nhiệt độ quá thấp")
                return
            # Nếu tìm thấy nghiệm
            if h == 0:
                if state == self.goal:
                    self.show(self.canvas1, state, "green")
                    self.status.config(text=f"SA tìm thấy Goal ở bước {t}")
                    self.print_solution(state)
                else:
                    self.show(self.canvas1, state, "red")
                    self.status.config(text="SA tìm thấy nghiệm khác Goal")
                return
            # Chọn neighbor ngẫu nhiên
            neighbor = list(state)
            r = random.randrange(self.n)
            c = random.randrange(self.n)
            neighbor[r] = c
            neighbor = tuple(neighbor)
            neighbor_h = self.heuristic_conflicts(neighbor)
            # Đánh giá
            delta = h - neighbor_h
            improve = delta > 0
            accept = improve or random.random() < math.exp(delta / T)
            new_state, new_h = (neighbor, neighbor_h) if accept else (state, h)
            # Cập nhật hiển thị
            self.show(self.canvas1, new_state, "blue")
            self.status.config(text=f"Bước {t}, h={new_h}, T={T:.3f}")
            # Ghi vào bảng trace
            self.text.insert(tk.END,f"{t:<6}{str(new_state):<30}{T:<10.3f}{new_h:<8}{delta:<8.2f}{str(improve):<12}{str(new_state == self.goal):<8}\n")
            self.text.see(tk.END)
            # Lặp lại
            self.resume_func = lambda: step(new_state, new_h, t + 1)
            self.job = self.root.after(100, step, new_state, new_h, t + 1)
        step(current, current_h, t)

    # ================ Genetic Algorithms ================
    def run_genetic(self):
        self.stop()
        pop_size = 50
        mut_rate = 0.2
        max_gen = 700
        # Hàm fitness: càng ít xung đột thì càng tốt
        def fitness(state):
            non_attacking = 28 - self.heuristic_conflicts(state)  # 28 = số cặp tối đa (8C2)
            return max(1, non_attacking)  # tránh chia 0
        # Khởi tạo quần thể ban đầu
        population = [tuple(random.randint(0, self.n - 1) for _ in range(self.n)) for _ in range(pop_size)]
        generation = 0
        # Tạo bảng trace
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"{'Gen':<6}{'Cá thể tốt nhất':<35}{'Thích nghi':<15}{'Xung đột':<12}{'Goal':<8}\n")
        self.text.insert(tk.END, "-" * 80 + "\n")
        def step(pop, gen):
            scored = [(fitness(ind), ind) for ind in pop]
            scored.sort(reverse=True)
            best_fit, best = scored[0]
            best_conf = self.heuristic_conflicts(best)
            # Hiển thị cá thể tốt nhất lên canvas
            self.show(self.canvas1, best, "blue")
            # Ghi vào bảng trace
            is_goal = (best == self.goal)
            self.text.insert(tk.END, f"{gen:<6}{str(best):<35}{best_fit:<15}{best_conf:<12}{str(is_goal):<8}\n")
            self.text.see(tk.END)
            # Cập nhật trạng thái
            self.status.config(text=f"GA gen={gen}, thích nghi nhất={best_fit}, xung đột={best_conf}")
            # Nếu đạt GOAL
            if best_fit == 28:
                if best == self.goal:
                    self.show(self.canvas1, best, "green")
                    self.status.config(text=f"GA tìm thấy Goal ở gen={gen}!")
                    self.print_solution(best)
                    return
                else:
                    self.status.config(text="GA tìm thấy nghiệm khác goal, chạy lại...")
                    self.job = self.root.after(self.delay, self.run_genetic)
                    return
            # Nếu quá giới hạn thế hệ
            if gen >= max_gen:
                self.show(self.canvas1, best, "yellow")
                self.status.config(text="GA dừng: đã đạt thế hệ tối đa")
                return
            # Chọn lọc (Roulette Wheel)
            total_fit = sum(f for f, _ in scored)
            probs = [f / total_fit for f, _ in scored]
            def select():
                r = random.random()
                cum = 0
                for p, (f, ind) in zip(probs, scored):
                    cum += p
                    if r <= cum:
                        return ind
                return scored[-1][1]
            # Lai ghép để tạo thế hệ mới
            new_pop = []
            while len(new_pop) < pop_size:
                p1, p2 = select(), select()
                cut = random.randint(1, self.n - 2)
                child = p1[:cut] + p2[cut:]
                # Đột biến
                if random.random() < mut_rate:
                    r = random.randrange(self.n)
                    c = random.randrange(self.n)
                    child = list(child)
                    child[r] = c
                    child = tuple(child)
                new_pop.append(child)
            # Gọi lại bước tiếp theo
            self.resume_func = lambda: step(new_pop, gen + 1)
            self.job = self.root.after(self.delay, step, new_pop, gen + 1)
        step(population, generation)

    # ================= Beam Search ===================
    def beam_search(self, beam_width=300, max_restart=20):
        step_count = 0
        restart_count = 0
        queue = [()]  # bắt đầu từ trạng thái rỗng
        # Chuẩn bị bảng hiển thị
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"{'Bước':<6}{'Trạng thái':<35}{'Depth':<8}{'Heuristic':<12}{'Goal':<8}\n")
        self.text.insert(tk.END, "-" * 80 + "\n")
        def step():
            nonlocal queue, step_count, restart_count
            if not queue:
                # Nếu không còn state hợp lệ → restart
                if restart_count < max_restart:
                    restart_count += 1
                    self.text.insert(tk.END, f"\n--- Restart {restart_count}/{max_restart} ---\n")
                    self.status.config(text=f"Beam Search bế tắc, restart {restart_count}/{max_restart}...")
                    queue[:] = [()]  # reset lại từ đầu
                    self.job = self.root.after(self.delay, step)
                    return
                else:
                    self.status.config(text="Beam Search: không tìm thấy nghiệm.")
                    return
            new_states = []
            for state in queue:
                if len(state) == self.n:
                    if state == self.goal:
                        self.show(self.canvas1, state, "green")
                        self.status.config(text=f"Beam Search tìm thấy GOAL sau {step_count} bước")
                        self.print_solution(state)
                        return
                    continue
                row = len(state)
                for col in range(self.n):
                    if self.is_safe(row, col, state):
                        new_states.append(state + (col,))
            # Nếu không có state mới, chuẩn bị restart
            if not new_states:
                queue.clear()
                self.job = self.root.after(self.delay, step)
                return
            # Chọn beam_width tốt nhất dựa trên heuristic
            new_states.sort(key=lambda s: (self.heuristic_conflicts(s), -len(s)))
            queue = new_states[:beam_width]
            step_count += 1
            # Hiển thị trạng thái trên canvas
            for s in queue:
                self.show(self.canvas1, s, "blue")
            # Ghi vào bảng trace
            for s in queue:
                depth = len(s)
                h = self.heuristic_conflicts(s)
                is_goal = (len(s) == self.n and all(self.is_safe(r, s[r], s[:r]) for r in range(self.n)))
                self.text.insert(tk.END, f"{step_count:<6}{str(s):<35}{depth:<8}{h:<12}{str(is_goal):<8}\n")
            self.text.see(tk.END)
            self.status.config(text=f"Beam Search bước {step_count}, beam size={len(queue)}")
            self.resume_func = step  # lưu lại để Continue gọi tiếp
            self.job = self.root.after(self.delay, step)
        step()

    # ================= AND-OR Tree Search ==================
    def run_and_or_search(self):
        self.stop()
        self.status.config(text="AND-OR Tree Search đang chạy...")
        self.path = []
        # Đệ quy AND-OR
        def and_or(state):
            if state == tuple(self.goal):  # so sánh đúng kiểu tuple
                self.path.append((state, "Goal đạt được"))
                return True
            if len(state) == self.n:
                self.path.append((state, "Đủ hàng nhưng chưa phải goal"))
                return False
            r = len(state)
            for c in range(self.n):
                if self.is_safe(r, c, state):
                    new_state = state + (c,)
                    action = f"Đặt hậu hàng {r} vào cột {c}"
                    self.path.append((new_state, action))
                    if and_or(new_state):
                        return True
            self.path.append((state, "Dead-end"))
            return False
        and_or(())
        # Tạo bảng trace
        self.text.delete(1.0, tk.END)
        header = f"{'Bước':<6}{'Trạng thái':<30}{'Hành động':<30}{'Goal':<8}\n"
        self.text.insert(tk.END, header)
        self.text.insert(tk.END, "-" * 80 + "\n")
        # Phát lại quá trình
        step_count = 0  # biến đếm bước
        def step():
            nonlocal step_count
            if step_count >= len(self.path):
                self.status.config(text="AND-OR Tree Search hoàn thành")
                return
            state, action = self.path[step_count]
            is_goal = (state == self.goal)
            if len(state) == self.n and self.is_goal(state):
                color = "green" if is_goal else "orange"
            else:
                color = "blue"
            # Vẽ trạng thái
            self.show(self.canvas1, state, "blue")
            # Cập nhật bảng trace
            pos_str = "(" + ", ".join(str(c) for c in state) + ")" if state else "∅"
            self.text.insert(
                tk.END,f"{step_count + 1:<6}{pos_str:<30}{action:<30}{str(is_goal):<8}\n")
            self.text.see(tk.END)
            step_count += 1  # cập nhật sau khi hiển thị
            # Nếu đạt goal thì dừng lại
            if is_goal:
                self.status.config(text=f"And-Or Tree Search đã tìm thấy Goal ở bước {step_count}")
                self.print_solution(state)
                return
            # Gọi lại step() sau delay
            self.resume_func = step  # lưu lại để Continue gọi tiếp
            self.job = self.root.after(max(self.delay, 30), step)
        step()

    # ================= Belief State Search (Sensorless) ==================
    def run_belief_search(self):
        self.stop()
        belief_state = {()}  # bắt đầu với trạng thái rỗng
        step_count = 0
        # Vẽ belief state lên bàn cờ
        def visualize_belief(belief):
            cv = self.canvas1
            cv.delete("all")
            counts = [[0] * self.n for _ in range(self.n)]
            total = len(belief)
            for state in belief:
                for r, c in enumerate(state):
                    counts[r][c] += 1
            for r in range(self.n):
                for c in range(self.n):
                    x0, y0 = c * self.size, r * self.size
                    x1, y1 = x0 + self.size, y0 + self.size
                    base_color = "#eeeed2" if (r + c) % 2 == 0 else "#769656"
                    cv.create_rectangle(x0, y0, x1, y1, fill=base_color, outline=base_color)
                    # tô màu biểu diễn xác suất xuất hiện
                    if counts[r][c] == total and total > 0:
                        cv.create_rectangle(x0, y0, x1, y1, fill="#0d6efd", stipple="gray25")  # chắc chắn
                    elif counts[r][c] > 0:
                        cv.create_rectangle(x0, y0, x1, y1, fill="#5bc0de", stipple="gray50")  # có thể
        # Mở rộng belief state
        def expand_belief(belief):
            new_belief = set()
            for state in belief:
                row = len(state)
                if row == self.n:
                    new_belief.add(state)
                    continue
                extended = False
                for col in range(self.n):
                    if self.is_safe(row, col, state):
                        new_belief.add(state + (col,))
                        extended = True
                        # thêm 1 khả năng lệch
                        if col + 1 < self.n and self.is_safe(row, col + 1, state):
                            new_belief.add(state + (col + 1,))
                            extended = True
                if not extended:
                    new_belief.add(state)  # giữ lại trạng thái dead-end
            return new_belief
        # Phân loại trạng thái
        def classify_state(state):
            if len(state) == self.n and self.is_goal_state(state, self.goal):
                return True, "Goal"
            elif len(state) < self.n:
                row = len(state)
                can_extend = any(self.is_safe(row, c, state) for c in range(self.n))
                return False, "Expandable" if can_extend else "Dead-end"
            else:
                return False, "Invalid"
        # Hiển thị bảng trace
        def show_belief_states(belief):
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, f"Tổng cộng: {len(belief)} trạng thái\n\n")
            self.text.insert(tk.END, f"{'STT':<5}{'Trạng thái hậu':<55}{'Hành động':<15}{'Goal':<8}\n")
            self.text.insert(tk.END, "-" * 85 + "\n")
            for i, state in enumerate(sorted(belief), 1):
                pos_str = ", ".join([f"({r},{c})" for r, c in enumerate(state)])
                is_goal, label = classify_state(state)
                # Các hành động
                if is_goal:
                    action = "Terminate"
                elif label == "Dead-end":
                    action = "Prune"
                else:
                    action = "Expand"
                goal_flag = str(is_goal)
                self.text.insert(tk.END, f"{i:<5}{pos_str:<55}{action:<15}{goal_flag:<8}\n")
        # Bước thực thi
        def step():
            nonlocal belief_state, step_count
            if not belief_state:
                self.status.config(text="Belief Search thất bại: belief rỗng")
                return
            visualize_belief(belief_state)
            show_belief_states(belief_state)
            # dừng nếu có goal trong belief
            if any(len(s) == self.n and self.is_goal_state(s, self.goal) for s in belief_state):
                self.status.config(text="Belief Search: Đã tìm thấy goal")
                return
            next_belief = expand_belief(belief_state)
            if next_belief == belief_state:
                self.status.config(text="Belief Search dừng lại: không thể mở rộng thêm (dead-end toàn cục).")
                return
            belief_state = next_belief
            step_count += 1
            self.status.config(text=f"Belief Search - Bước {step_count}, belief size={len(belief_state)}")
            self.job = self.root.after(self.delay * 2, step)
        # Kiểm tra goal
        def is_goal_state(self_obj, state, goal_state):
            return len(state) == self_obj.n and all(self_obj.is_safe(r, state[r], state[:r]) for r in range(self_obj.n))
        self.resume_func = step  # lưu lại để Continue gọi tiếp
        self.is_goal_state = is_goal_state.__get__(self, self.__class__)
        step()

    # ================= Partial Observation Search ==================
    def run_partial_search(self):
        self.stop()
        n = self.n
        step_count = 0
        observed_rows = 2  # số hàng quan sát được
        observed_state = tuple(self.goal[:observed_rows])
        belief_state = {observed_state}
        # Kiểm tra goal
        def is_goal_state(state):
            return len(state) == n and all(self.is_safe(r, state[r], state[:r]) for r in range(n))
        # Phân loại trạng thái
        def classify_state(state):
            if len(state) == n:
                if is_goal_state(state):
                    if state == self.goal:
                        return True, "Goal (chính xác)"
                    else:
                        return True, "Goal khác self.goal"
                else:
                    return False, "Đủ hàng nhưng không hợp lệ"
            else:
                row = len(state)
                can_extend = any(self.is_safe(row, c, state) for c in range(n))
                return False, "Dead-end" if not can_extend else "Expandable"
        # Mở rộng belief
        def expand_belief(belief):
            new_belief = set()
            for state in belief:
                row = len(state)
                if row < observed_rows:
                    new_belief.add(state)
                    continue
                if len(state) == n:
                    new_belief.add(state)
                    continue
                extended = False
                for col in range(n):
                    if self.is_safe(row, col, state):
                        new_belief.add(state + (col,))
                        extended = True
                if not extended:
                    new_belief.add(state)
            return new_belief
        # Vẽ belief state lên canvas (ô màu)
        def visualize_belief(belief):
            cv = self.canvas1
            cv.delete("all")
            counts = [[0] * n for _ in range(n)]
            total = len(belief)
            for state in belief:
                for r, c in enumerate(state):
                    counts[r][c] += 1
            for r in range(n):
                for c in range(n):
                    x0, y0 = c * self.size, r * self.size
                    x1, y1 = x0 + self.size, y0 + self.size
                    base = "#eeeed2" if (r + c) % 2 == 0 else "#769656"
                    cv.create_rectangle(x0, y0, x1, y1, fill=base, outline=base)
                    # hàng đã quan sát chuyển sang màu cam
                    if r < observed_rows:
                        if counts[r][c] > 0:
                            cv.create_rectangle(x0, y0, x1, y1, fill="#ff9800")
                    # ô chắc chắn xuất hiện trong mọi belief thì xanh đậm
                    elif counts[r][c] == total and total > 0:
                        cv.create_rectangle(x0, y0, x1, y1, fill="#0d6efd", stipple="gray25")
                    # ô có thể thì xanh nhạt
                    elif counts[r][c] > 0:
                        cv.create_rectangle(x0, y0, x1, y1, fill="#5bc0de", stipple="gray50")
        # Hiển thị bảng trace
        def show_trace_table(belief):
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, f"Tổng cộng: {len(belief)} trạng thái\n\n")
            self.text.insert(tk.END, f"{'STT':<5}{'Trạng thái hậu':<60}{'Hành động':<15}{'Goal':<8}\n")
            self.text.insert(tk.END, "-" * 85 + "\n")
            for i, state in enumerate(sorted(belief), 1):
                pos_str = ", ".join([f"({r},{c})" for r, c in enumerate(state)])
                is_goal, label = classify_state(state)
                # Các hành động
                if is_goal:
                    action = "Terminate"
                elif label == "Dead-end":
                    action = "Prune"
                else:
                    action = "Expand"
                goal_flag = str(is_goal)
                self.text.insert(
                    tk.END,f"{i:<5}{pos_str:<60}{action:<15}{goal_flag:<8}\n")
        # Vòng lặp belief search
        def step():
            nonlocal belief_state, step_count
            if not belief_state:
                self.status.config(text="Belief Search 2 thất bại: belief rỗng")
                return
            visualize_belief(belief_state)
            show_trace_table(belief_state)
            # Kiểm tra goal
            if any(is_goal_state(s) for s in belief_state):
                self.status.config(text="Belief Search 2 đã tìm thấy goal")
                return
            next_belief = expand_belief(belief_state)
            if next_belief == belief_state:
                self.status.config(text="Belief Search 2 dừng lại: không thể mở rộng thêm")
                return
            belief_state = next_belief
            step_count += 1
            self.status.config(text=f"Belief Search 2 - Bước {step_count}, belief size={len(belief_state)}")
            self.resume_func = step  # lưu lại để Continue gọi tiếp
            self.job = self.root.after(self.delay * 2, step)
        step()

    # ================= BackTracking ==================
    def run_backtracking(self):
        # Hủy tiến trình cũ nếu đang chạy
        if hasattr(self, 'job') and self.job:
            self.root.after_cancel(self.job)
        # Khởi tạo trạng thái
        self.running = True
        self.paused = False
        self.step_count = 0
        self.found = False
        stack = [tuple()]
        # Reset giao diện
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"{'Bước':<6}{'Trạng thái':<35}{'Depth':<10}{'Goal':<6}\n")
        self.text.insert(tk.END, "-" * 70 + "\n")
        self.status.config(text="Bắt đầu chạy Backtracking...")
        # Hàm step thực hiện từng bước
        def step():
            # Nếu bị pause, vòng lặp sẽ dừng lại. Hàm continue_backtracking sẽ gọi lại step.
            if self.paused:
                return
            if not self.running or not stack:
                if not self.found and self.running:
                    self.status.config(text="Backtracking hoàn thành, không tìm thấy Goal.")
                self.running = False
                return
            # Logic thuật toán cho một bước
            state = stack.pop()
            self.step_count += 1
            depth = len(state)
            # Cập nhật bảng trace
            self.text.insert(tk.END, f"{self.step_count:<6}{str(state):<35}{depth:<10}{str(state == self.goal):<6}\n")
            self.text.see(tk.END)
            self.show(self.canvas1, state, "blue")
            # Kiểm tra goal
            if depth == self.n and state == self.goal:
                self.found = True
                self.running = False
                self.show(self.canvas1, state, "green")
                self.status.config(text=f"Backtracking tìm thấy Goal ở bước {self.step_count}")
                self.print_solution(state)
                return
            # Sinh trạng thái con nếu chưa đủ N hậu
            if depth < self.n:
                row = depth
                for col in range(self.n - 1, -1, -1):
                    if self.is_safe(row, col, state):
                        stack.append(state + (col,))
            # Lên lịch cho bước tiếp theo
            self.job = self.root.after(1, step)
        # Bắt đầu thuật toán
        self.resume_func = step
        # Bắt đầu lần chạy đầu tiên
        step()

    # ================= Forward Checking ====================
    def run_forwardchecking(self):
        # Hủy tiến trình cũ nếu đang chạy
        if hasattr(self, 'job') and self.job:
            self.root.after_cancel(self.job)
        # Khởi tạo trạng thái
        self.running = True
        self.paused = False
        self.step_count = 0
        self.found = False
        n = self.n
        # Reset giao diện
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"{'Bước':<6}{'Trạng thái':<35}{'Depth':<10}{'Goal':<6}\n")
        self.text.insert(tk.END, "-" * 70 + "\n")
        self.status.config(text="Bắt đầu chạy Forward Checking...")
        # Khởi tạo domains ban đầu
        initial_domains = {r: set(range(n)) for r in range(n)}
        stack = [(tuple(), initial_domains)]
        # Hàm forward_checking
        def forward_checking(state, domains):
            row = len(state) - 1
            col = state[-1]
            new_domains = {r: set(domains[r]) for r in range(n)}
            for r in range(row + 1, n):
                if col in new_domains[r]:
                    new_domains[r].remove(col)
                dist = r - row
                if col - dist in new_domains[r]:
                    new_domains[r].remove(col - dist)
                if col + dist in new_domains[r]:
                    new_domains[r].remove(col + dist)
                if not new_domains[r]:
                    return None
            return new_domains
        # Hàm step() để thực hiện từng bước
        def step():
            if self.paused:
                return
            if not self.running or not stack:
                if not self.found and self.running:
                    self.status.config(text="Forward Checking hoàn thành, không tìm thấy Goal.")
                self.running = False
                return
            state, domains = stack.pop()
            self.step_count += 1
            depth = len(state)
            # Cập nhật giao diện
            self.text.insert(tk.END, f"{self.step_count:<6}{str(state):<35}{depth:<10}{str(state == self.goal):<6}\n")
            self.text.see(tk.END)
            self.show(self.canvas1, state, "blue")
            # Xử lý khi tìm thấy một giải pháp
            if depth == n:
                # Kiểm tra goal
                if state == self.goal:
                    self.found = True
                    self.running = False
                    self.show(self.canvas1, state, "green")
                    self.status.config(text=f"Forward Checking tìm thấy Goal ở bước {self.step_count}")
                    self.print_solution(state)
                # Lên lịch cho bước tiếp theo để xử lý các trạng thái khác trong stack.
                self.job = self.root.after(1, step)
                return  # Dừng thực thi hàm step cho trạng thái này
            # Sinh ra các trạng thái con hợp lệ
            row = depth
            for col in sorted(list(domains[row]), reverse=True):
                new_state = state + (col,)
                new_domains = forward_checking(new_state, domains)
                if new_domains is not None:
                    stack.append((new_state, new_domains))
            # Lên lịch để thực hiện bước tiếp theo
            self.job = self.root.after(1, step)
        # Bắt đầu chạy thuật toán
        self.resume_func = step
        step()

root = tk.Tk()
app = NQueensGUI(root)
root.mainloop()
