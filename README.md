# TableauVizCompare
Excel + Python + Selenium Tool to capture and compare before and after images from Tableau Server

## 必要環境
* Microsoft Excel
* Python (3.8-)
* Google Chrome
* Microsoft IE 11 (Optional)

## インストール方法

### ファイルの格納
以下のファイルを同じフォルダーに格納する。
* TableauVizCompare.xlsm
* TableauCapture_chrome.py
* TableauCapture_ie.py
* TableauDiffImage.py

### Chrome Driverのダウンロード
https://sites.google.com/a/chromium.org/chromedriver/downloads  
上記サイトから、利用中のChromeと同じバージョンのものをダウンロードして、Excelファイルと同じフォルダーにchromedriver.exeを解凍する。

### IE Driverのダウンロード
https://www.seleniumhq.org/download/  
上記サイトから、32bit版をダウンロードして、Excelファイルと同じフォルダーにIEDriverServer.exeを解凍する。（OSが64bit版でも、32bit版の方を使用すること）

### Pythonのインストール
https://www.python.org/downloads/  
上記サイトから、最新版をダウンロードしてインストールする。  
オプションの「Add to PATH」にチェックを入れておくこと。

### Pythonモジュールのインストール
コマンドプロンプトを管理者で実行し、以下のコマンドを実行する。
```
pip install selenium
pip install opencv-python
pip install imutils
pip install scikit-image
pip install scipy
```
※ ネットワーク環境によっては、--proxy=のオプションスイッチなどを指定する必要がある。
