# gillard
redo backend to nginx/gunicorn/flask/postgres stack

## connect
- nginx
- gunicorn
- flask
- postgres
- pollard

## build
- dev
- staging
- prod

## test
- nosetest

## routes
- /playlist/new/:showid - GET
- /playlist/:id - read-only - GET
- /playlist/:id+:pw - edit mode - GET
- /playlist/:id/add_song - POST
- /playlist/:id/delete_song - POST
- /playlist/:id/delete - POST

- /playlists/:showid - GET

- /song/:id - GET
- /song/:id - POST

- /search/:artist+:title - GET
- /nowPlaying/:format - GET
- /health - GET


## models
- Playlist
  - display_id
  - pw
  - 1 - Many Songs
  - FK showID
  - created at

- Song
  - artist
  - title
  - album
  - label
  - year
  - notes
  - img64px
  - img300px
  - played
  - played_at
  - created_at

- Show
  - showID: String,
  - startDay: Number,
  - startHour: Number,
  - endDay: Number,
  - endHour: Number,


## auth
- dev only auth testing route
- lock playlists through WP access
- on create new playlist, return ID/PW
- store ID/PW in WP
- session mgmt


## pollard
- remove socket.io
- use async calls
- online/offline display
- search reqs thru server
- read-only/edit-mode w/ auth

## backups

## deploy
- staging
- production

## log
- postgres logs
- nginx logs
- gunicorn/flask logs

## monitor
- smoke testing
- non-destructive functional tests

## debug
- log tailing at first
- pdb prompt in dev container - ideal
