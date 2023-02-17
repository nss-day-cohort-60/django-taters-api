rm db.sqlite3
rm -rf ./rareapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations rareapi
python3 manage.py migrate rareapi
python3 manage.py loaddata users
python3 manage.py loaddata authors
python3 manage.py loaddata tokens
python3 manage.py loaddata category
python3 manage.py loaddata tags
python3 manage.py loaddata reactions
python3 manage.py loaddata post
python3 manage.py loaddata post_reaction
python3 manage.py loaddata post_tag
python3 manage.py loaddata subscriptions
python3 manage.py loaddata comment
