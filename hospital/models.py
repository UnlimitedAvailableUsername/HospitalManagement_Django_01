from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

departments = [
    ('Cardiologist', 'Cardiologist'),
    ('Dermatologists', 'Dermatologists'),
    ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'),
    ('Allergists/Immunologists', 'Allergists/Immunologists'),
    ('Anesthesiologists', 'Anesthesiologists'),
    ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')
]

hospital_choices = [
    ('HAU', 'HAU'),
    ('AUF', 'AUF'),
    ('DHVSU', 'DHVSU'),
    ('OLFU', 'OLFU'),
]


class UserManager(BaseUserManager):
    def createUser(
            self,
            username,
            password=None,
            is_active=True,
            is_staff=False,
            is_admin=False,
    ):
        if not username:
            raise ValueError("Username is a requirement")
        if not password:
            raise ValueError("Password is a requirement")

        user_obj = self.model(username=username)
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)

        return user_obj

    def createStaff(
            self,
            username,
            password=None
    ):
        user = self.createUser(username, password=password, is_staff=True, is_active=True)
        return user

    def create_superuser(self, username, password=None):
        user = self.createUser(username, password=password, is_staff=True, is_admin=True, is_active=True)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    hospital = models.CharField(max_length=10, default='HAU', choices=hospital_choices)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pic/DoctorProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=50, choices=departments, default='Cardiologist')
    status = models.BooleanField(default=False)
    hospital = models.CharField(max_length=10, default='HAU', choices=hospital_choices)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.department)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pic/PatientProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    symptoms = models.CharField(max_length=100, null=False)
    assigned_doctor_id = models.PositiveIntegerField(null=True)
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    hospital = models.CharField(max_length=10, default='HAU', choices=hospital_choices)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name + " (" + self.symptoms + ")"


class MainAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pic/DoctorProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.IntegerField(null=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name


class Appointment(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    doctorId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40, null=True)
    doctorName = models.CharField(max_length=40, null=True)
    appointmentDate = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)


class PatientDischargeDetail(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40)
    assignedDoctorName = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    symptoms = models.CharField(max_length=100, null=True)

    admitDate = models.DateField(null=False)
    releaseDate = models.DateField(null=False)
    daySpent = models.PositiveIntegerField(null=False)

    roomCharge = models.PositiveIntegerField(null=False)
    medicineCost = models.PositiveIntegerField(null=False)
    doctorFee = models.PositiveIntegerField(null=False)
    OtherCharge = models.PositiveIntegerField(null=False)
    total = models.PositiveIntegerField(null=False)

