from celery import shared_task
from .mail_service import send_message
from .models import User, Role, db
from jinja2 import Template
import os


@shared_task(ignore_result=True)
def daily_reminder(to, subject):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, 'test.html')
    users = User.query.filter()
    for user in users:
        print(user)
        with open(html_file_path, 'r') as f:
            template = Template(f.read())
            send_message(user.email, subject,
                         template.render(email=user.email))
    return "OK"

@shared_task(ignore_result=True)
def toremind():
    users = User.query.filter(~User.roles.any(Role.name == 'admin')).all()
    for u in users:
        u.visited=False
    db.session.commit()    

@shared_task(ignore_result=True)
def add_to_last_played(uid,sid):
    user=User.query.filter(User.id==uid).first()
    lp=user.last_played.split(',')   
    lp=[id for id in lp if id]
    if len(lp)>4:
        lp.pop(-1)
    lp=[str(sid)]+lp
    lp=set(lp)
    lp=list(lp)
    user.last_played = ','.join(lp)
    db.session.commit()



