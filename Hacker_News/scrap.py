from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless=new") # 창없이 가상창에서 실행
    options.add_argument("--window-size=1920,1080") # 가상 창 크기

    service = Service("/Users/songhyolim/PycharmProjects/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://news.ycombinator.com/news")

    return driver

def parsing_only_number_in_comments(comment):
    match = re.search(r"(\d+)", comment)
    return int(match.group(1)) if match else 0

def scrap():
    driver = get_driver()
    # 기사제목
    title_elements = driver.find_elements(By.CLASS_NAME, "titleline") # class 가 여러개있다면 find_elements
    subline_elements = driver.find_elements(By.CLASS_NAME, "subline")

    for idx, (el1, el2) in enumerate(zip(title_elements, subline_elements), 1):
        a_tag = el1.find_element(By.TAG_NAME, "a")
        title_text = a_tag.text # 기사제목 추출
        href = a_tag.get_attribute("href") # 링크추출
        try:
            score = el2.find_element(By.CLASS_NAME, "score").text # 포인트 추출
        except:
            score = "0 points"

        print(f"{idx}. {title_text}")
        print(f"link: {href}")
        print(f"points: {score}")

        comment_links = el2.find_elements(By.TAG_NAME, "a")
        comment_count = None

        for link in comment_links:
            text = link.text.strip()
            # .text: 텍스트 콘텐츠를 그대로 가져와서 [ 댓글 7개 ] 이렇게 공백이 껴 있을 수 있음
            # .strip(): 양쪽 끝의 공백/개행 문자 등을 제거해줌
            if "comment" in text:
                comment_count = parsing_only_number_in_comments(text)
                break # 댓글 링크는 하나만 있으므로 반복 중단

        if comment_count is not None:
            print(f"댓글 수: {comment_count}")
        else:
            print("댓글 수: 0 또는 없음")

scrap()