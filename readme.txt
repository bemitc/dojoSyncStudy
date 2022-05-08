- download from github or just clone repo with git clone https://github.com/bemitc/dojoSyncStudy.git

- install requirements with pip install -r requirements.txt

- create OAuth token with https://lichess.org/account/oauth/token/create and enable private lichess studies
  this has to be done on the account that owns the studies

- create a .env file somewhere along the path which contains the following:

LICHESS_AUTH="<OAuth token here>"
STUDY_DB_PATH="<path to database -- /Users/brian/dojo_work/dojoStudyInterface/studies.db for example>

- delete studies.db if you're going to store your database in the same location (it has some sample data
  I used in testing)

- the updatestudies.py tool needs to be run periodically. You provide the lichess study IDs on the command
  line (can be multiple) and the pgns are stored in the database. You can run it via cron -- remember to
  cd to the directory so the .env can easily be found (cd dir;./updatestudies.py studyid1 studyid2 etc).
  I'd recommend updating every hour or so, or maybe once a day if you want. Whichever.

- In the service directory you can start the api server with something like FLASK_APP=pgn_service.py flask run -h 0.0.0.0 for testing.
  It's not ideal to generally use flask's built in web server for production, but considering the relatively small user
  base, it's probably okay. Gunicorn might be a good choice for production, but this URL might be helpful for making a
  decision:

  https://flask.palletsprojects.com/en/2.1.x/deploying/wsgi-standalone/
  
