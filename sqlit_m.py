# -*- coding:utf-8 -*-
import sqlite3


class Persistence:
    save_file = ''  # 数据文件存放路径

    def __init__(self, save_file):
        self.save_file=save_file
        self.db_init()

    def get_conn(self):
        return sqlite3.connect(self.save_file)

    def db_init(self):
        print('初始化表结构')
        conn = sqlite3.connect(self.save_file)
        conn.execute('''
            create table if not exists ESP_NODE(
                id integer primary key autoincrement,
                uuid varchar(20) not null,
                ip   varchar(20) not null,
                status integer not null
                
            )''')
        conn.execute('''
            create table if not exists ESP_PORT(
                id integer primary key autoincrement,
                port integer not null,
                status integer not null,
                node_id integer not null
            )''')
        conn.execute('''
            create table if not exists ROOM(
                id integer primary key autoincrement,
                name varchar(20) not null
            )''')
        conn.execute('''
            create table if not exists SWITCH(
                id integer primary key autoincrement,
                name varchar(20) not null,
                port_id integer not null,
                room_id integer not null
            )''')
        print('初始化表结构完成')

    def insert_esp_node(self, espNode, ports):
        conn = self.get_conn()
        conn.execute('insert into ESP_NODE (uuid,ip,status)values(?,?,?)', (espNode.uuid, espNode.ip, espNode.status))
        conn.commit()
        node_id = self.query_esp_node_by_uuid(espNode.uuid).id
        params = []
        for port in ports:
            params.append((port, 0, node_id))
        conn.executemany('insert into ESP_PORT (port,status,node_id)values(?,?,?)', params)
        conn.commit()
        conn.close()
        return True

    def delete_esp_node_by_id(self, id):
        conn = self.get_conn()
        conn.execute('delete from SWITCH where port_id in (select id from ESP_PORT where node_id=' + str(id)+')')
        conn.execute('delete from ESP_PORT where node_id =' + str(id))
        conn.execute('delete from ESP_NODE where id = '+str(id))
        conn.commit()
        return True

    def query_esp_nodes(self):
        cursor = self.get_conn().cursor().execute('select * from ESP_NODE')
        nodes = []
        for params in cursor:
            nodes.append(EspNode(params))
        return nodes

    def query_esp_node_by_id(self, node_id):
        cursor = self.get_conn().cursor().execute('select * from ESP_NODE where id = ' + str(node_id))
        for params in cursor:
            return EspNode(params)
        return None

    def query_esp_node_by_uuid(self, uuid):
        cursor = self.get_conn().cursor().execute('select * from ESP_NODE where uuid =  \'' + str(uuid)+'\'')
        for node in cursor:
            return EspNode(node)
        return None

    def query_esp_ports(self):
        cursor = self.get_conn().cursor().execute('select * from ESP_PORT')
        esp_ports = []
        for params in cursor:
            esp_ports.append(EspPort(params))
        return esp_ports

    def update_esp_port_status_by_id(self, id , status):
        conn = self.get_conn()
        conn.execute('update esp_port set status='+ str(status)+ ' where id ='+str(id))
        conn.commit()
        return True

    def query_esp_port_by_id(self, port_id):
        cursor = self.get_conn().cursor().execute('select * from ESP_PORT where id = ' + str(port_id))
        for params in cursor:
            return EspPort(params)
        return None

    def query_esp_ports_by_node_id(self, node_id):
        cursor = self.get_conn().cursor().execute('select * from ESP_PORT where node_id = '+ str(node_id))
        esp_ports = []
        for params in cursor:
            esp_ports.append(EspPort(params))
        return esp_ports

    def insert_room(self, room):
        conn = self.get_conn()
        conn.execute("insert into room (name)values('"+room.name+"')")
        conn.commit()
        return True

    def del_room(self, room_id):
        conn = self.get_conn()
        conn.execute('delete from SWITCH where room_id='+str(room_id))
        conn.execute('delete from ROOM where id = ' + str(room_id))
        conn.commit()
        return True

    def query_rooms(self):
        cursor = self.get_conn().cursor().execute('select * from ROOM')
        rooms = []
        for params in cursor:
            rooms.append(Room(params))
        return  rooms

    def insert_switch(self, switch):
        conn = self.get_conn()
        conn.execute('insert into switch (name, port_id,room_id)values(?,?,?)', (switch.name, switch.port_id, switch.room_id))
        conn.commit()
        conn.close()
        return True

    def delete_switch(self, id):
        conn = self.get_conn()
        conn.execute('delete from SWITCH where id ='+str(id))
        conn.commit()
        return True

    def query_switch_by_room_id(self, room_id):
        cursor = self.get_conn().cursor().execute('select * from switch where room_id='+str(room_id))
        switchs = []
        for params in cursor:
            switchs.append(Switch(params))
        return switchs

    def query_switch_by_id(self, id):
        cursor = self.get_conn().cursor().execute('select * from switch where id='+str(id))
        for switch in cursor:
            return Switch(switch)
        return None


class EspNode:
    id = 0
    uuid = ''
    ip = ''
    status = 0

    def __init__(self, params):
        self.id = params[0]
        self.uuid = params[1]
        self.ip = params[2]
        self.status = params[3]


class EspPort:
    id = 0
    port = 0
    status = 0
    node_id = 0

    def __init__(self, params):
        self.id = params[0]
        self.port = params[1]
        self.status = params[2]
        self.node_id = params[3]


class Room:
    id = 0
    name = ''

    def __init__(self, params):
        self.id = params[0]
        self.name = params[1]


class Switch:
    id = 0
    name = ''
    port_id = 0
    room_id = 0

    def __init__(self, params):
        self.id = params[0]
        self.name = params[1]
        self.port_id = params[2]
        self.room_id = params[3]



if __name__ == '__main__':
    per = Persistence('easy_homev2.db')
    per.db_init()

