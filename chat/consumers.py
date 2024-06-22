import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone

class ChatConsumer(WebsocketConsumer):
     def connect(self):
          self.id = self.scope['url_route']['kwargs']['room_id']
          self.room_group_name = 'sala_chat_%s' % self.id
          self.user = self.scope['user']

          print('conexion al room_group_name: ' + self.room_group_name)
          print('conexion al channel_name: ' + self.channel_name)
          async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
          self.accept()

     def disconnect(self, close_code):
          print('se ha desconectado')
          async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
          
     def receive(self, text_data):
          print(f"Message received from user {self.user}")
          try:
               text_data_json = json.loads(text_data)
               message = text_data_json['message']
     #Get id user
               if self.scope['user'].is_authenticated:
                    sender_id = self.scope['user'].id
               else:
                    None
               if sender_id:
                    async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
                         'type': 'chat_message',
                         'message': message,
                         'username': self.user.username,
                         'datetime': timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M'),
                         'sender_id': sender_id
                    })
               
                    print(f"Message sent to group {self.room_group_name}")
               else:
                    print('Usuario no conectado')    

          except json.JSONDecodeError as e:
               print('Error al decodificar JSON: ', e)
          except KeyError as e:
               print('Clave faltante en el json: ', e)
          except Exception as e:
               print('Error desconocido: ', e)

     def chat_message(self, event):
          message = event['message']
          username = event['username']
          datetime = event['datetime']
          sender_id = event['sender_id']

          current_user_id = self.scope['user'].id
          if sender_id != current_user_id:
               self.send(text_data=json.dumps({'message': message, 'username': username, 'datetime': datetime}))