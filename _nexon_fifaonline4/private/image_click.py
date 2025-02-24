# 필요한 라이브러리 설치 (주석 처리된 상태)
# pip install pyautogui opencv-python numpy scikit-image pydirectinput-rgx pygetwindow pywinauto

import os
import time

import cv2
import numpy as np
import pyautogui
import pydirectinput
import pygetwindow as gw
import pywinauto
from skimage.metrics import structural_similarity as ssim


# 프로그램 포커스
def focus_window_partial(partial_title):
    windows = gw.getWindowsWithTitle(partial_title)
    if windows:
        win = windows[0]
        pywinauto.application.Application().connect(handle=win._hWnd).top_window().set_focus()
        win.activate()

# 이미지 비교
def compare_images(image1, image2):
    image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(gray1, gray2, full=True)
    return score

# 비슷한 이미지 찾기
def find_similar_image(template_path, threshold=0.05, save_path="./similar_images", max_wait=5):
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            # 템플릿 이미지 로드
            template = cv2.imread(template_path)
            if template is None:
                raise FileNotFoundError(f"템플릿 이미지를 찾을 수 없습니다: {template_path}")

            # 스크린샷 캡처
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # 이미지 유사도 비교
            similarity = compare_images(template, screenshot)
            
            if similarity > threshold:
                print(f"유사한 이미지를 찾았습니다! 유사도: {similarity:.2f}")
                
                # 템플릿 매칭으로 이미지 위치 찾기
                result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                # 찾은 이미지의 중심점 계산
                top_left = max_loc
                bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
                center_x = (top_left[0] + bottom_right[0]) // 2
                center_y = (top_left[1] + bottom_right[1]) // 2
                
                # 찾은 이미지 주변에 빨간 사각형 그리기
                cv2.rectangle(screenshot, top_left, bottom_right, (0, 0, 255), 2)
                
                # 중심점에 파란색 점 그리기
                cv2.circle(screenshot, (center_x, center_y), 5, (255, 0, 0), -1)
                
                # 저장 경로 확인 및 생성
                os.makedirs(save_path, exist_ok=True)
                
                # 수정된 스크린샷 저장
                save_file = os.path.join(save_path, "test.png")
                cv2.imwrite(save_file, screenshot)
                print(f"결과 이미지가 저장되었습니다: {save_file}")
                
                # 창 포커스 셋팅
                focus_window_partial('FC ONLINE')
                time.sleep(0.5)
                pyautogui.click(center_x, center_y)
                print(f"이미지의 중심점 ({center_x}, {center_y})을 클릭했습니다.")
                
                return True
            else:
                print(f"유사한 이미지를 찾지 못했습니다. 유사도: {similarity:.2f}")
                time.sleep(0.5)  # 0.5초 대기 후 다시 시도

        except Exception as e:
            print(f"오류 발생: {str(e)}")
            time.sleep(0.5)  # 0.5초 대기 후 다시 시도

    # 최대 대기 시간 초과
    raise TimeoutError(f"{max_wait}초 동안 이미지를 찾지 못했습니다.")

if __name__ == "__main__":
    # 사용 예시
    template_path = "./images/next.png"  # 비교할 이미지 경로
    threshold = 0.05  # 유사도 임계값
    save_path = "./similar_images"  # 결과 저장 경로
    
    try:
        find_similar_image(template_path, threshold, save_path)
    except TimeoutError as e:
        print(e)
    except Exception as e:
        print(f"예상치 못한 오류 발생: {str(e)}")