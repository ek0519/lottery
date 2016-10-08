# lottery

這是一個產生12組序號，可以依照取得序號大頭照摸彩的小實驗，在產生序號後的30分鐘內可以上傳  
摸彩摸出的人員會出現列表，不在可摸彩的人員之中，不會重複出現。  

2016.10.8 新增功能如下  
1.抽獎頁面可以值些新增產生序號組數，時間重新計算。  
2.產生序號組數空白，按下重新設定，可清空所有資料，時間重新計算。  
3.重新設定時，會同時刪除上傳的照片檔。



## 1. 建立Python3的環境
python3 -m venv any_name  
cd any_name  
source bin/activate

## 2. clone專案
git clone https://github.com/ek0519/lottery.git  project_name  
cd project_name

## 3. 安裝所有使用到的套件 
pip3 install -r requirement.txt

## 4. 啟動網站
./manage.py runserver 0.0.0.0:8080  or any port

