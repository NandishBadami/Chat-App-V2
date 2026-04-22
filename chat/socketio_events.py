import socketio
from datetime import datetime, timezone
from asgiref.sync import sync_to_async

from .models import Friend, Message
from django.contrib.auth.models import User

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

connected_clients = {}

create_friend = sync_to_async(Friend.objects.create, thread_sensitive=True)
create_message = sync_to_async(Message.objects.create, thread_sensitive=True)
get_user = sync_to_async(User.objects.filter, thread_sensitive=True)
get_friend = sync_to_async(Friend.objects.filter, thread_sensitive=True)
update_or_create_message = sync_to_async(Message.objects.update_or_create, thread_sensitive=True)

@sio.event
async def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
async def disconnect(sid, data):
    if sid in connected_clients:
        print('Client Disconnected:', connected_clients[sid], connected_clients[sid]['username'])
        await sio.emit('status', {'status': 'Offline'}, room=[connected_clients[sid]['friend'] + connected_clients[sid]['username'], connected_clients[sid]['username'] + connected_clients[sid]['friend']])
        del connected_clients[sid]

async def save_and_broadcast_message(friend_name, username, message):
    user_qs = await get_user(username=username)
    friend_qs = await get_user(username=friend_name)
    user = await sync_to_async(user_qs.first)()
    friend = await sync_to_async(friend_qs.first)()
    if user and friend:
        friendship_qs = await get_friend(user=user, friend=friend)
        friendship = await sync_to_async(friendship_qs.exists)()
        if not friendship:
            await create_friend(user=user, friend=friend)
            await create_friend(user=friend, friend=user)

        msg = await create_message(sender=user, receiver=friend, text=message)
        """
        for client in connected_clients.items():
            if client[0] != 'homepage':
                if client[1]['username'] == friend_name:
                    await 
        """
        for client in connected_clients.items():
            if client[1]['username'] == friend_name and client[1]['room'] == friend_name + username:
                msg.read = True
                await sync_to_async(msg.save)()
        timestamp = msg.timestamp.isoformat()

        friend_name_first = friend_name + username
        user_name_first = username + friend_name

        await sio.emit('message', {
          'username': username,
          'message': message,
          'timestamp': timestamp,
          'read': msg.read
        }, room=[friend_name_first, user_name_first])

@sio.event
async def join(sid, data):
    username = data.get('username')
    friend_name = data.get('friend')

    if not username or not friend_name:
        return False

    connected_clients[sid] = {'username': username, 'friend': friend_name, 'room': username + friend_name}

    rooms = [friend_name + username, username + friend_name]
    for room in rooms:
        await sio.enter_room(sid, room)

    for client in connected_clients.items():
        if client[1]['username'] == friend_name and client[1]['room'] == friend_name + username:
            await sio.emit('status', {'status': 'Online'}, room=[friend_name + username, username + friend_name])

@sio.event
async def send_message(sid, data):
    if sid not in connected_clients:
        return False
    
    user = connected_clients[sid]
    message = data.get('message')

    if not message:
        return False
    
    await save_and_broadcast_message(
        friend_name=user['friend'],
        username=user['username'],
        message=message
    )