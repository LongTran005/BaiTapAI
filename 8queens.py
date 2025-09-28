import tkinter as tk
from tkinter import ttk
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
        self.running = False  # flag chung cho một số search

        self.root.title("8 Queens")
        self.canvas1 = tk.Canvas(root, width=n*self.size, height=n*self.size)
        self.canvas1.pack(side="left", padx=5, pady=5)
        self.canvas2 = tk.Canvas(root, width=n*self.size, height=n*self.size)
        self.canvas2.pack(side="right", padx=5, pady=5)

        # tạo 3 dòng nút
        frame_top = ttk.Frame(root)
        frame_top.pack(side="bottom", pady=2)

        frame_bottom = ttk.Frame(root)
        frame_bottom.pack(side="bottom", pady=2)

        frame_middle = ttk.Frame(root)
        frame_middle.pack(side="bottom", pady=5)

        # ====== Dòng trên ======
        ttk.Button(frame_bottom, text="Random Goal", command=self.new_goal).pack(side="left", padx=5)
        ttk.Button(frame_bottom, text="BFS", command=self.run_bfs).pack(side="left", padx=5)
        ttk.Button(frame_bottom, text="BFS(2)", command=self.run_bfs2).pack(side="left", padx=5)
        ttk.Button(frame_bottom, text="DFS", command=self.run_dfs).pack(side="left", padx=5)
        ttk.Button(frame_bottom, text="DLS", command=self.run_dls).pack(side="left", padx=5)
        ttk.Button(frame_bottom, text="UCS", command=self.run_ucs).pack(side="left", padx=5)
        ttk.Button(frame_bottom, text="IDS", command=self.run_ids).pack(side="left", padx=5)

        # ====== Dòng dưới ======
        self.dls_limit_var = tk.IntVar(value=self.n)
        ttk.Label(frame_top, text="DLS limit:").pack(side="left", padx=(12, 2))
        ttk.Entry(frame_top, width=3, textvariable=self.dls_limit_var).pack(side="left", padx=(0, 8))

        ttk.Button(frame_top, text="Greedy", command=self.run_greedy).pack(side="left", padx=5)
        ttk.Button(frame_top, text="A*", command=self.run_astar).pack(side="left", padx=5)
        ttk.Button(frame_top, text="Hill Climbing", command=self.run_hill_climbing).pack(side="left", padx=5)
        ttk.Button(frame_top, text="SA", command=self.run_simulated_annealing).pack(side="left", padx=5)
        ttk.Button(frame_top, text="GA", command=self.run_genetic).pack(side="left", padx=5)
        ttk.Button(frame_top, text="Stop", command=self.stop).pack(side="left", padx=5)

        # ====== Dòng giữa ======
        ttk.Button(frame_middle, text="Beam", command=self.beam_search).pack(side="left", padx=5)
        ttk.Button(frame_middle, text="AND-OR", command=self.run_and_or_search).pack(side="left", padx=5)
        ttk.Button(frame_middle, text="Belief", command=self.run_belief_search).pack(side="left", padx=5)

        self.status = ttk.Label(root, text="Ready", relief="sunken", anchor="w")
        self.status.pack(side="bottom", fill="x")

        # Khung hiển thị belief cuối cùng
        self.belief_text = tk.Text(root, height=12, width=80, font=("Consolas", 11))
        self.belief_text.pack(pady=5)

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
        # stop any ongoing animation/search
        self.running = False
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

    def attacked_positions(self, state):
        """Trả về tập các ô (r,c) bị chiếm/đe dọa bởi state."""
        attacked = set()
        for r, c in enumerate(state):
            # hàng & cột
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
        """Kiểm tra có thể đặt ở (row,col) với state hiện tại không."""
        for r, c in enumerate(state):
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def is_goal(self, state):
        """Kiểm tra xem state có phải là lời giải hoàn chỉnh hay không."""
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

    # ================= Greedy ==================
    def heuristic_to_goal(self, state):
        # heuristic đơn giản: số hậu còn thiếu để đạt 8
        return self.n - len(state)
    def run_greedy(self):
        self.stop()
        pq = []  # (h(n), state)
        start = ()
        heapq.heappush(pq, (self.heuristic_to_goal(start), start))
        visited = set()
        goal = tuple(self.goal)
        def step():
            if not pq:
                self.status.config(text="Greedy fail")
                return
            h, s = heapq.heappop(pq)
            if s in visited:
                self.job = self.root.after(self.delay, step)
                return
            visited.add(s)
            # Hiển thị bước hiện tại
            self.show(self.canvas1, s, "blue")
            self.status.config(text=f"Greedy: h={h} depth={len(s)}")
            if s == goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text="Greedy found")
                self.print_solution(s)
                return
            r = len(s)
            if r < self.n:
                for c in range(self.n):
                    if all(cc != c and abs(rr - r) != abs(cc - c) for rr, cc in enumerate(s)):
                        new_state = s + (c,)
                        hn = self.heuristic_to_goal(new_state)
                        heapq.heappush(pq, (hn, new_state))
            self.job = self.root.after(self.delay, step)
        step()

    # ================= A* ==================
    def run_astar(self):
        self.stop()
        start = ()
        goal = tuple(self.goal)
        pq = []  # (f, g, state, path_costs)
        heapq.heappush(pq, (self.heuristic_to_goal(start), 0, start, []))
        visited = set()
        def step():
            if not pq:
                self.status.config(text="A* fail")
                return
            f, g, s, costs = heapq.heappop(pq)
            if s in visited:
                self.job = self.root.after(self.delay, step)
                return
            visited.add(s)
            # Hiển thị trạng thái hiện tại
            self.show(self.canvas1, s, "blue")
            self.status.config(text=f"A*: g={g}, h={f - g}, f={f}, depth={len(s)}")
            if s == goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text="A* found")
                print("Nghiệm tìm được:", s)
                print("Chi phí từng bước:", costs)
                return
            r = len(s)
            if r < self.n:
                for c in range(self.n):
                    if all(cc != c and abs(rr - r) != abs(cc - c) for rr, cc in enumerate(s)):
                        new_state = s + (c,)
                        step_cost = self.attacked_count(new_state)
                        new_g = g + step_cost
                        new_h = self.heuristic_to_goal(new_state)
                        heapq.heappush(pq, (new_g + new_h, new_g, new_state, costs + [step_cost]))
            self.job = self.root.after(self.delay, step)
        step()
    # ================= Hill Climbing ==================
    def heuristic_conflicts(self, state):
        """Hàm heuristic: đếm số cặp hậu tấn công nhau"""
        conflicts = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def run_hill_climbing(self):
        self.stop()
        import random
        # Khởi tạo: mỗi hàng một hậu ngẫu nhiên
        current = tuple(random.randint(0, self.n - 1) for _ in range(self.n))
        current_h = self.heuristic_conflicts(current)

        self.status.config(text=f"Hill Climbing start: h={current_h}")
        self.show(self.canvas1, current, "blue")

        def step(state, h):
            if h == 0:
                self.show(self.canvas1, state, "red")
                self.status.config(text="Hill climbing reached GOAL (no conflicts)!")
                self.print_solution(state)
                return

            neighbors = []
            # Sinh các neighbor bằng cách di chuyển hậu ở hàng r sang cột khác
            for r in range(self.n):
                for c in range(self.n):
                    if c != state[r]:
                        new_state = list(state)
                        new_state[r] = c
                        new_state = tuple(new_state)
                        hn = self.heuristic_conflicts(new_state)
                        neighbors.append((hn, new_state))

            if not neighbors:
                self.status.config(text="Hill climbing stuck (no neighbors)!")
                return

            # Sắp xếp neighbor theo heuristic
            neighbors.sort(key=lambda x: x[0])
            best_h, best_state = neighbors[0]

            # Hiển thị việc đang xét các neighbor
            if best_h < h:
                self.show(self.canvas1, best_state, "blue")
                self.status.config(text=f"Hill climbing: h={best_h}")
                self.job = self.root.after(self.delay, step, best_state, best_h)
            else:
                # Kẹt: không có neighbor nào tốt hơn
                self.show(self.canvas1, state, "orange")
                self.status.config(text="Hill climbing stuck at local optimum!")
        self.job = self.root.after(self.delay, step, current, current_h)

    # =============== Simulated Annealing ================
    def run_simulated_annealing(self):
        self.stop()
        goal = tuple(self.goal)

        def temperature(t):
            return max(0.01, min(1, 1 - t / 500))

        current = tuple(random.randint(0, self.n - 1) for _ in range(self.n))
        current_h = self.heuristic_conflicts(current)
        t = 0

        def step(state, h, t):
            T = temperature(t)
            if T <= 0.01:
                self.show(self.canvas1, state, "yellow")
                self.status.config(text="SA stopped: temperature too low")
                return
            if h == 0:  # nghiệm hợp lệ
                if state == goal:
                    self.show(self.canvas1, state, "green")
                    self.status.config(text="SA found the GOAL!")
                    self.print_solution(state)
                else:
                    self.show(self.canvas1, state, "red")
                    self.status.config(text="SA found another solution (not the goal)")
                return
            # chọn láng giềng
            neighbor = list(state)
            r = random.randrange(self.n)
            c = random.randrange(self.n)
            neighbor[r] = c
            neighbor = tuple(neighbor)
            neighbor_h = self.heuristic_conflicts(neighbor)
            delta = h - neighbor_h
            if delta > 0 or random.random() < math.exp(delta / T):
                new_state, new_h = neighbor, neighbor_h
            else:
                new_state, new_h = state, h
            self.show(self.canvas1, new_state, "blue")
            self.status.config(text=f"SA step {t}, h={new_h}, T={T:.3f}")
            self.job = self.root.after(self.delay, step, new_state, new_h, t + 1)
        step(current, current_h, t)

    # ================ Genetic Algorithms ================
    def run_genetic(self):
        self.stop()
        goal = tuple(self.goal)
        POP_SIZE = 50
        MUT_RATE = 0.2
        MAX_GEN = 700
        # --- hàm fitness ---
        def fitness(state):
            non_attacking = 28 - self.heuristic_conflicts(state)  # 28 cặp max
            return max(1, non_attacking)  # tránh chia 0
        # --- khởi tạo quần thể ---
        population = [tuple(random.randint(0, self.n - 1) for _ in range(self.n))
                      for _ in range(POP_SIZE)]
        generation = 0
        def step(pop, gen):
            scored = [(fitness(ind), ind) for ind in pop]
            scored.sort(reverse=True)
            best_fit, best = scored[0]
            # hiển thị cá thể tốt nhất
            self.show(self.canvas1, best, "blue")
            self.status.config(text=f"GA gen={gen}, best_fit={best_fit}")
            if best_fit == 28:
                if best == goal:
                    self.show(self.canvas1, best, "green")
                    self.status.config(text=f"GA found GOAL at gen={gen}!")
                    self.print_solution(best)
                    return
                else:
                    self.status.config(text="GA found another solution, restarting...")
                    self.job = self.root.after(self.delay, self.run_genetic)
                    return
            if gen >= MAX_GEN:
                self.show(self.canvas1, best, "yellow")
                self.status.config(text="GA stopped: max generations reached")
                return
            # --- chọn lọc theo roulette wheel ---
            total_fit = sum(f for f, _ in scored)
            probs = [f/total_fit for f, _ in scored]

            def select():
                r = random.random()
                cum = 0
                for p, (f, ind) in zip(probs, scored):
                    cum += p
                    if r <= cum:
                        return ind
                return scored[-1][1]
            # --- tạo thế hệ mới ---
            new_pop = []
            while len(new_pop) < POP_SIZE:
                p1, p2 = select(), select()
                # crossover
                cut = random.randint(1, self.n - 2)
                child = p1[:cut] + p2[cut:]
                # mutation
                if random.random() < MUT_RATE:
                    r = random.randrange(self.n)
                    c = random.randrange(self.n)
                    child = list(child)
                    child[r] = c
                    child = tuple(child)
                new_pop.append(child)
            self.job = self.root.after(self.delay, step, new_pop, gen + 1)
        step(population, generation)

    # ================= Beam Search ===================
    def beam_search(self, beam_width=200, max_restart=20):
        goal = tuple(self.goal)
        step_count = 0
        restart_count = 0
        queue = [()]  # bắt đầu từ trạng thái rỗng

        def step():
            nonlocal queue, step_count, restart_count
            if not queue:
                if restart_count < max_restart:
                    restart_count += 1
                    self.status.config(
                        text=f"Beam Search bế tắc, restart {restart_count}/{max_restart}..."
                    )
                    queue[:] = [()]  # reset lại từ đầu
                    self.job = self.root.after(self.delay, step)
                    return
                else:
                    self.status.config(text="Beam Search: không tìm thấy nghiệm.")
                    return
            new_states = []
            for state in queue:
                if len(state) == self.n:
                    if state == goal:
                        self.show(self.canvas1, state, "green")
                        self.status.config(
                            text=f"Beam Search tìm thấy GOAL sau {step_count} bước!"
                        )
                        self.print_solution(state)
                        return
                    continue
                row = len(state)
                for col in range(self.n):
                    if self.is_safe(row, col, state):
                        new_states.append(state + (col,))
            if not new_states:
                queue.clear()  # để trigger restart
                self.job = self.root.after(self.delay, step)
                return
            # chọn beam_width tốt nhất
            new_states.sort(key=lambda s: (self.heuristic_conflicts(s), -len(s)))
            queue = new_states[:beam_width]
            step_count += 1
            for s in queue:
                self.show(self.canvas1, s, "blue")
            self.status.config(
                text=f"Beam Search bước {step_count}, beam size={len(queue)}"
            )
            self.job = self.root.after(self.delay, step)
        step()

    # ================= AND-OR Tree Search ==================
    def run_and_or_search(self):
        self.stop()
        goal = tuple(self.goal)
        self.status.config(text="AND-OR Tree Search đang chạy...")

        self.path = []  # để lưu lại các bước đặt hậu

        # đệ quy để lấy danh sách các bước
        def and_or_search_steps(state):
            # Nếu đã là goal
            if state == goal:
                self.path.append(("solution", state))
                return True
            # Nếu đặt đủ hậu nhưng không phải goal → thất bại
            if len(state) == self.n:
                return False

            r = len(state)  # hàng kế tiếp để đặt hậu
            for c in range(self.n):
                if self.is_safe(r, c, state):
                    new_state = state + (c,)
                    self.path.append(("place", new_state))  # thêm bước đặt hậu
                    if and_or_search_steps(new_state):
                        return True
                    self.path.append(("backtrack", state))  # quay lui nếu sai
            return False
        # Gọi đệ quy 1 lần để thu thập tất cả các bước
        and_or_search_steps(())
        # phát lại các bước
        self.step_index = 0
        def animate_steps():
            if self.step_index >= len(self.path):
                self.status.config(text="AND-OR Tree Search hoàn thành!")
                return
            action, state = self.path[self.step_index]
            if action == "place":
                self.show(self.canvas1, state, "blue")
            elif action == "backtrack":
                self.show(self.canvas1, state, "red")
            elif action == "solution":
                self.show(self.canvas1, state, "green")
            self.step_index += 1
            # 👇 điều chỉnh thời gian mỗi bước
            self.job = self.root.after(20, animate_steps)  # 20ms mỗi bước
        # Bắt đầu phát từng bước
        animate_steps()

    # ================= Belief State Search ==================
    def run_belief_search(self):
        self.stop()
        goal = tuple(self.goal)
        belief_state = {()}  # bắt đầu với trạng thái rỗng
        step_count = 0
        def visualize_belief(belief):
            """Vẽ các ô dựa trên xác suất xuất hiện hậu."""
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
                    if counts[r][c] == total and total > 0:
                        cv.create_rectangle(x0, y0, x1, y1, fill="#0d6efd", stipple="gray25")
                    elif counts[r][c] > 0:
                        cv.create_rectangle(x0, y0, x1, y1, fill="#5bc0de", stipple="gray50")
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
                        # thêm trường hợp lệch
                        if col + 1 < self.n and self.is_safe(row, col + 1, state):
                            new_belief.add(state + (col + 1,))
                            extended = True
                # nếu không mở rộng được -> vẫn giữ trạng thái này để đánh dấu dead-end
                if not extended:
                    new_belief.add(state)
            return new_belief
        def classify_state(state):
            if len(state) == self.n and self.is_goal_state(state, goal):
                return "Goal"
            elif len(state) < self.n:
                # kiểm tra xem có thể mở rộng tiếp không
                row = len(state)
                can_extend = any(self.is_safe(row, c, state) for c in range(self.n))
                return "Dead-end" if not can_extend else "Expandable"
            else:
                return "Invalid"
        def show_belief_states(belief):
            self.belief_text.delete(1.0, tk.END)
            self.belief_text.insert(tk.END, f"Tổng: {len(belief)} trạng thái\n\n")
            self.belief_text.insert(tk.END, f"{'STT':<5}{'Trạng thái hậu':<50}{'Trạng thái':<15}\n")
            self.belief_text.insert(tk.END, "-" * 70 + "\n")
            for i, state in enumerate(sorted(belief), 1):
                pos_str = ", ".join([f"({r},{c})" for r, c in enumerate(state)])
                label = classify_state(state)
                self.belief_text.insert(tk.END, f"{i:<5}{pos_str:<55}{label:<15}\n")
        def step():
            nonlocal belief_state, step_count
            if not belief_state:
                self.status.config(text="Belief search thất bại: belief rỗng")
                return
            visualize_belief(belief_state)
            show_belief_states(belief_state)
            # nếu đã có goal trong belief → dừng
            if any(len(s) == self.n and self.is_goal_state(s, goal) for s in belief_state):
                self.status.config(text=f"Belief Search: Đã tìm thấy goal")
                return
            next_belief = expand_belief(belief_state)
            if next_belief == belief_state:
                self.status.config(text=f"Belief Search dừng lại: không thể mở rộng thêm (dead-end toàn cục).")
                return
            belief_state = next_belief
            self.status.config(text=f"Belief Search - bước {step_count}, belief size={len(belief_state)}")
            self.job = self.root.after(self.delay * 2, step)
        # Hàm kiểm tra goal chính xác
        def is_goal_state(self_obj, state, goal_state):
            return len(state) == self_obj.n and all(self_obj.is_safe(r, state[r], state[:r]) for r in range(self_obj.n))
        # gắn hàm kiểm tra goal vào self
        self.is_goal_state = is_goal_state.__get__(self, self.__class__)
        step()

root = tk.Tk()
app = NQueensGUI(root)
root.mainloop()
