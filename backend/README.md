# firebase_fastAPI 🚀
Before you start, I recommend working with a virtual environment:
```
python -m venv venv
.\venv\Scripts\activate
```
## REST API with FastAPI (Python) to Firebase Firestore (Google) 🌎
```
git clone https://github.com/rtobart/firebase_fastAPI.git
```

### First, install the necessary dependencies 🖥
```
pip install -r requirement.txt
```

### To use this REST API, you need to download Firebase credentials from your Firebase console 🤓
To do this process:

- Go to Firebase 🌎
- Create a new project 🚀
- Create a Firestore database in production or test mode
- In the project, select > Project Settings > Service accounts > python 🐍
- Select "Generate new private key" 🔑
- Add the generated file to the root of the REST API 📩
- Rename the file to "serviceAccountKey.json" 📄


With this, you can now run your REST API using the command 🖥
```
uvicorn main:app --reload 
```
## End-points

The URL http://127.0.0.1:8000/docs will render the interactive documentation of FastAPI, where you can test the endpoints you create, as well as the ones already added by default.

The URL http://127.0.0.1:8000/addUser allows you to add users using the POST method. The user data structure is defined in the 'models.py' file at the root of the API.

The URL http://127.0.0.1:8000/ will return the complete list of registered users.

The URL http://127.0.0.1:8000/delUser allows you to delete users using the DELETE method. It requires the user's ID to delete.

The URL http://127.0.0.1:8000/modName allows you to modify the user's name. It requires the user's ID.

For more information, please check the official documentation of these technologies:

- [Firebase documentation](https://firebase.google.com/docs?authuser=0&hl=es)
- [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/)