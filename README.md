# the-daily-image

### Sqlite import
```
sqlite3 instance/db.sqlite
.mode ascii
.separator "," "\n"
.import --skip 1 data/images.csv images
```

### BUGS:
* Some tall images are shown way too large e.g. http://127.0.0.1:8000/image/a72c20a0-1e07-40b8-9d44-a8b808572f6f