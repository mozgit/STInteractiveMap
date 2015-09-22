ST interactive monitor
-------------------

Runing interactive monitor:
- Install mongodb (http://docs.mongodb.org/manual/installation/). If you use mac, you may simply type:
```
brew update
brew install mongodb
```
- Install Flask (http://flask.pocoo.org/docs/0.10/installation/) or, if you already have pip, just type:
```
pip install Flask
pip install flask-script
pip install WTForms
pip install pymongo==2.8 #doesn't work with 3.0
pip install mongoengine #works at 0.8.7
pip install flask_mongoengine
```
- Install ROOT v5:
- 
```
git clone http://root.cern.ch/git/root.git
git tag -l
git checkout -b v5-34-32 v5-34-32
./configure --enable-soversion --all
make -j2
cd bin
source thisroot.sh
```
- Copy repository from github (https://help.github.com/articles/duplicating-a-repository/)
- Run database (you may be asked to create /data/db direcotry):
```
mongod
```
- Run monitor in another terminal:
```
python manage.py runserver
```
- open http://0.0.0.0:5000/index in your browser.

In this version, you may interactively upload files from your browser. It will require username ('admin') and password ('1234').
