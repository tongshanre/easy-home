#encoding:utf-8
import sqlite3, logging


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


#2. 创建房间表
class Room(object):
    id = -1
    name = ''
    desc = ''
    def __init__(self,params):
        self.id = params[0]
        self.name = params[1]
        self.desc = params[2]


#3. 创建开关表
class Switch(object):
    id = -1
    name = ''
    desc = ''
    device_id = -1
    room_id = -1
    def __init__(self, params):
        self.id = params[0]
        self.name = params[1]
        self.desc = params[2]
        self.device_id = params[3]
        self.room_id = params[4]



#4. 创建设备表
class Device(object):
    id = -1
    name = ''
    code = ''
    status = -1
    value = -1
    desc = ''
    def __init__(self, params):
        self.id = params[0]
        self.name = params[1]
        self.code = params[2]
        self.status = params[3]
        self.value = params[4]
        self.desc = params[5]



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
            users.append(User(u))
        return users

    def query_user_by_np(self, name, password):
        query = self.__get_conn().cursor()
        cursor = query.execute('select * from user where name=? and password=?', (name, password))
        for u in cursor:
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
        conn.execute('delete from switch where room_id =?', (id))
        conn.execute('delete from room where id =?', (id))
        conn.commit()
        conn.close()
        return True

    def update_room(self, id, name, desc):
        conn = self.__get_conn()
        conn.execute('update room set name=?,desc=? where id=?', (name, desc, id))
        conn.commit()
        conn.close()


    def query_rooms(self):
        conn = self.__get_conn()
        cursor  = conn.cursor().execute('select * from room')
        rooms = []
        for room in cursor:
            rooms.append(Room(room))
        conn.close()
        return rooms
    def add_switch(self,name,desc,device_id,room_id):
        conn = self.__get_conn()
        conn.execute('insert into switch (name,desc,device_id,room_id)values(?,?,?,?)',(name,desc,device_id,room_id))
        conn.commit()
        conn.close()
        return True

    def del_switch(self, id):
        conn = self.__get_conn();
        conn.execute('delete from switch where id = ?',(id));
        conn.commit();
        conn.close();
        return True

    def query_switchs_by_roomid(self, roomid):
        conn = self.__get_conn();
        cursor  = conn.cursor().execute('select * from switch where room_id='+str(roomid))
        switchs = []
        for switch in cursor:
            switchs.append(Switch(switch))
        conn.close()
        return switchs

    def query_switch_by_id(self, id):
        conn = self.__get_conn();
        result = None
        cursor = conn.cursor().execute('select * from switch where id='+str(id))
        for switch in cursor:
            result = Switch(switch)
            break;
        conn.close()
        return result


    def add_device(self, name, code,status, value, desc):
        conn = self.__get_conn()
        conn.execute('insert into device (name,code,status,value,desc)values(?,?,?,?,?)', (name, code, status, value, desc))
        conn.commit()
        conn.close()
        return True

    def del_device(self, id):
        conn = self.__get_conn()
        conn.execute('delete from switch where device_id= ?', (id))
        conn.execute('delete from device where id= ?', (id))
        conn.commit()
        conn.close()
        return True

    def update_device(self, id, status, value):
        conn = self.__get_conn()
        conn.execute('update device set status=?,value=? where id =?', (status, value, id))
        conn.commit()
        conn.close()
        return True


    def query_devices(self):
        conn = self.__get_conn()
        cursor = conn.cursor().execute('select * from device')
        devices = []
        for device in cursor:
            devices.append(Device(device))
        conn.close()
        return devices

    def query_device_by_id(self, id):
        conn = self.__get_conn()
        cursor = conn.cursor().execute('select * from device where id='+str(id))
        result = None
        for device in cursor:
            result = Device(device)
        conn.close()
        return result

if __name__ == '__main__':
    conn = sqlite3.connect('easy_home.db')
    conn.execute('''
        create table IF NOT EXISTS user(
            id integer primary key autoincrement,
            name varchar(50) not null,
            password varchear(50) not null,
            type int not null
        )
    ''')
    conn.execute("insert into user (name,password,type)values('admin','admin',1)")
    conn.execute('''
        create table if not exists room(
            id integer primary key autoincrement,
            name varchar(50) not null,
            desc varchar(255) not null
        )
    ''')
    conn.execute('''
        create table if not exists switch(
            id integer primary key autoincrement,
            name varchar(50) not null,
            desc varchar(255) default '',
            device_id int not null,
            room_id int not null
        )
    ''')
    conn.execute('''
        create table if not exists device(
            id integer primary key autoincrement,
            name varchar(50) not null,
            code varchar(50) not null,
            status int not null,
            value  int default '-1',
            desc varchar(255) default ''
        )
    ''')
    conn.commit()
    conn.close()
