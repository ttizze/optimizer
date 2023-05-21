#仮想環境起動
source .venv/bin/activate

deactivate

#開発環境プッシュコマンド
git push staging development:master

#本番環境プッシュコマンド
git pull staging development
git push heroku main

#ローカルでテストする際のコマンド
python3 local_test_main.py

