# -*- coding:utf-8 -*-
import json
from flask import  Flask, render_template, redirect, url_for, request, make_response, session
from sqlit_m import SqlUtil
from music_m import MusicUtil
#from gpio_m import GPioUtil
import config, os, datetime


app = Flask(__name__)
app.config.from_object(config)

sqlUtil = SqlUtil()
#gpioUtil = GPioUtil()
musicUtil = MusicUtil(app.config['MUSIC_DIR'], app.config['UPLOAD_FOLDER'])
musicUtil.run_thread()


#首页
@app.route('/')
def index():
    return render_template('index.html')


#导航-菜单
@app.route('/to_menu')
def menu():
    return render_template('menu.html', user_type=session['user_type'])


#导航-房间
@app.route('/to_rooms')
def rooms():
    devices = sqlUtil.query_devices();
    statusMap = {};
    codeMap = {};
    for device in devices:
        statusMap[str(device.id)]=device.status
        codeMap[str(device.id)]=device.code
    rooms = sqlUtil.query_rooms()
    for room in rooms:
        room.switchs = sqlUtil.query_switchs_by_roomid(room.id)
        for switch in room.switchs:
            switch.status = statusMap[str(switch.device_id)]
            switch.code = codeMap[str(switch.device_id)]

    return render_template('rooms.html', rooms=rooms,devices=devices, user_type=session['user_type'])


#导航-音乐
@app.route('/to_music')
def music():
    isPlay = musicUtil.is_play()
    volume = musicUtil.get_volume()
    return render_template('music.html', isPlay=isPlay, volume=volume)

#导航-喊话
@app.route('/to_speaker')
def speaker():
    return render_template('speaker.html', user_id=session['user_id'])


#导航-设备
@app.route('/to_devces')
def devices():
    devices = sqlUtil.query_devices();
    return render_template('devices.html', devices=devices)


#导航-用户
@app.route('/to_user')
def user():
    users = sqlUtil.query_users()
    return render_template('user.html', users=users, user_type=session['user_type'])


#功能-登录
@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    password = request.form['password']
    if name == '':
        return '-1'
    if password == '':
        return '-1'
    return login_func(name,password)

def login_func(name, password):
    u = sqlUtil.query_user_by_np(name,password)
    if u == None:
        return make_response('0')
    else:
        response = make_response('1')
        session['user_type'] = u.type
        session['user_id'] = u.id
        outdate=datetime.datetime.today() + datetime.timedelta(days=30)
        response.set_cookie('name',name, expires=outdate)
        response.set_cookie('password',password, expires=outdate)
        return response

#功能-用户
@app.route('/add_user', methods=['POST'])
def add_user():
    u_name = request.form['u_name']
    u_passwd = request.form['u_passwd']
    u_type = request.form['u_type']
    if u_name=='' or u_passwd =='' or u_type=='':
        return '-1'
    flag = sqlUtil.add_user(u_name,u_type,u_passwd)
    if flag:
        return '1'
    else:
        return '0'


@app.route('/del_user', methods=['POST'])
def del_user():
    u_id = request.form['u_id']
    if u_id == '':
        return '-1'
    flag = sqlUtil.delete_user(u_id)
    if flag:
        return '1'
    else:
        return '0'


#功能-房间
@app.route('/add_room', methods=['POST'])
def add_room():
    r_name = request.form['r_name']
    r_desc = request.form['r_desc']
    if r_name == '' or r_desc == '':
        return  '-1'
    flag = sqlUtil.add_room(r_name, r_desc)
    if flag:
        return '1'
    else :
        return '0'


@app.route('/del_room', methods=['POST'])
def del_room():
    r_id = request.form['r_id']
    flag = sqlUtil.del_room(r_id)
    if flag:
        return '1'
    else :
        return '0'


#功能-开关
@app.route('/add_switch', methods=['POST'])
def add_switch():
    s_name = request.form['s_name']
    s_desc = request.form['s_desc']
    s_device_id = request.form['s_device_id']
    s_room_id = request.form['s_room_id']
    flag = sqlUtil.add_switch(s_name,s_desc,s_device_id,s_room_id)
    if flag:
        return '1'
    else :
        return '0'


@app.route('/del_switch', methods=['POST'])
def del_switch():
    s_id = request.form['s_id']
    flag = sqlUtil.del_switch(s_id)
    if flag:
        return '1'
    else :
        return '0'


#功能-设备
@app.route('/add_device', methods=['POST'])
def add_device():
    d_name = request.form['d_name']
    d_code = request.form['d_code']
    d_desc = request.form['d_desc']
    flag = sqlUtil.add_device(d_name, d_code, 0, 0, d_desc)
    if flag:
        return '1'
    else:
        return '0'

@app.route('/del_device', methods=['POST'])
def del_device():
    if sqlUtil.del_device(request.form['d_id']):
        return '1'
    else:
        return '0'


#功能-音乐播放
@app.route('/music/play', methods=['GET', 'POST'])
def music_play():
    musicUtil.play()
    return '1'


@app.route('/music/pause', methods=['GET', 'POST'])
def music_pause():
    musicUtil.pause()
    return '1'


@app.route('/music/prev', methods=['GET', 'POST'])
def music_prev():
    musicUtil.prev()
    return '1'


@app.route('/music/next', methods=['GET', 'POST'])
def music_next():
    musicUtil.nex()
    return '1'


@app.route('/music/set_volume', methods=['GET', 'POST'])
def music_set_volume():
    volume = float(request.form['volume'])
    musicUtil.set_volume(volume)
    return '1'


@app.route('/music/flush_dir', methods=['GET', 'POST'])
def music_flush_dir():
    musicUtil.flush_musics()
    return '1'


#功能-喊话上传接口
@app.route('/speaker/upload', methods=['POST'])
def upload_wav():
    file = request.files['file']
    if file:
        wav_path = os.path.join(app.config['UPLOAD_FOLDER'], request.form['filename'])
        file.save(wav_path)
        musicUtil.add_record(wav_path)
    return '1'


#功能-开关控制接口
@app.route('/switch_toggle', methods=['POST'])
def switch_toggle():
    d_id = request.form['s_id']
    status = request.form['status']
    switch = sqlUtil.query_switch_by_id(d_id)
    device = sqlUtil.query_device_by_id(switch.device_id)
    #更新开关状态
    flag = False;
    if '1' == status:
        flag = True
    #if(device.desc.find('192.168.')>-1):
        #gpioUtil.change_net(device.desc, 80, device.code, status)
    #else:
        #gpioUtil.change(device.code, flag)
    #更新数据库数据
    sqlUtil.update_device(switch.device_id, status, -1)
    return '1'


@app.before_request
def bf_request():
    if request.path.find('static')== -1 and request.path.find('to_') > -1 and session.get('user_type') == None:
        name = request.cookies.get('name')
        password = request.cookies.get('password')
        if name == None or password == None:
            return render_template('index.html')
        else:
            login_func(name,password)


if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc')
    #app.run(host='0.0.0.0')
