

#################################################################### 定数・宣言

import sys
import os
import re

import math

from skimage.measure import compare_ssim
import imutils
import cv2

from time import sleep
from datetime import datetime


#################################################################### メイン処理

#-------------------------------------------------
# 設定ファイルの読み込み
#-------------------------------------------------

# 設定ファイルパス
src_dir = sys.argv[1]
src_key = sys.argv[2]
src_path = src_dir + '/DS_' + src_key + '.txt'

# 設定ファイルを開く
fsrc = open(src_path, 'rt')

# 結果格納フォルダー
result_dir = fsrc.readline().rstrip()

# 取得リスト
list_item = []
for line in fsrc:
	list = line.rstrip()
	list_item.append(list)

# 設定ファイルを閉じる
fsrc.close()


#-------------------------------------------------
# 画面比較
#-------------------------------------------------

# 出力ファイルパス
out_path = src_dir + '/DR_' + src_key + '.txt'

# 出力ファイルを開く
fout = open(out_path, 'wt')

if list_item:
	
	# 全項目を順次処理
	for list in list_item:
		
		# 設定項目（行・ID・更新前画像・更新後画像）を取得する
		row, id, bfile_chrome, afile_chrome, bfile_ie, afile_ie = list.split("\t")
		score_chrome = ''
		dfile_chrome = ''
		bdfile_chrome = ''
		adfile_chrome = ''
		score_ie = ''
		dfile_ie = ''
		bdfile_ie = ''
		adfile_ie = ''
		
		# ブラウザごとに順次処理
		for browser in ['chrome', 'ie']:
			
			# ファイル名
			bfile = ''
			afile = ''
			if browser == 'chrome':
				bfile = bfile_chrome
				afile = afile_chrome
			elif browser == 'ie':
				bfile = bfile_ie
				afile = afile_ie
			
			# ファイルの存在を確認する
			if bfile != '' and afile != '':
				if os.path.isfile(bfile) and os.path.isfile(afile):
					
					# 画像を読み込む
					bimg = cv2.imread(bfile)
					aimg = cv2.imread(afile)
					
					# 両画像のグレースケールをとる
					bgray = cv2.cvtColor(bimg, cv2.COLOR_BGR2GRAY)
					agray = cv2.cvtColor(aimg, cv2.COLOR_BGR2GRAY)
					
					# 両画像を比較してスコアを算出する
					(score, diff) = compare_ssim(bgray, agray, full=True)
					
					# 差分画像のグレースケールを赤にする
					diff = (diff * 255).astype('uint8')
					diff = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
					diff[:,:,0] = diff[:,:,2]
					diff[:,:,1] = diff[:,:,2]
					diff[:,:,2] = 255
					
					# 差分画像を出力する
					dfile = browser + '_' + id + '_Diff.png'
					cv2.imwrite(result_dir + dfile, diff)
					
					# 重ね合わせ用差分を作成する
					pile = diff
					pile[:,:,2] = 255 - diff[:,:,0]
					pile[:,:,:2] = 0
					
					# Beforeに差分を重ねた画像を出力する
					bdiff = bimg
					bdiff[:,:,0] = bdiff[:,:,0] - pile[:,:,2]
					bdiff[:,:,1] = bdiff[:,:,1] - pile[:,:,2]
					bdiff[:,:,2] = bdiff[:,:,2] + (255 - bdiff[:,:,2]) * (pile[:,:,2] / 255)
					bdfile = browser + '_' + id + '_BDiff.png'
					cv2.imwrite(result_dir + bdfile, bdiff)
					
					# Afterに差分を重ねた画像を出力する
					adiff = aimg
					adiff[:,:,0] = adiff[:,:,0] - pile[:,:,2]
					adiff[:,:,1] = adiff[:,:,1] - pile[:,:,2]
					adiff[:,:,2] = adiff[:,:,2] + (255 - adiff[:,:,2]) * (pile[:,:,2] / 255)
					adfile = browser + '_' + id + '_ADiff.png'
					cv2.imwrite(result_dir + adfile, adiff)
					
					# 結果を受け渡す
					if browser == 'chrome':
						score_chrome = str(score)
						dfile_chrome = dfile
						bdfile_chrome = bdfile
						adfile_chrome = adfile
					elif browser == 'ie':
						score_ie = str(score)
						dfile_ie = dfile
						bdfile_ie = bdfile
						adfile_ie = adfile
					
		# 結果を出力する
		dt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		res = "\t".join([row, id, dt, score_chrome, dfile_chrome, bdfile_chrome, adfile_chrome, score_ie, dfile_ie, bdfile_ie, adfile_ie])
		print(res, file = fout)
		


#-------------------------------------------------
# 出力ファイルを閉じる
#-------------------------------------------------

# 終了を出力する
print("END", file = fout)

# 出力ファイルを保存する
fout.close()

