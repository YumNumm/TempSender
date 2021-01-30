#!/usr/bin/env python3

# IDとパスワードの設定

# YSFH-SINE ID/Password
UserID = []
UserPW = []


# Twitter API Keys
CK = ""
CS = ""
AT = ""
AS = ""

# LINE Notify API Token
LT = ""

# 体温の乱数生成の幅設定
TempMin = 36.0
TempMax = 36.8


# ライブラリをインポート
import subprocess
import sys

try:

    import json
    import os
    import random
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

except:
    print("importに失敗 インストールします")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    )
    try:
        import json
        import os
        import random
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

    except:
        print("\n\nインストール失敗。pipから自分でインストールしてください。")
        exit(0)
    print("\n\nインストール完了\n\n")


def chromesend(ID, PW, TEMP):
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
        driver.find_element(By.ID, "UserUsername").send_keys(ID)
        driver.find_element(By.ID, "UserPassword").send_keys(PW)
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
        ).send_keys(TEMP)
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

        driver.save_screenshot(PhotoName)
        driver.quit()
        print("Posting finished.")
    except:
        print(traceback.format_exc())
        driver.quit()


try:
    # sys.argvの個数を確認
    count = len(sys.argv)
    print(count)

    if count == 4:
        TempNow = float(sys.argv[1])
        UserID = str(sys.argv[2])
        UserPW = str(sys.argv[3])
        TempSet = 0
        SetUser = 0

    elif count == 3:
        UserID = str(sys.argv[1])
        UserPW = str(sys.argv[2])
        TempSet = 1
        SetUser = 0

    elif count == 2:
        TempNow = float(sys.argv[1])
        TempSet = 0
        SetUser = 1

    elif count == 1:
        TempSet = 1
        SetUser = 1

    else:
        raise ValueError("Error")

except:
    print("引数の順番が正しいか再確認してください。")
    sys.exit()

if len(UserID) != 0:
    SetUser = 0


if TempSet == 1:
    TempNow = str(
        Decimal(str(random.uniform(TempMin, TempMax))).quantize(Decimal("0.1"))
    )
if SetUser == 1:
    UserID = str(input("IDを入力してください : "))
    UserPW = str(input("パスワードを入力してください : "))

# Twitter API KEYが定義されているかを確認
if CK == CS == AT == AS:
    TwiSend = 0
else:
    TwiSend = 1

# LINE API Keyが定義されているかを確認
if LT == "":
    LineSend = 0
else:
    LineSend = 1

if len(UserID) == len(UserPW):
    print()
else:
    print("事前設定したIDとパスワードの個数が正しくありません。\n再確認してください。")
    sys.exit(1)


UserID = UserID.split(",")
UserPW = UserPW.split(",")


# 繰り返し回数判定
for i in range(len(UserID)):
    ID = UserID[i]
    PW = UserPW[i]
    PhotoName = str(UserID[i]) + ".png"
    t1 = time.time()
    chromesend(ID, PW, TempNow)
