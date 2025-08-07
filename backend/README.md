My server for text extraction and cleaning from images for my WhisperConfesssions project

# Before you start

I recommend working with a virtual environment:

```
python -m venv venv
.\venv\Scripts\activate
```

### First, install the necessary dependencies 🖥

```
pip install -r requirement.txt
```

### Then setup .env files:

These files will host the allowed frontend url's for each environment.

They will look like:

```
FRONTEND_URL=http://localhost:3000
FRONTEND_URL_2=http://localhost:3000
FIREBASE_SERVICE_ACCOUNT_JSON_B64={BASE_64_ENCODED_FIREBASE_SERVICE_ACCOUNT_JSON}
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

# OR

### Use Docker (Testing):

Run: `docker compose -f docker-compose.development.yaml up --build` to build and run app in development environment (1st time)
or use `docker compose -f docker-compose.development.yaml` to run if already built

NB: There is a docket cheatsheet in the root `backend` directory
NB: Run: `docker compose -f docker-compose.production.yaml up --build -d` to build and run production app in detached mode (1st time)

### To Build Docker Image and Push to Dockerhub (Deployment):

Run `docker build -t thefirsthero/confessions-fast-api-server:1.0.0 .` (build)
Run `docker push thefirsthero/confessions-fast-api-server1.0.0` (push)

## End-points

The URL http://127.0.0.1:8000/docs will render the interactive documentation of FastAPI, where you can test the endpoints you create, as well as the ones already added by default.

The URL http://127.0.0.1:8000/ will return a json of all confessions currently present in the confessions collection on the firebase firestore.

The URL http://127.0.0.1:8000/addConfession allows you to post a confession to the confessions collection on the firebase firestore.

The URL http://127.0.0.1:8000/upload-images/ allows you to upload images to the server memory using the POST method.

The URL http://127.0.0.1:8000/list-images/ will return a complete list of all images currently on the server.

The URL http://127.0.0.1:8000//process-images/ will run through and process each image uploaded to the server, extracting its text via ocr, cleaning that text and running the text through a profanity filter, and at the end of the processing, return a json file, with the results of the processing.

The URL http://127.0.0.1:8000/delete-images/ allows you to delete all images currently on the server.

The URL http://127.0.0.1:8000/delete-image/{filename} allows you to delete {filename} from the server.

The URL http://127.0.0.1:8000/healthcheck allows you to check the health of the API.

- [Firebase documentation](https://firebase.google.com/docs?authuser=0&hl=es)
- [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/)

### Docker Tutorial Videos that aided in this Project:

Found in`./docker_tutorial`
