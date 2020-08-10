from django.utils import timezone
from users.models import Subject
subs = ["Enf", "Mat"]
now = timezone.now()
m = Subject(name = "sddf", date_created=now)
m.save()

# for s in subs:
#     print(m)
#     m = Subject(name = s, date_created=now)
#     m.save()