import os
import time
import pandas as pd

# 폴더 경로 설정
folder_path = "/Users/myungjunlee/Desktop/Kopis/"

# 폴더 내 모든 엑셀 파일 불러오기
all_files = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".xlsx"):
            all_files.append(os.path.join(root, file))

def convert_all_excel_to_csv(all_files):
    for excel_file in all_files:
        start_time = time.time()  # 변환 시작 시간 기록
        
        # 같은 이름의 CSV 파일 경로 설정
        csv_file_name = os.path.splitext(excel_file)[0] + ".csv"
        
        # 엑셀 파일을 CSV 파일로 변환
        df = pd.read_excel(excel_file)
        df.to_csv(csv_file_name, index=False)
        
        end_time = time.time()  # 변환 완료 시간 기록
        elapsed_time = end_time - start_time  # 소요 시간 계산
        
        print(f"Converted: {os.path.basename(excel_file)} to {os.path.basename(csv_file_name)} in {elapsed_time:.2f} seconds")

# 모든 엑셀 파일을 CSV 파일로 변환
convert_all_excel_to_csv(all_files)