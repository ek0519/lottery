# lottery

這是一個產生12組序號，可以依照取得序號大頭照摸彩的小實驗，在產生序號後的30分鐘內可以上傳  
摸彩摸出的人員會出現列表，不在可摸彩的人員之中，不會重複出現。

## 1. Create Venv
python3 -m venv any_name  
cd any_name  
source bin/activate

## 2. clone
git clone https://github.com/ek0519/lottery.git  project_name  
cd project_name

## 3. pip3 install -r requirement.txt

## 4. runserver
./manage.py runserver 0.0.0.0:8080  or any port

## 5. Create lottery
./manage.py gen_lottery  
將會在資料庫產生12筆連號的8碼序號(00000001-00000012)，在這之前會清光資料庫所有內容
