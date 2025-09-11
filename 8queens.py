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

        f = ttk.Frame(root)
        f.pack(side="bottom", fill="x", pady=5)
        ttk.Button(f, text="Random Goal", command=self.new_goal).pack(side="left", padx=5)
        ttk.Button(f, text="BFS", command=self.run_bfs).pack(side="left", padx=5)
        ttk.Button(f, text="BFS(2)", command=self.run_bfs2).pack(side="left", padx=5)
        ttk.Button(f, text="DFS", command=self.run_dfs).pack(side="left", padx=5)
        ttk.Button(f, text="UCS", command=self.run_ucs).pack(side="left", padx=5)
        ttk.Button(f, text="Stop", command=self.stop).pack(side="left", padx=5)

        self.status = ttk.Label(root, text="Ready", relief="sunken", anchor="w")
        self.status.pack(side="bottom", fill="x")

        self.draw_board(self.canvas1)
        self.draw_board(self.canvas2)
        self.show(self.canvas2, self.goal, "purple")

    def draw_board(self, cv):
        cv.delete("all")
        for r in range(self.n):
            for c in range(self.n):
                x0, y0 = c*self.size, r*self.size
                x1, y1 = x0+self.size, y0+self.size
                color = "#eeeed2" if (r+c)%2==0 else "#769656"
                cv.create_rectangle(x0,y0,x1,y1,fill=color,outline=color)

    def show(self, cv, state, color="red"):
        self.draw_board(cv)
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

    def run_bfs(self):
        self.stop()
        q = deque([()])
        goal = self.goal
        def step():
            if not q:
                self.status.config(text="BFS fail")
                return
            s = q.popleft()
            self.show(self.canvas1, s, "blue")
            if s == goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text="BFS found")
                self.print_solution(s)
                return
            r = len(s)
            if r < self.n:
                for c in range(self.n):
                    ok = True
                    for rr,cc in enumerate(s):
                        if cc==c or abs(rr-r)==abs(cc-c): ok=False; break
                    if ok: q.append(s+(c,))
            self.job = self.root.after(self.delay, step)
        step()

    def run_bfs2(self):
        self.stop()
        q = deque([()])
        explored = []
        goal = self.goal
        def step():
            if not q:
                self.status.config(text="BFS2 fail")
                return
            s = q.popleft()
            if s in explored:
                self.job = self.root.after(self.delay, step)
                return
            explored.append(s)
            self.show(self.canvas1, s, "blue")
            if s == goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text="BFS2 found")
                self.print_solution(s)
                return
            r = len(s)
            if r < self.n:
                for c in range(self.n):
                    ok = True
                    for rr,cc in enumerate(s):
                        if cc==c or abs(rr-r)==abs(cc-c): ok=False; break
                    if ok and s+(c,) not in explored and s+(c,) not in q:
                        q.append(s+(c,))
            self.job = self.root.after(self.delay, step)
        step()

    def run_dfs(self):
        self.stop()
        st = [()]
        visited = []
        goal = self.goal
        def step():
            if not st:
                self.status.config(text="DFS fail")
                return
            s = st.pop()
            if s in visited:
                self.job = self.root.after(self.delay, step)
                return
            visited.append(s)
            self.show(self.canvas1, s, "blue")
            if s == goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text="DFS found")
                self.print_solution(s)
                return
            r = len(s)
            if r < self.n:
                for c in reversed(range(self.n)):
                    ok = True
                    for rr,cc in enumerate(s):
                        if cc==c or abs(rr-r)==abs(cc-c): ok=False; break
                    if ok and s+(c,) not in visited and s+(c,) not in st:
                        st.append(s+(c,))
            self.job = self.root.after(self.delay, step)
        step()

    def run_ucs(self):
        self.stop()
        h = [(0,())]
        seen = []
        goal = self.goal
        def step():
            if not h:
                self.status.config(text="UCS fail")
                return
            cost,s = heapq.heappop(h)
            if s in seen:
                self.job = self.root.after(self.delay, step)
                return
            seen.append(s)
            self.show(self.canvas1, s, "blue")
            if s == goal:
                self.show(self.canvas1, s, "green")
                self.status.config(text="UCS found")
                self.print_solution(s)
                return
            r = len(s)
            if r < self.n:
                for c in range(self.n):
                    ok = True
                    for rr,cc in enumerate(s):
                        if cc==c or abs(rr-r)==abs(cc-c): ok=False; break
                    if ok and s+(c,) not in seen:
                        heapq.heappush(h,(cost+1,s+(c,)))
            self.job = self.root.after(self.delay, step)
        step()

root = tk.Tk()
app = NQueensGUI(root)
root.mainloop()