#encoding:utf-8
import sqlite3, logging

conn = sqlite3.connect('easy_home1.db')

#1. 创建用户表
class User(object):
    id = -1
    name = '';
    password = ''
    type = -1
    def __init__(self,params):
        self.id = params[0]
        self.name = params[1]
        self.password = params[2]
        self.type = params[3]

conn.execute('create table IF NOT EXISTS user(id integer primary key autoincrement,name varchar(50) not null,password varchear(50) not null,type int not null)')
conn.commit()
#2. 创建初始用户
conn.execute("insert into user (name,password,type)values('admin','admin',1)")
#conn.execute("delete from user")
conn.commit()
#3. 创建房间表
class Room(object):
    id = -1
    name = ''
    desc = ''
    def __init__(self,params):
        self.id = params[0]
        self.name = params[1]
        self.desc = params[2]


conn.execute('''
    create table if not exists room(
        id integer primary key autoincrement,
        name varchar(50) not null,
        desc varchar(255) not null
    )
''')
conn.commit()
#4. 创建设备表
class Device(object):
    id = -1
    name = ''
    code = ''
    status = -1
    value = -1
    desc = ''
    room_id = -1
    def __init__(self, params):
        self.id = params[0]
        self.name = params[1]
        self.code = params[2]
        self.status = params[3]
        self.value = params[4]
        self.desc = params[5]
        self.room_id = params[6]


conn.execute('''
    create table if not exists device(
        id integer primary key autoincrement,
        name varchar(50) not null,
        code varchar(50) not null,
        status int not null,
        value  int default '-1',
        desc varchar(255) default '',
        room_id integer not null
    )
''')
conn.commit()
conn.close()

class SqlUtil(object):

    def __get_conn(self):
        return sqlite3.connect('easy_home.db')

    def add_user(self, name, type, password):
        conn = self.__get_conn()
        conn.execute('insert into user (name,type,password)values(?,?,?)', (name, type, password))
        conn.commit()
        conn.close()
        return True

    def update_user(self, id, name, type, desc):
        conn = self.__get_conn()
        conn.execute('update user set name=?,type=?,desc=? where id=?', (name, type, desc, id))
        conn.commit()
        conn.close()
        return True

    def delete_user(self, id):
        try:
            conn = self.__get_conn()
            conn.execute('delete from user where id = '+str(id))
            conn.commit()
            conn.close()
            return True
        except BaseException as e:
            print logging.exception(e)
            return False


    def query_users(self):
        query = self.__get_conn().cursor()
        cursor = query.execute('select * from user')
        users = []
        for u in cursor:
            print u
            users.append(User(u))
        return users

    def query_user_by_np(self, name, password):
        query = self.__get_conn().cursor()
        cursor = query.execute('select * from user where name=? and password=?', (name, password))
        for u in cursor:
            print u
            return User(u)
        return None

    def add_room(self, name, desc):
        conn = self.__get_conn()
        conn.execute('insert into room (name,desc)values(?,?)', (name, desc))
        conn.commit()
        conn.close()
        return True

    def del_room(self, id):
        conn = self.__get_conn()
        conn.execute('delete from room where id =?', (id))
        conn.commit()
        conn.close()

    def update_room(self, id, name, desc):
        conn = self.__get_conn()
        conn.execute('update room set name=?,desc=? where id=?', (name, desc, id))
        conn.commit()
        conn.close()

    def query_room_by_id(self, id):
        conn = self.__get_conn()
        cursor = conn.cursor().execute('select * from room where id=?', (id))
        for room in cursor:
            print room
        conn.close()

    def query_rooms(self):
        conn = self.__get_conn()
        cursor  = conn.cursor().execute('select * from room')
        rooms = []
        for room in cursor:
            print rooms.append(Room(room))
        conn.close()
        return rooms

    def add_device(self, name, code,status, value, desc, room_id):
        conn = self.__get_conn()
        conn.execute('insert into device (name,code,status,value,desc,room_id)values(?,?,?,?,?,?)', (name, code, status, value, desc, room_id))
        conn.commit()
        conn.close()
        return True

    def del_device(self, id):
        conn = self.__get_conn()
        conn.execute('delete from device where id= ?', (id))
        conn.commit()
        conn.close()
        return True

    def update_device(self, id, name, code, status, value, desc):
        conn = self.__get_conn()
        conn.execute('update device set name=?,code=?,status=?,value=?,desc=? where id = ?', (name, code, status, value, desc, id))
        conn.commit()
        conn.close()
        return True

    def query_device_by_id(self, id):
        conn = self.__get_conn()
        cursor  = conn.cursor().execute('select * from device where id=?', (id))
        for device in cursor:
            conn.close()
            return Device(device)
        conn.close()
        return None

    def query_devices_by_roomid(self, room_id):
        conn = self.__get_conn()
        cursor = conn.cursor().execute('select * from device where room_id=?', (str(room_id)))
        devices = []
        for device in cursor:
            print devices.append(Device(device))
        conn.close()
        return devices
