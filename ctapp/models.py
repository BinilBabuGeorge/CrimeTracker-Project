from django.db import models

# Create your models here.

class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    user_type = models.CharField(max_length=50, null=False)
    status = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'tbl_login'

class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=20, null=False)
    email_id = models.EmailField(max_length=254, null=False)
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    dob=models.DateField(null=True, blank=True)
    address=models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'tbl_user'
class Category(models.Model):
    category_id=models.AutoField(primary_key=True)
    category=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_category'
class State(models.Model):
    state_id=models.AutoField(primary_key=True)
    state=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_state'

class District(models.Model):
    district_id=models.AutoField(primary_key=True)
    state=models.ForeignKey(State, on_delete=models.CASCADE)
    district=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_district'
class PoliceStation(models.Model):
    police_station_id=models.AutoField(primary_key=True)

    login=models.ForeignKey(Login, on_delete=models.CASCADE, null=True)

    district=models.ForeignKey(District, on_delete=models.CASCADE)

    station_name = models.CharField(max_length=255, null=True, blank=True)

    place=models.CharField(max_length=50, null=True)

    address=models.TextField(blank=True, null=True)

    phone_number=models.BigIntegerField(null=True)

    mail_id=models.CharField(max_length=50)

    latitude = models.DecimalField(max_digits=18, decimal_places=15, blank=True, null=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, blank=True, null=True)

    status=models.CharField(max_length=50, default="pending")

    class Meta:
        db_table='tbl_police_station'

    def __str__(self):
        return f"{self.station_name or 'Police Station'} - {self.place or ''}".strip()
class PoliceOfficer(models.Model):

    police_officer_id=models.AutoField(primary_key=True)

    login=models.ForeignKey(Login, on_delete=models.CASCADE,null=True)

    name=models.CharField(max_length=50, null=True)

    police_station=models.ForeignKey(PoliceStation, on_delete=models.CASCADE)

    district=models.ForeignKey(District, on_delete=models.CASCADE)

    place=models.CharField(max_length=50, null=True)

    address=models.TextField(blank=True, null=True)

    phone_number=models.BigIntegerField(null=True)

    mail_id=models.CharField(max_length=50)

    qualification=models.CharField(max_length=50,blank=True, null=True)

    photo=models.CharField(max_length=50,blank=True, null=True)

    proof=models.CharField(max_length=50,blank=True, null=True)

    date_of_birth=models.DateField(blank=True, null=True)

    gender=models.CharField(max_length=50,blank=True, null=True)

    created_at=models.DateTimeField(auto_now_add=True)

    p_type=models.CharField(max_length=50,blank=True, null=True)

    class Meta:
        db_table='tbl_police_officer'

class Crime(models.Model):
    crime_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='user_district')
    police_station = models.ForeignKey(PoliceStation, on_delete=models.CASCADE, null=True, blank=True)
    place = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    complaint_text = models.TextField()
    crime_datetime = models.DateTimeField()
    supporting_document = models.FileField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending')  
    # Example: Pending, Reviewed, Resolved
    police_officer= models.ForeignKey(PoliceOfficer, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=15, blank=True, null=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, blank=True, null=True)

    def has_location(self):
        return self.latitude is not None and self.longitude is not None

    def coordinates_display(self):
        if not self.has_location():
            return "Not set"
        return f"{self.latitude}, {self.longitude}"

    class Meta:
        db_table = 'tbl_crime'

class CrimeUpdates(models.Model):
    crime_updates_id = models.AutoField(primary_key=True)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)
    crime_updates=models.TextField(null=True, blank=True)
    police_officer= models.ForeignKey(PoliceOfficer, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    filedoc=models.CharField(max_length=50,null=True)  
    class Meta:
        db_table = 'tbl_crime_updates'
    
class Feedback(models.Model):
    feedback_id=models.AutoField(primary_key=True)
    feedback=models.CharField(max_length=150)
    user=models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True)
    reply=models.CharField(max_length=50, null=True)
    class Meta:
        db_table='tbl_feedback'

class FIR(models.Model):
    fir_id=models.AutoField(primary_key=True)
    crime_id = models.ForeignKey(Crime, on_delete=models.CASCADE)
    description = models.TextField()
    witness_details = models.TextField()
    evidence_details = models.TextField()

    class Meta:
        db_table = 'tbl_fir'


class ChatRoom(models.Model):
    chat_room_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    police_station = models.ForeignKey(PoliceStation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_chat_room"
        unique_together = ("user", "police_station")
        ordering = ["-updated_at", "-created_at"]


class ChatMessage(models.Model):
    chat_message_id = models.AutoField(primary_key=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender_type = models.CharField(max_length=20)  # "user" | "station"
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = "tbl_chat_message"
        ordering = ["created_at"]


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True, blank=True)
    police_station = models.ForeignKey(PoliceStation, on_delete=models.CASCADE, null=True, blank=True)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tbl_notification"


class PanicAlert(models.Model):
    panic_alert_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=18, decimal_places=15, null=True, blank=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="new")  # new | forwarded | resolved
    police_station = models.ForeignKey(PoliceStation, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "tbl_panic_alert"
