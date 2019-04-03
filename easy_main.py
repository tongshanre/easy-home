# -*- coding:utf-8 -*-
from flask import  Flask, render_template, redirect, url_for, request
from sqlit_m import Persistence, Room, Switch, EspNode
import config, json

app = Flask(__name__)
app.config.from_object(config)
persis = Persistence('easy_homev2.db')


@app.route('/')
def index():
    return render_template('rooms.html')


@app.route('/to_menu')
def menu():
    return render_template('menu.html')


@app.route('/to_rooms')
def rooms():
    port_status = {}
    esp_ports = persis.query_esp_ports()
    for esp_port in esp_ports:
        port_status[esp_port.id] = esp_port.status
    rooms = persis.query_rooms()
    for room in rooms:
        room.switchs = persis.query_switch_by_room_id(room.id)
        for switch in room.switchs:
            switch.status = port_status[switch.port_id]
    return render_template('rooms.html', rooms=rooms)


@app.route('/to_rooms_config')
def rooms_config():
    port_status = {}
    esp_ports = persis.query_esp_ports()
    for esp_port in esp_ports:
        port_status[esp_port.id] = esp_port.status
    rooms = persis.query_rooms()
    for room in rooms:
        room.switchs = persis.query_switch_by_room_id(room.id)
        for switch in room.switchs:
            switch.status = port_status[switch.port_id]
    sel_ports = []
    esp_nodes = persis.query_esp_nodes()
    for esp_node in esp_nodes:
        esp_ports = persis.query_esp_ports_by_node_id(esp_node.id)
        for esp_port in esp_ports:
            sel_ports.append({'node_uuid': esp_node.uuid, 'node_ip': esp_node.ip, 'port_id': esp_port.id, 'port': esp_port.port})
    return render_template('rooms-config.html', rooms=rooms, sel_ports=sel_ports)


@app.route('/to_esp_node')
def esp_nodes():
    esp_nodes = persis.query_esp_nodes()
    for esp_node in esp_nodes:
        esp_node.esp_ports = persis.query_esp_ports_by_node_id(esp_node.id)
    return render_template('esp-node.html', esp_nodes=esp_nodes)


@app.route('/del_esp_node', methods=['POST'])
def del_esp_node():
    node_id = request.form['node_id']
    flag = persis.delete_esp_node_by_id(node_id)
    if flag:
        return '1'
    else:
        return '0'


@app.route('/add_room', methods=['POST'])
def add_room():
    r_name = request.form['r_name']
    if r_name == '':
        return '-1'
    flag = persis.insert_room(Room((0, r_name)))
    if flag:
        return '1'
    else:
        return '0'


@app.route('/del_room', methods=['POST'])
def del_room():
    r_id = request.form['r_id']
    flag = persis.del_room(r_id)
    if flag:
        return '1'
    else:
        return '0'


@app.route('/add_switch', methods=['POST'])
def add_switch():
    switch = Switch([1, 1, 1, 1])
    switch.name = request.form['s_name']
    switch.port_id = request.form['s_port_id']
    switch.room_id = request.form['s_room_id']
    flag = persis.insert_switch(switch)
    if flag:
        return '1'
    else:
        return '0'


@app.route('/del_switch', methods=['POST'])
def del_switch():
    s_id = request.form['s_id']
    flag = persis.delete_switch(s_id)
    if flag:
        return '1'
    else:
        return '0'


@app.route('/port_toggle', methods=['POST'])
def port_toggle():
    esp_port_id = request.form['esp_port_id']
    status = request.form['status']
    esp_port = persis.query_esp_port_by_id(esp_port_id)
    esp_node = persis.query_esp_node_by_id(esp_port.node_id)
    print(esp_node.ip, esp_port.port, status)
    # 2. 设备控制
    # 3. 持久化
    persis.update_esp_port_status_by_id(esp_port.id, status)
    return '1'


@app.route('/switch_toggle', methods=['POST'])
def switch_toggle():
    print(request.form)
    s_id = request.form['s_id']
    status = request.form['status']
    switch = persis.query_switch_by_id(s_id)
    esp_port = persis.query_esp_port_by_id(switch.port_id)
    esp_node = persis.query_esp_node_by_id(esp_port.node_id)
    print(esp_node.ip, esp_port.port, status)
    # 2. 设备控制
    # 3. 持久化
    persis.update_esp_port_status_by_id(esp_port.id, status)
    return '1'


@app.route('/esp_node_register', methods=['POST'])
def esp_node_register():
    info = json.loads(request.form['info'])
    esp_node = persis.query_esp_node_by_uuid(info['UUID'])
    if not esp_node:
        persis.insert_esp_node(EspNode((-1, info['UUID'], info['IP'], 1)), info['PORT'])
    return '1'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
