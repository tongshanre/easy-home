# -*- coding:utf-8 -*-
import json
from flask import  Flask, render_template, redirect, url_for, request, session
from sqlit_m import SqlUtil
from music_m import MusicUtil
from gpio_m import GPioUtil
import config, os


app = Flask(__name__)
app.config.from_object(config)

gpioUtil = GPioUtil()

sqlUtil = SqlUtil()
musicUtil = MusicUtil(app.config['MUSIC_DIR'], app.config['UPLOAD_FOLDER'])
musicUtil.run_thread()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user')
def user():
    users = sqlUtil.query_users()
    return render_template('user.html', users=users, user_type=session['user_type'])


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


@app.route('/login', methods=['POST'])
def login():
    print request.form
    name = request.form['name']
    password = request.form['password']
    if name == '':
        return '-1'
    if password == '':
        return '-1'
    u = sqlUtil.query_user_by_np(name,password)
    if u == None:
        return '0'
    else:
        session['user_type'] = u.type
        session['user_id'] = u.id
        return '1'

@app.route('/menu')
def menu():
    return render_template('menu.html', user_type=session['user_type'])


@app.route('/switchs')
def switchs():
    rooms = sqlUtil.query_rooms()
    for room in rooms:
        room.devices = sqlUtil.query_devices_by_roomid(room.id)
    return render_template('switchs.html', rooms=rooms, user_type=session['user_type'])


@app.route('/switch_toggle', methods=['POST'])
def switch_toggle():
    d_id = request.form['d_id']
    status = request.form['status']
    device = sqlUtil.query_device_by_id(d_id)
    #更新开关状态
    flag = False;
    if '1' == status:
        flag = True
    GPioUtil.change(device.code, flag)
    #更新数据库数据
    sqlUtil.update_device(device.id, device.name, device.code, status, device.value, device.desc)
    return '1'


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


@app.route('/add_device', methods=['POST'])
def add_device():
    d_name = request.form['d_name']
    d_code = request.form['d_code']
    d_desc = request.form['d_desc']
    d_room_id = request.form['d_room_id']
    flag = sqlUtil.add_device(d_name, d_code, 0, 0, d_desc, d_room_id)
    if flag:
        return '1'
    else:
        return '0'


@app.route('/music')
def music():
    isPlay = musicUtil.is_play()
    volume = musicUtil.get_volume()
    return render_template('music.html', isPlay=isPlay, volume=volume)


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


@app.route('/speaker')
def speaker():
    return render_template('speaker.html', user_id=session['user_id'])


@app.route('/speaker/upload', methods=['POST'])
def upload_wav():
    file = request.files['file']
    if file:
        wav_path = os.path.join(app.config['UPLOAD_FOLDER'], request.form['filename'])
        file.save(wav_path)
        musicUtil.add_record(wav_path)
    return '1'


if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc')