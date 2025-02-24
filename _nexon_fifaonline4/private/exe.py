# 권한 



import os
import subprocess
import sys


def run_executable(SVC_NAME,file_path):
    try:
        # 파일이 존재하는지 확인
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

        # 파일이 실행 가능한지 확인
        if not os.access(file_path, os.X_OK):
            raise PermissionError(f"파일에 실행 권한이 없습니다: {file_path}")

        # subprocess.run()을 사용하여 파일 실행
        result = subprocess.run(file_path, check=True, capture_output=True, text=True)


        print("프로그램이 성공적으로 실행되었습니다.")
        print("출력:", result.stdout)

    except FileNotFoundError as e:
        print(f"오류: {e}")
    except PermissionError as e:
        print(f"오류: {e}")
    except subprocess.CalledProcessError as e:
        print(f"프로그램 실행 중 오류가 발생했습니다. 종료 코드: {e.returncode}")
        print("오류 출력:", e.stderr)
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    # 실행할 파일의 경로 지정
    SVC_NAME = "fczf.exe"
    file_path = "C:\\Nexon\\EA SPORTS(TM) FC ONLINE\\fczf.exe"
    run_executable(SVC_NAME,file_path)
