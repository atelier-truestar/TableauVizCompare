

#################################################################### 定数・宣言

import sys
import os
import re

from selenium import webdriver

from time import sleep
from datetime import datetime

# 対象ブラウザ
KEY_Browser = 'chrome'

# 基本待機秒数
SEC_Wait = 3

# ページロード待機秒数
SEC_WaitLoad = 10


#################################################################### メイン処理

#-------------------------------------------------
# 設定ファイルの読み込み
#-------------------------------------------------

# 設定ファイルパス
src_dir = sys.argv[1]
src_key = sys.argv[2]
src_path = src_dir + '/TS_' + src_key + '.txt'

# 設定ファイルを開く
fsrc = open(src_path, 'rt')

# ダウンロードフォルダー
download_dir = fsrc.readline().rstrip()

# Driverファイル
driver_file = fsrc.readline().rstrip()

# ユーザー名とパスワード
tableau_id = fsrc.readline().rstrip()
tableau_pw = sys.argv[3]

# 画面幅
screen_width = int(fsrc.readline().rstrip())

# 接頭辞(B or A)
prefix = fsrc.readline().rstrip()

# 取得リスト
list_item = []
for line in fsrc:
	list = line.rstrip()
	list_item.append(list)

# 設定ファイルを閉じる
fsrc.close()


#-------------------------------------------------
# 各画面の高さを取得
#-------------------------------------------------

# ブラウザを起動する
options = webdriver.ChromeOptions()
options.add_argument('--window-size=' + str(screen_width) + ',800')
options.add_argument('--disable-infobars')
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path = driver_file, chrome_options = options)
driver.implicitly_wait(SEC_Wait)

# 最初のURL
row, id, url = list_item[0].split("\t")
driver.get(url)
print(url)
sleep(SEC_WaitLoad)

# ログイン
driver.find_element_by_name('username').send_keys(tableau_id)
driver.find_element_by_name('password').send_keys(tableau_pw)
driver.find_element_by_css_selector('button').click()
sleep(SEC_WaitLoad)

list_source = []
if list_item:
	
	# 全項目を順次処理
	for list in list_item:
		
		# 設定項目（行・ID・URL）を取得する
		row, id, url = list.split("\t")
		
		# URLに遷移する
		driver.get(url)
		print(url)
		sleep(SEC_WaitLoad)
		
		# 高さを取得する
		wh = driver.execute_script("return window.innerHeight;")
		vh = driver.execute_script("return top.document.getElementsByTagName('iframe')[0].contentWindow.document.getElementById('main-content').clientHeight;")
		hh = wh - vh
		ph = driver.execute_script("return top.document.getElementsByTagName('iframe')[0].contentWindow.document.getElementById('dashboard-spacer').scrollHeight;")
		if ph < vh:
			ph = vh
		h = hh + ph
		if h < wh:
			h = wh
		
		# データを格納する
		list_source.append("\t".join([row, id, url, str(h)]))
		
# ブラウザを閉じる
driver.close()
driver.quit()


#-------------------------------------------------
# 画面キャプチャー
#-------------------------------------------------

# 出力ファイルパス
out_path = src_dir + '/TR_' + src_key + '.txt'

# 出力ファイルを開く
fout = open(out_path, 'wt')

if list_source:
	
	# 全項目を順次処理
	for list in list_source:
		
		# 設定項目（行・ID・URL・高さ）を取得する
		row, id, url, h = list.split("\t")
		
		# ブラウザを起動する
		options = webdriver.ChromeOptions()
		options.add_argument('--window-size=' + str(screen_width) + ',' + h)
		options.add_argument('--disable-infobars')
		options.add_argument('--headless')
		driver = webdriver.Chrome(executable_path = driver_file, chrome_options = options)
		driver.implicitly_wait(SEC_Wait)
		
		# URLに遷移する
		driver.get(url)
		print(url)
		sleep(SEC_WaitLoad)
		
		# ログイン
		driver.find_element_by_name('username').send_keys(tableau_id)
		driver.find_element_by_name('password').send_keys(tableau_pw)
		driver.find_element_by_css_selector('button').click()
		sleep(SEC_WaitLoad)
		
		# スクリーンショットを保存する
		file = KEY_Browser + '_' + id + '_' + prefix
		driver.save_screenshot(download_dir + file + '.png')
		
		# 結果を出力する
		dt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		res = "\t".join([row, id, file, h, dt])
		print(res, file = fout)
		
		# ブラウザを閉じる
		driver.close()
		driver.quit()
		


#-------------------------------------------------
# 出力ファイルを閉じる
#-------------------------------------------------

# 終了を出力する
print("END", file = fout)

# 出力ファイルを保存する
fout.close()

