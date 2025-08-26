bang_diem = {
    1112233: {'Tin ky thuat': 9.2, 'An toan dien': 8.9, 'The duc': 4.1},
    1112244: {'Tin ky thuat': 3.7, 'The duc': 9.0}
}
ma_sv = int(input("Nhập mã sinh viên: "))
if ma_sv not in bang_diem:
    print("Không tìm thấy SV")
else:
    dict_diem = bang_diem[ma_sv]
    mon_no = [mon for mon, diem in dict_diem.items() if diem < 5]
    if mon_no:
        print(f"SV {ma_sv} nợ môn:", mon_no)
    else:
        print(f"SV {ma_sv} không nợ môn nào.")