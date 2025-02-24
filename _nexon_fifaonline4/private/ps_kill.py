# 관리자 권한 실행
import ctypes
import sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)

# ps kill
import asyncio

import psutil


async def terminate_ps(ps):
    found = False
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == ps:
            found = True
            try:
                print(f"{ps} 프로세스를 2초뒤 종료합니다. (PID: {proc.pid})")
                await asyncio.sleep(2)
                proc.terminate()
                proc.wait(timeout=3)
                print(f"{ps} (PID: {proc.pid}) 종료 완료.")
            except psutil.NoSuchProcess:
                print(f"{ps} 프로세스를 찾을 수 없습니다.")
            except psutil.AccessDenied:
                print(f"{ps} 프로세스를 종료할 권한이 없습니다.")
            except psutil.TimeoutExpired:
                print(f"{ps} (PID: {proc.pid})를 강제 종료를 시작합니다.")
                proc.kill()
            except Exception as e:
                print(f"오류 발생: {e}")
    
    if not found:
        print(f"{ps} 프로세스를 시스템에서 찾을 수 없습니다.")
    
    print('END')
    return 0

async def main(ps):
    await terminate_ps(ps)

# main
if __name__ == "__main__":
    # process = input("ps를 입력하세요 :")
    # process = 'fczf.exe'
    process = 'Notepad.exe'
    asyncio.run(main(process))