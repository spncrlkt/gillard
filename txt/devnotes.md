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
  - returns playlist.display_id
- /playlist/:id - read-only - GET
- /playlist/:id?:show_id+:pw - edit mode - GET
- /playlist/:id/add_song - POST
- /playlist/:id/delete_song - POST
- /playlists/:showid - GET
- /song/:id - POST
- /loadSchedule - post
- /search/:search_term - GET

- /nowPlaying/:format - GET
- /health - GET

- /playlist/:id/delete - POST


## Data Model

In a nutshell for each Show, there's 1 or more Playlists,
and for each Playlist there's 1 or more Song.

For each song we capture:
artist, title, album, label, release_date, dj provided notes,
a link to an album cover img, whether it was played,
and (start) time it was played.

- Show
  - (Has Many) Playlists
  - display_id
  - startDay
  - startHour
  - endDay
  - endHour

- Playlist
  - (Has Many) Songs
  - display_id
  - password
  - FK showID
  - created at
  - updated at

- Song
  - FK playlist_id
  - artist
  - title
  - album
  - label
  - release_date
  - notes
  - img64px
  - img300px
  - played
  - played_at
  - created_at
  - updated_at


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
