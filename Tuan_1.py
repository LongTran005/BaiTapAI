import tkinter as tk
from tkinter import messagebox
# Danh sách câu hỏi
questions = [
    "Bạn có còn nhiều bài tập/chưa làm việc không?",
    "Ngày mai có việc học/làm quan trọng không?",
    "Bạn cảm thấy mệt mỏi hôm nay không?",
    "Bạn đã tập thể dục hoặc vận động hôm nay chưa?",
    "Bạn có hứa với bạn bè sẽ đi chơi không?"
]
answers = []   # Lưu câu trả lời Yes/No
index = 0      # Câu hỏi hiện tại

# Hàm xử lí câu hỏi
def answer(response):
    global index
    answers.append(response)   # Lưu lại câu trả lời
    index += 1                 # Chuyển sang câu hỏi tiếp theo
    if index < len(questions):
        label.config(text = questions[index])   # Cập nhật câu hỏi mới
    else:
        make_decision()                         # Hết câu hỏi thì đưa ra quyết định

# Hàm xử lí các quyết định tương đương với câu trả lời
def make_decision():
    if answers[0] == "Yes" or answers[1] == "Yes":
        decision = "Bạn nên hoàn thành việc học/làm trước"
    elif answers[2] == "Yes":
        decision = "Bạn nên nghỉ ngơi và chăm sóc sức khỏe"
    elif answers[4] == "Yes":
        decision = "Bạn nên đi chơi với bạn bè như đã hứa"
    else:
        decision = "👌 Không có gì gấp, bạn có thể thư giãn hoặc làm điều mình thích"

    # Hiện kết quả
    messagebox.showinfo("Kết quả quyết định", decision)
    root.destroy()

# Giao diện
root = tk.Tk()
root.title("Có nên đi chơi không?")
root.geometry("450x200")

# Hiển thị câu hỏi đầu tiên
label = tk.Label(root, text=questions[index], font=("Arial", 12), wraplength=400)
label.pack(pady=25)

# Khung chứa nút Yes/No
frame = tk.Frame(root)
frame.pack()
btn_yes = tk.Button(frame, text="Yes", width=12, command=lambda: answer("Yes"))
btn_no = tk.Button(frame, text="No", width=12, command=lambda: answer("No"))
btn_yes.grid(row=0, column=0, padx=15)
btn_no.grid(row=0, column=1, padx=15)
# Chạy ứng dụng
root.mainloop()
