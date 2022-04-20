from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='users/%y.%m/', null=True, blank=True, default='avatar.png')
    university_or_institute = models.CharField(max_length=200, null=True, blank=True)
    discipline = models.CharField(max_length=200, null=True, blank=True)
    batch = models.CharField(max_length=200, null=True, blank=True)
    student_id = models.CharField(max_length=200, null=True, blank=True)
    blood_group = models.CharField(max_length=200, null=True, blank=True)
    contact_number = models.CharField(max_length=200, null=True, blank=True)
    profession = models.CharField(max_length=200, null=True, blank=True)
    hometown = models.CharField(max_length=200, null=True, blank=True)
    current_city = models.CharField(max_length=200, null=True, blank=True)
    fb_link = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Notice(models.Model):
    title = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='notice/%m.%y', null=True, blank=True)
    text = models.CharField(max_length=20000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='notice/%m.%y', null=True, blank=True)
    registration_link = models.URLField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.title} {self.date}'


class Event(models.Model):
    Offline_Event = 'Offline Event'
    Online_Event = 'Online_Event'
    Fund_Raising_Event = 'Fund_Raising_Event'

    Event_TYPE_CHOICES = [
        (Offline_Event, 'Offline Event'),
        (Online_Event, 'Online_Event'),
        (Fund_Raising_Event, 'Fund_Raising_Event'),
    ]
    event_type = models.CharField(max_length=100, choices=Event_TYPE_CHOICES, null=True, blank=True,
                                  default="Offline Event")
    event_location = models.CharField(max_length=500, null=True, blank=True)
    event_platform = models.CharField(max_length=100, null=True, blank=True)
    target_amount = models.IntegerField(default=0.00, null=True, blank=True)
    current_amount = models.IntegerField(default=0.00, null=True, blank=True)
    online_event_link = models.URLField(max_length=1000, null=True, blank=True)
    event_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=False)
    participation_fee = models.CharField(default=0, max_length=100, null=True, blank=True)
    description = models.TextField(max_length=10000)
    facebook_link = models.URLField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='event/%m.%y', null=True, blank=True)
    contact_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.event_name} {self.event_type}'


class About(models.Model):
    President = 'President'
    Vise_President = 'Vise President'
    General_Secretary = 'General Secretary'
    Treasurer = 'Treasurer'
    ACCOUNT_TYPE_CHOICES = [
        (President, 'President'),
        (Vise_President, 'Vise President'),
        (General_Secretary, 'General Secretary'),
        (Treasurer, 'Treasurer'),
    ]
    First = '2020-2021'
    Second = '2021-2022'
    Third = '2022-2023'
    Fourth = '2023-2024'
    session_choice = [
        (First, '2020-2021'),
        (Second, '2021-2022'),
        (Third, '2022-2023'),
        (Fourth, '2023-2024'),
    ]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, choices=ACCOUNT_TYPE_CHOICES, null=True, blank=True)
    active_session = models.CharField(max_length=100, choices=session_choice, null=True, blank=True)
    designation_priority = models.IntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return f'{self.designation} {self.active_session}'


class Settings(models.Model):
    org_full_name = models.CharField(max_length=100, null=True, blank=True)
    org_nickname = models.CharField(max_length=100, null=True, blank=True)
    org_mail = models.EmailField(max_length=254, null=True, blank=True)
    org_institution = models.CharField(max_length=100, null=True, blank=True)
    org_fb_link = models.URLField(max_length=500, null=True, blank=True)
    org_linkedin_link = models.URLField(max_length=500, null=True, blank=True)
    org_youtube_link = models.URLField(max_length=500, null=True, blank=True)
    org_icon_image = models.ImageField(upload_to='settings/%m.%y', null=True, blank=True)
    org_location = models.CharField(max_length=1000, null=True, blank=True)
    org_contact_number = models.CharField(max_length=20, null=True, blank=True)
    org_homepage_description = models.TextField(max_length=20000, null=True, blank=True)
    org_map_location = models.URLField(max_length=5000, null=True, blank=True)
    org_active_session = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.org_nickname


class Carousel(models.Model):
    image = models.ImageField(upload_to='carousel/%y.%m')
    image_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.image_name


class PhotoGallery(models.Model):
    image_caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/%y.%m')
    home_visibility_status = models.BooleanField(default=False)
    category = models.CharField(max_length=100, default='home')
    category_visible = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.image_caption}'


class Fee(models.Model):
    Monthly = 'Monthly'
    Yearly = 'Yearly'
    Occasionally = 'Occasionally'

    fee_choice = [
        (Monthly, 'Monthly'),
        (Yearly, 'Yearly'),
        (Occasionally, 'Occasionally'),

    ]
    January = 'January'
    February = 'February'
    March = 'March'
    April = 'April'
    May = 'May'
    June = 'June'
    July = 'July'
    August = 'August'
    September = 'September'
    October = 'October'
    November = 'November'
    December = 'December'

    month_choice = [
        (January, 'January'),
        (February, 'February'),
        (March, 'March'),
        (April, 'April'),
        (May, 'May'),
        (June, 'June'),
        (July, 'July'),
        (August, 'August'),
        (September, 'September'),
        (October, 'October'),
        (November, 'November'),
        (December, 'December'),

    ]

    y2020 = '2020'
    y2021 = '2021'
    y2022 = '2022'
    y2023 = '2023'
    y2024 = '2024'
    y2025 = '2025'
    y2026 = '2026'
    y2027 = '2027'
    y2028 = '2028'
    y2029 = '2029'
    y2030 = '2030'
    y2031 = '2031'

    Year_choice = [
        (y2020, '2020'),
        (y2021, '2021'),
        (y2022, '2022'),
        (y2023, '2023'),
        (y2024, '2024'),
        (y2025, '2025'),
        (y2026, '2026'),
        (y2027, '2027'),
        (y2028, '2028'),
        (y2029, '2029'),
        (y2030, '2030'),
        (y2031, '2031'),

    ]

    member = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    feetype = models.CharField(max_length=100, choices=fee_choice, default="Monthly")
    amount = models.IntegerField(default="0.00", null=True, blank=True)
    month = models.CharField(max_length=100, choices=month_choice, blank=True, null=True)
    year = models.CharField(max_length=10, choices=Year_choice, blank=True, null=True)
    txnid = models.CharField(max_length=100, null=True)
    recived = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="Pending", null=True, blank=True)
    method = models.CharField(max_length=100, null=True, blank=True)
    depositdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.member} Feetype:{self.feetype}, amount: {self.amount}/- , Fee Month:{self.month} {self.year}'


class Fund(models.Model):
    current_balance = models.IntegerField(default=0.00, null=True, blank=True)

    def __str__(self):
        return f'{self.current_balance}'


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    comment = models.TextField(max_length=50000)
    visited = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.phone} {self.email}'


class Resource(models.Model):
    PDF = 'PDF'
    Video = 'Video'
    Tutorials = 'Tutorials'
    Others = 'Others'
    type_choice = [
        (PDF, 'PDF'),
        (Video, 'Video'),
        (Tutorials, 'Tutorials'),
        (Others, 'Others'),
    ]
    file_name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(upload_to='resource/file/%y.%m', blank=True, null=True)
    file_cover_photo = models.ImageField(upload_to='resource/%y.%m', blank=True, null=True)
    file_type = models.CharField(max_length=100, choices=type_choice)
    file_drive_link = models.URLField(max_length=5000, null=True, blank=True)
    file_youtube_link = models.URLField(max_length=5000, null=True, blank=True)
    file_tag = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.file_name


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50, null=True, blank=True)
    transaction = models.CharField(max_length=500, null=True, blank=True)
    verified = models.BooleanField(default=False)
    method = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.event} {self.user} {self.amount}'

class Designation(models.Model):
    designation = models.CharField(max_length=50)
    priority = models.IntegerField(default=216)

    def __str__(self):
        return f'{self.designation} priority {self.priority}'