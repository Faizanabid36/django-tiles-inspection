from django.db import models


class EmployeeModel(models.Model):
    # Id_emp = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/', blank=True)
    # image = models.CharField(max_length=200, default='null')
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class ReportModel(models.Model):
    id = models.IntegerField(primary_key=True)
    user_inspection_id = models.IntegerField(default=-1)
    defect_type = models.CharField(max_length=255, default='null')
    number_of_defects = models.IntegerField(default=0)
    defect_ratio = models.FloatField(default=0)
    defect_grade = models.CharField(max_length=255, default='null')
    defected_image = models.CharField(max_length=255, default='null')

    def __str__(self):
        return self.name


# class con_tile(models.Model):
#     con_tile_id= models.IntegerField(primary_key=True)
#     user_id = models.ForeignKey(user, on_delete=models.CASCADE)


class InspectionModel(models.Model):
    user_id = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE)
    user_inspection_id = models.IntegerField(default=-1)
    type = models.CharField(max_length=255, default='null')
    generate_report = models.BooleanField(default=False)
    initial_frame = models.CharField(max_length=255, default='null')
    frame = models.CharField(max_length=255, default='null')
    grey_frame = models.CharField(max_length=255, default='null')
    difference = models.CharField(max_length=255, default='null')
    img_edges_b_rotation = models.CharField(max_length=255, default='null')
    dilation_b_rotation = models.CharField(max_length=255, default='null')
    rotated_image = models.CharField(max_length=255, default='null')
    img_edges_a_rotation = models.CharField(max_length=255, default='null')
    cropped_image = models.CharField(max_length=255, default='null')
    grey_cropped_image = models.CharField(max_length=255, default='null')
    blurred_cropped_image = models.CharField(max_length=255, default='null')
    enhanced_image = models.CharField(max_length=255, default='null')
    standard_image = models.CharField(max_length=255, default='null')
    image_to_compare = models.CharField(max_length=255, default='null')
    binary_cropped = models.CharField(max_length=255, default='null')
    morphed_cropped = models.CharField(max_length=255, default='null')
    defected_image = models.CharField(max_length=255, default='null')
    cracks = models.IntegerField(default=0)
    spot = models.IntegerField(default=0)
    pinhole = models.IntegerField(default=0)
    number_of_defects = models.IntegerField(default=0)
    defect_ratio= models.CharField(max_length=255, default='null')
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.type


class UserInspectionModel(models.Model):
    user_id = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='null')
    # inspection_id=models.ForeignKey(InspectionModel, on_delete=models.CASCADE)
    generate_report = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    report_id = models.ForeignKey(ReportModel, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.type
