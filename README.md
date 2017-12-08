# Stay Plus
工房に滞在している人のみの帯域使用率を監視するためのもの
※現在(2017年12月9日現在)は単純なStayのみの機能しかない

## Environment
- Python3.x

## Install
1. リポジトリのclone
`$ git clone https://github.com/yudaishimanak/Stay-Plus.git`
2. Pythonのパッケージインストール
`$ pip install -r requirements.txt`
3. 必要な外部ソフトウェアのインストール
`$ sudo apt-get install arping mysql-client mysql-server`

## Deploy
1. DBの作成 
`$ mysql -u root -p`
`mysql> create database stay_and_analyzation;`
2. DBのinitialize ※プロジェクトのルートで行ってください
`$ python`
```python
>>> from database import init_db

>>> init_db()
```
3. イメージ保存ディレクトリの作成
`$ sudo mkdir /client_images && sudo chmod 755 /clinet_images`
4. サーバーの起動
`$ python app.py && python stay_status.py`

http://machine_ip:5000/signin
