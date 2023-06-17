# the-daily-image

### Sqlite import
```
sqlite3 instance/db.sqlite
.mode ascii
.separator "," "\n"
.import --skip 1 data/images.csv images
```