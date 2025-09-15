import tkinter as tk
from tkinter import ttk
import random
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

        self.root.title("8 Queens")
        self.canvas1 = tk.Canvas(root, width=n*self.size, height=n*self.size)
        self.canvas1.pack(side="left", padx=5, pady=5)
        self.canvas2 = tk.Canvas(root, width=n*self.size, height=n*self.size)
        self.canvas2.pack(side="right", padx=5, pady=5)

        # tạo 2 dòng nút
        frame_top = ttk.Frame(root)
        frame_top.pack(side="bottom", pady=2)

        frame_bottom = ttk.Frame(root)
        frame_bottom.pack(side="bottom", pady=2)

        # ====== Dòng trên ======
        ttk.Button(frame_bottom, text="Random Goal", command=self.new_goal).pack(side="left", padx=5)
        ttk.Button(frame_bottom, text="BFS", command=self.run_bfs).pack(side="left", padx=5)
        ttk.Button(frame_bottom, text="BFS(2)", command=self.run_bfs2).pack(side="left", padx=5)
        ttk.Button(frame_bottom, text="DFS", command=self.run_dfs).pack(side="left", padx=5)

        # ====== Dòng dưới ======
        self.dls_limit_var = tk.IntVar(value=self.n)
        ttk.Label(frame_top, text="DLS limit:").pack(side="left", padx=(12, 2))
        ttk.Entry(frame_top, width=3, textvariable=self.dls_limit_var).pack(side="left", padx=(0, 8))

        ttk.Button(frame_top, text="DLS", command=self.run_dls).pack(side="left", padx=5)
        ttk.Button(frame_top, text="UCS", command=self.run_ucs).pack(side="left", padx=5)
        ttk.Button(frame_top, text="IDS", command=self.run_ids).pack(side="left", padx=5)
        ttk.Button(frame_top, text="Stop", command=self.stop).pack(side="left", padx=5)

        self.status = ttk.Label(root, text="Ready", relief="sunken", anchor="w")
        self.status.pack(side="bottom", fill="x")

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
        if self.job:
            try: self.root.after_cancel(self.job)
            except: pass
        self.job = None
        self.status.config(text="Stopped")

    def print_solution(self, s):
        print("Nghiệm tìm được:", tuple(s))

    def attacked_count(self, state):
        """Đếm số ô đã bị 'chiếm' (bởi các hậu trong state)."""
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

    # ================= BFS, BFS2, DFS ==================
    def run_bfs(self):
        self.stop()
        q = deque([()]); goal = self.goal
        def step():
            if not q:
                self.status.config(text="BFS fail"); return
            s = q.popleft()
            self.show(self.canvas1, s, "blue")
            if s == goal:
                self.show(self.canvas1, s, "green"); self.status.config(text="BFS found"); self.print_solution(s); return
            r = len(s)
            if r < self.n:
                for c in range(self.n):
                    if all(cc!=c and abs(rr-r)!=abs(cc-c) for rr,cc in enumerate(s)):
                        q.append(s+(c,))
            self.job = self.root.after(self.delay, step)
        step()

    def run_bfs2(self):
        self.stop()
        q = deque([()]); explored = []; goal = self.goal
        def step():
            if not q:
                self.status.config(text="BFS2 fail"); return
            s = q.popleft()
            if s in explored:
                self.job = self.root.after(self.delay, step); return
            explored.append(s)
            self.show(self.canvas1, s, "blue")
            if s == goal:
                self.show(self.canvas1, s, "green"); self.status.config(text="BFS2 found"); self.print_solution(s); return
            r = len(s)
            if r < self.n:
                for c in range(self.n):
                    if all(cc!=c and abs(rr-r)!=abs(cc-c) for rr,cc in enumerate(s)):
                        if s+(c,) not in explored and s+(c,) not in q:
                            q.append(s+(c,))
            self.job = self.root.after(self.delay, step)
        step()

    def run_dfs(self):
        self.stop()
        st = [()]; visited = []; goal = self.goal
        def step():
            if not st:
                self.status.config(text="DFS fail"); return
            s = st.pop()
            if s in visited:
                self.job = self.root.after(self.delay, step); return
            visited.append(s)
            self.show(self.canvas1, s, "blue")
            if s == goal:
                self.show(self.canvas1, s, "green"); self.status.config(text="DFS found"); self.print_solution(s); return
            r = len(s)
            if r < self.n:
                for c in reversed(range(self.n)):
                    if all(cc!=c and abs(rr-r)!=abs(cc-c) for rr,cc in enumerate(s)):
                        if s+(c,) not in visited and s+(c,) not in st:
                            st.append(s+(c,))
            self.job = self.root.after(self.delay, step)
        step()

    # ================= DLS ==================
    def run_dls(self):
        self.stop()
        # lấy limit từ entry (nếu người dùng nhập sai -> dùng n)
        try:
            limit = int(self.dls_limit_var.get())
            if limit < 0: limit = 0
        except Exception:
            limit = self.n
        stack = [()]   # stack chứa các state (tuple)
        goal = self.goal
        def step():
            if not stack:
                self.status.config(text=f"DLS fail (limit={limit})")
                return
            s = stack.pop()
            # hiển thị phần trạng thái (s có thể là ngắn)
            self.show(self.canvas1, s, "blue")
            if s == goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text=f"DLS found (limit={limit})")
                self.print_solution(s)
                return
            r = len(s)
            if r < limit:   # chỉ mở rộng khi chưa đạt limit
                # đẩy con lên stack theo thứ tự để mô phỏng DFS (đảo chiều để giống đệ quy)
                for c in reversed(range(self.n)):
                    if all(cc!=c and abs(rr-r)!=abs(cc-c) for rr,cc in enumerate(s)):
                        stack.append(s+(c,))
            self.job = self.root.after(self.delay, step)
        step()
    # ================= UCS ==================
    def run_ucs(self):
        self.stop()
        pq = [(0, (), [])]  # (tổng chi phí hoặc step_cost, state, danh sách chi phí)
        visited = set()
        goal = self.goal

        def step():
            if not pq:
                self.status.config(text="UCS fail"); return
            cost, s, costs = heapq.heappop(pq)
            if s in visited:
                self.job = self.root.after(self.delay, step); return
            visited.add(s)

            self.show(self.canvas1, s, "blue")

            if s == goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text="UCS found")
                print("Nghiệm tìm được:", s)
                print("Chi phí sau mỗi bước:", costs)
                return

            r = len(s)
            if r < self.n:
                for c in range(self.n):
                    if all(cc!=c and abs(rr-r)!=abs(cc-c) for rr,cc in enumerate(s)):
                        new_state = s+(c,)
                        step_cost = self.attacked_count(new_state)
                        heapq.heappush(pq, (step_cost, new_state, costs+[step_cost]))

            self.job = self.root.after(self.delay, step)
        step()
    # ================= IDS ==================
    def run_ids(self):
        self.stop()
        goal = self.goal
        max_depth = self.n
        current_limit = 0
        stack = [()]  # sẽ reset mỗi vòng
        def step():
            nonlocal current_limit, stack
            if not stack:
                # nếu hết stack mà chưa tìm thấy thì tăng limit
                current_limit += 1
                if current_limit > max_depth:
                    self.status.config(text="IDS fail")
                    return
                stack = [()]
                self.status.config(text=f"IDS: tăng limit lên {current_limit}")
                self.job = self.root.after(self.delay, step)
                return
            s = stack.pop()
            self.show(self.canvas1, s, "blue")
            if s == goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text=f"IDS found (depth={len(s)})")
                self.print_solution(s)
                return

            r = len(s)
            if r < current_limit:
                for c in reversed(range(self.n)):
                    if all(cc != c and abs(rr - r) != abs(cc - c) for rr, cc in enumerate(s)):
                        stack.append(s + (c,))
            self.job = self.root.after(self.delay, step)
        self.status.config(text=f"IDS: bắt đầu với limit = {current_limit}")
        step()

root = tk.Tk()
app = NQueensGUI(root)
root.mainloop()
