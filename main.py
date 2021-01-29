import json
import os
import random
import sys
import time
import traceback
from decimal import Decimal

import requests
import tweepy
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

for i in range(len(sys.argv)):
    print(sys.argv[i])


def check():
    # ユーザ名とパスワードの確認
    try:
        user_name = str(sys.argv[1])
        user_password = str(sts.argv[2])
    except:
        print("[ Error ] IDとパスワードが確認できませんでした。もう一度入力してください")
        print("IDを入力してください")
        user_name = input()
        print("パスワードを入力してください")
        user_password = str(input())

    print("ID:" + user_name + "\nパスワード:" + user_password + "\nを利用します")
    photo_name = user_name + ".png"
    # 体温設定
    try:
        temp = str(sys.argv[3])
        print("[ Info ] 体温は" + temp + "を使用します(引数より)")
    except:
        temp = str(random.uniform(36.0, 36.7))
        print("[ Info ] 体温は" + temp + "を使用します(乱数生成)")
    return 0


def twisend():
    CK = "XXX"
    CS = "XXX"
    AT = "XXX"
    AS = "XXX"

    # Twitterオブジェクトの生成
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)
    return 0


def chromesend():
    t1 = time.time()
    try:
        print("Starting Chrome...")
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_argument("--headless")
        chrome_option.add_argument("--no-sandbox")
        chrome_option.add_argument("--disable-setuid-sandbox")
        driver = webdriver.Chrome(
            executable_path="/usr/lib/chromium-browser/chromedriver",
            options=chrome_option,
        )

        print("Starting Sending...")
        driver.get("https://www.ysfh.ed.jp/auth/login")
        driver.set_window_size(512, 512)
        driver.find_element(By.ID, "UserUsername").click()
        driver.find_element(By.ID, "UserUsername").send_keys(user_name)
        driver.find_element(By.ID, "UserPassword").send_keys(user_password)
        driver.find_element(By.ID, "UserPassword").send_keys(Keys.ENTER)
        driver.find_element(
            By.CSS_SELECTOR, "#MenuFramesPageMajor21072 > .pull-left"
        ).click()
        driver.find_element(
            By.ID, "RegistrationAnswerE394dc05b7942a637e052a64670ffd770AnswerValue"
        ).click()
        driver.find_element(By.CSS_SELECTOR, ".col-sm-4").click()
        driver.find_element(By.CSS_SELECTOR, ".today").click()
        driver.find_element(
            By.ID, "RegistrationAnswerBbceb1b7d337c58f2e972fbc908f97310AnswerValue"
        ).send_keys(Keys.CONTROL, "a")
        driver.find_element(
            By.ID, "RegistrationAnswerBbceb1b7d337c58f2e972fbc908f97310AnswerValue"
        ).send_keys(Keys.DELETE)
        driver.find_element(
            By.ID, "RegistrationAnswerBbceb1b7d337c58f2e972fbc908f97310AnswerValue"
        ).send_keys(temp)
        driver.find_element(
            By.ID,
            "RegistrationAnswer44b3e23a28d39ea0840898d7b7bc8c590AnswerValueC3056ac26d8d0590690d4c81e11dc1f8登校予定",
        ).click()
        driver.find_element(
            By.ID,
            "RegistrationAnswer44b3e23a28d39ea0840898d7b7bc8c590AnswerValueC3056ac26d8d0590690d4c81e11dc1f8登校予定",
        ).click()
        driver.find_element(By.NAME, "next_").click()
        driver.find_element(By.NAME, "confirm_registration").click()
        print("Saving Screenshot...")
        driver.save_screenshot("screenshot.png")
        driver.find_element(By.LINK_TEXT, "終了").click()

        driver.save_screenshot(photo_name)
        driver.quit()
        print("Posting finished.")
    except:
        print(traceback.format_exc())
        driver.quit()


def fin():
    t2 = time.time()
    elst = t2 - t1
    print("経過時間は", elst)

    text = "体温送信が完了しました\n実行時間は:" + elst + "秒"

    api.update_with_media(filename="./screenshot.png", status=text)

    token = "XXX"
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + token}
    payload = {"message": text}
    files = {"imageFile": open("./screenshot.png", "rb")}
    line_notify = requests.post(url, data=payload, headers=headers, files=files)

    print("終了")


def main():
    check()
    twisend()
    chromesend()


if __name__ == "__main__":
    main()
