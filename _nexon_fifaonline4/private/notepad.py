# 비동기
import asyncio
import time
# 시간
from datetime import datetime

# 프로세스 
import psutil
import pytz


def timeNow() :
    return datetime.now(pytz.timezone('Asia/Seoul'))



async def terminate_ps(ps):
    # 모든 실행 중인 프로세스를 순회
    for proc in psutil.process_iter(['name']):
        try:
            # 프로세스 이름이 'notepad.exe'인 경우
            if proc.info['name'].lower() == ps:
                print(f"{ps} 프로세스를 찾았습니다. NAME: {proc.info['name']} PID: {proc.pid} ")
                print("time:", timeNow())
                print("1초 후에 종료됩니다...")
                await asyncio.sleep(1)  # 5초 대기
                print("time:", timeNow())
                # proc.terminate()  # 프로세스 종료
                proc.kill()
                print(f"{ps}가 종료되었습니다.")
                return
        # except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        #     pass
        except psutil.NoSuchProcess:
                print(f"{proc} 프로세스를 찾을 수 없습니다.")
        except psutil.AccessDenied:
                print(f"{proc} 프로세스를 종료할 권한이 없습니다.")
        except Exception as e:
                print(f"오류 발생: {e}")    
    print("실행 중인 Notepad 프로세스를 찾을 수 없습니다.")

if __name__ == "__main__":
#   asyncio.run(terminate_ps('fczf.exe'))
#   asyncio.run(terminate_ps('fclient.exe'))
  asyncio.run(terminate_ps('fclauncher.exe'))
    