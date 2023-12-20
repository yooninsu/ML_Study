import os
from datetime import datetime, timedelta

# 시작 날짜, 종료 날짜 및 폴더 생성 경로 설정
start_date = datetime(2023, 12, 19)  # 예시: 2023년 1월 1일 시작
end_date = datetime(2023, 12, 31)  # 예시: 2023년 12월 31일 종료
path = "C:/Users/yis82/OneDrive/Desktop/모두연"

# 하위 폴더 이름
subfolders = ["UX트랙", "AI트랙", "WEB트랙"]

# 지정된 기간 동안 매일 폴더 생성 및 하위 폴더 생성
current_date = start_date
while current_date <= end_date:
    folder_name = current_date.strftime("%Y-%m-%d")  # 폴더 이름 형식: YYYY-MM-DD
    folder_path = os.path.join(path, folder_name)

    # 메인 폴더 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 하위 폴더 생성
    for subfolder in subfolders:
        subfolder_path = os.path.join(folder_path, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

    current_date += timedelta(days=1)
