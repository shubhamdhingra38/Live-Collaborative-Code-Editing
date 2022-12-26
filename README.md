# Live Collaborative Code Editing
A web application which uses sockets to enable real-time code sharing, chatting and canvas sketching all at once. 
Live hosted website: https://collab-code-edit.fly.dev/ (deployed using fly.io)

# Screenshot
<img src="https://github.com/shubhamdhingra38/Basic-Chat-App-Django-Channels/blob/master/Screenshots/Screenshot.png"/>

# Setting up Locally (Docker: RECOMMENDED)
1. Download Docker and start Docker engine
2. Register for HackerEarth API v4 (free tier) and copy `CLIENT_SECRET`, paste it in `Dockerfile`
3. In project directory with `Dockerfile`, run `docker build -t collabcode .`
4. Run the docker image using `docker run -p 8000:8000 collabcode`
5. Access application on `localhost:8000`

# Setting up Locally (without Docker)
1. Install Python 3.7
2. Register for HackerEarth API v4 and copy `CLIENT_SECRET`
3. Run `pip install -r requirements.txt`
4. Run `python3 manage.py migrate` to set up your local database tables
5. Run `CLIENT_SECRET=<VALUE COPIED EARLIER> python3 manage.py runserver`
6. Access application on `localhost:8000`
   

# Video Demo
https://youtu.be/Tez2jAOlcM8


# TODO
- [x] Password protection for chat and live code editing
- [x] Canvas screen (to draw) which is shared
- [x] UI improvements (chatroom)
- [x] FIX: New users can't access chat
- [x] Synchronization fixes (check every few seconds maybe)
- [x] Ability to run code
- [ ] Zombie rooms removal (in case server crashes and rooms are still occupied)
- [ ] Resize code window and chat window partition
- [x] FIX: Different canvas sizes cause problems
- [x] Change code to be run in sandbox environment only (or use third party API)
- [ ] Replace SQLite as database
