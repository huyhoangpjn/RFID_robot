# RFID_robot π€
## This robot includes 2 parts:
π₯ The line follower robot

π₯ RFID reader which use to scan info of clothing to store them into database (Format of data from RFID tag: ID_color_name_size_price_mark)

## How to use?
π Clone our repo
### 2 files arduino for Line Follower Robot and RFID reader
π Upload directly to 2 arduino boards

### Folder cotonwate contains source code python to make an interface and manage the database
π First, create database, we'll improve our database in the future. In this project, we use MySQL database to store and manage clothing data. Install MYSQL: https://www.mysql.com/ and you can also use PopSQL to create queries.

π Then, run control.py to connect RFID via bluetooth

### About us:
πWe are 3 members from IMT Atlantique ποΈ, major: Communication Object

πDemo: https://telefab.fr/
