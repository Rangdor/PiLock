#!/usr/bin/env python3

import sqlite3

######################################################
#                  User DB Class                     #
######################################################
class user_DB:


    #Supply the DB name then the "users" Table will be created    
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name +".db")
        self.cursor = self.db.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            name TEXT,
            login TEXT,
            badge TEXT,
            permissions TEXT
            )
            ''')
        self.db.commit()

    #add a user to the DB
    def add(self,name,login,badge,permissions):
        self.cursor = self.db.cursor()       
        if (self.check_user(badge)==False):
            self.cursor.execute('''INSERT INTO users(name, login, badge, permissions)
                          VALUES(?,?,?,?)''', (name, login, badge, permissions))
            self.db.commit()


    #remove a user from the DB
    def remove(self,badge):
        self.cursor = self.db.cursor()
        self.cursor.execute('''DELETE FROM users WHERE badge = ? ''', (badge,))
        self.db.commit()

    #dump the contents of the DB
    def dump(self):
        self.cursor.execute("SELECT * FROM users")
        dump=self.cursor.fetchall()
        for i in dump:
            output=str(i)
            print(output[1:-2])
    

    #check if badge is in DB
    def check_user(self, badge):
        self.cursor = self.db.cursor()
        self.cursor.execute('''SELECT * FROM users WHERE badge = ? ''', (badge,))
        result=self.cursor.fetchall()
        return bool(result)

    #returns users permissions
    #1 admin
    #2 user with gate access
    #3 user without gate access
    def check_permissions(self, badge):
        self.cursor = self.db.cursor()
        self.cursor.execute('''SELECT * FROM users WHERE badge = ? ''', (badge,))
        permissions=str(self.cursor.fetchone())
        return int(permissions[-3:-2])

    #export DB as CSV
    def export(self,filename):
        file= open(filename+".csv","w")
        self.cursor.execute("SELECT * FROM users")
        dump=self.cursor.fetchall()
        for i in dump:
            output=str(i)
            file.write(output[1:-1]+'\n')

    #get name of badge holder
    def get_name(self,badge):
        self.cursor = self.db.cursor()
        self.cursor.execute('''SELECT * FROM users WHERE badge = ? ''', (badge,))
        data = str(self.cursor.fetchone())
        data = data[1:-1]
        data = data.split(",")
        return data[1][2:-1]
            
    #close the DB
    def close(self):
        self.db.close()

        


######################################################
#                  Gate Log DB Class                 #
######################################################
class log_DB:


    #Supply the DB name then the "users" Table will be created    
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name +".db")
        self.cursor = self.db.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS GateLog(
            id INTEGER PRIMARY KEY,
            dateTime TEXT,
            name TEXT,
            duration TEXT
            )
            ''')
        self.db.commit()

    #add a log to the DB
    def add(self,dateTime,name,duration):
        self.cursor = self.db.cursor()
        self.cursor.execute('''INSERT INTO GateLog(dateTime, name, duration)
                      VALUES(?,?,?)''', (dateTime, name, duration))
        self.db.commit()

    #dump the contents of the DB
    def dump(self):
        self.cursor.execute("SELECT * FROM GateLog")
        dump=self.cursor.fetchall()
        for i in dump:
            print(i)
            
    #close the DB
    def close(self):
        self.db.close()

    #export DB as CSV
    def export(self,filename):
        file= open(filename+".csv","w")
        self.cursor.execute("SELECT * FROM GateLog")
        dump=self.cursor.fetchall()
        for i in dump:
            output=str(i)
            file.write(output[1:-1]+'\n')
        
