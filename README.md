# YSFHTempSender
## [YSFH-SINE](https://www.ysfh.ed.jp/)の体温送信を簡略化しました。   
YSFHについては[こちら](https://www.edu.city.yokohama.lg.jp/school/hs/sfh/)をご覧ください。  

---  

### 使い方  

```
git clone https://github.com/YumNumm/TempSender.git
./main.py [体温] <ID> <パスワード>
```
  
 実行時に seleniumやchromewebdriverなどのライブラリが必要です。  
 ここは修正を検討しています。  
 
また、main.pyの6,7行目の[]の中にIDとパスワードを入れることにより実行時の負担を低減することができます。
