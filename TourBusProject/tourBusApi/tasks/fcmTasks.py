from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice

def sendTest():
    message = Message(
        notification= Notification(title="title", body="text"),
        # data={
        #     "Nick" : "Mario",
        #     "body" : "great match!",
        #     "Room" : "PortugalVSDenmark"
        # }
    )
    devices = FCMDevice.objects.all()
    devices.send_message(message)

def sendFcmInquiry():
    message = Message(
        notification= Notification(title="新需求單來囉！", body="回 app 查看~"),
    )
    devices = FCMDevice.objects.all()
    for device in devices:
        print('here')
        try:
            if device.user.isOwner:
                print('here 2')
                device.send_message(message)
        except:
            print('error next')