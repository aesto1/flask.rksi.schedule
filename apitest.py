from schedule import db, create_app
from schedule.models import Group
import json
a = create_app().app_context().push()

g = Group.query.all()

j = ['groups', {
                'list': {}
               } 
    ]
i=0
for group in g:
    j[1]['list'][int(i)] = group.name
    i+=1
js = json.dumps(j, ensure_ascii=False)


