from django.shortcuts import render, redirect
from django.http import HttpResponse
from inspection.models import EmployeeModel, InspectionModel

from .algorithm import Inspection


# Create your views here. Business logics

def home(request):
    return render(request, 'main-content.html', {"emp": EmployeeModel.objects.get(id=request.session['user_id'])})


def start_inspection(request):
    # if request.POST['type'] == '':
    #     return redirect('/cong?message=invalid_data')
    emp = EmployeeModel.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        self.send_header("Content-type", "image/jpeg")
        if request.POST['radio2'] == 'yes':
            generate_report = True
        else:
            generate_report = False

        detail = InspectionModel(
            user_id=emp,
            type=request.POST['type'],
            generate_report=generate_report
        )
        detail.save()
        request.session['inspection_id'] = detail.id
        inspection = Inspection(r'inspection/svm.cpickle',
                                detail.type, request.session['inspection_id'])
        inspection.start_inspection()

        debug = InspectionModel.objects.get(id=request.session['inspection_id'])
        if debug.type == 'defects_detection':
            debug_data = [
                {'step': 1, 'title': 'First Frame', 'frame': debug.initial_frame,
                 'status': 200 if debug.initial_frame != 'null' else 404},
                {'step': 2, 'title': 'Frame', 'frame': debug.frame, 'status': 200 if debug.frame != 'null' else 404},
                {'step': 3, 'title': 'Grey Frame', 'frame': debug.grey_frame,
                 'status': 200 if debug.grey_frame != 'null' else 404},
                {'step': 4, 'title': 'Difference', 'frame': debug.difference,
                 'status': 200 if debug.difference != 'null' else 404},
                {'step': 5, 'title': 'Edged Image', 'frame': debug.img_edges_b_rotation,
                 'status': 200 if debug.img_edges_b_rotation != 'null' else 404},
                {'step': 6, 'title': 'Dilated Image', 'frame': debug.dilation_b_rotation,
                 'status': 200 if debug.dilation_b_rotation != 'null' else 404},
                {'step': 7, 'title': 'Rotated Image', 'frame': debug.rotated_image,
                 'status': 200 if debug.rotated_image != 'null' else 404},
                {'step': 8, 'title': 'Edged Image', 'frame': debug.img_edges_a_rotation,
                 'status': 200 if debug.img_edges_a_rotation != 'null' else 404},
                {'step': 9, 'title': 'Cropped Image', 'frame': debug.cropped_image,
                 'status': 200 if debug.cropped_image != 'null' else 404},
                {'step': 10, 'title': 'Grey Cropped', 'frame': debug.grey_cropped_image,
                 'status': 200 if debug.grey_cropped_image != 'null' else 404},
                {'step': 11, 'title': 'Blur Cropped', 'frame': debug.blurred_cropped_image,
                 'status': 200 if debug.blurred_cropped_image != 'null' else 404},
                {'step': 12, 'title': 'Enhanced Image', 'frame': debug.enhanced_image,
                 'status': 200 if debug.enhanced_image != 'null' else 404},
                {'step': 13, 'title': 'Binary Cropped', 'frame': debug.binary_cropped,
                 'status': 200 if debug.binary_cropped != 'null' else 404},
                {'step': 14, 'title': 'Morphed Cropped', 'frame': debug.morphed_cropped,
                 'status': 200 if debug.morphed_cropped != 'null' else 404},
                {'step': 15, 'title': 'Output', 'frame': debug.defected_image,
                 'status': 200 if debug.defected_image != 'null' else 404},
            ]
        else:
            debug_data = [
                {'step': 1, 'title': 'First Frame', 'frame': debug.initial_frame,
                 'status': 200 if debug.initial_frame != 'null' else 404},
                {'step': 2, 'title': 'Frame', 'frame': debug.frame, 'status': 200 if debug.frame != 'null' else 404},
                {'step': 3, 'title': 'Grey Frame', 'frame': debug.grey_frame,
                 'status': 200 if debug.grey_frame != 'null' else 404},
                {'step': 4, 'title': 'Difference', 'frame': debug.difference,
                 'status': 200 if debug.difference != 'null' else 404},
                {'step': 5, 'title': 'Edged Image', 'frame': debug.img_edges_b_rotation,
                 'status': 200 if debug.img_edges_b_rotation != 'null' else 404},
                {'step': 6, 'title': 'Dilated Image', 'frame': debug.dilation_b_rotation,
                 'status': 200 if debug.dilation_b_rotation != 'null' else 404},
                {'step': 7, 'title': 'Rotated Image', 'frame': debug.rotated_image,
                 'status': 200 if debug.rotated_image != 'null' else 404},
                {'step': 8, 'title': 'Edged Image', 'frame': debug.img_edges_a_rotation,
                 'status': 200 if debug.img_edges_a_rotation != 'null' else 404},
                {'step': 9, 'title': 'Cropped Image', 'frame': debug.cropped_image,
                 'status': 200 if debug.cropped_image != 'null' else 404},
                {'step': 10, 'title': 'Grey Cropped', 'frame': debug.grey_cropped_image,
                 'status': 200 if debug.grey_cropped_image != 'null' else 404},
                {'step': 11, 'title': 'Blur Cropped', 'frame': debug.blurred_cropped_image,
                 'status': 200 if debug.blurred_cropped_image != 'null' else 404},
                {'step': 12, 'title': 'Standard Image', 'frame': debug.standard_image,
                 'status': 200 if debug.standard_image != 'null' else 404},
                {'step': 13, 'title': 'Image to Compare', 'frame': debug.image_to_compare,
                 'status': 200 if debug.image_to_compare != 'null' else 404},
                {'step': 14, 'title': 'Binary Image', 'frame': debug.binary_cropped,
                 'status': 200 if debug.binary_cropped != 'null' else 404},
                {'step': 15, 'title': 'Morphed Cropped', 'frame': debug.morphed_cropped,
                 'status': 200 if debug.morphed_cropped != 'null' else 404},
                {'step': 16, 'title': 'Output', 'frame': debug.defected_image,
                 'status': 200 if debug.defected_image != 'null' else 404},
            ]

        context = {"Inspection": InspectionModel.objects.get(id=request.session['inspection_id']),
                   "emp": EmployeeModel.objects.get(id=request.session['user_id']),
                   "array": debug_data,

                   }
        return render(request, 'steps/debugging.html', context)

        # return render(request, 'main-content.html')


def check(request):
    return render(request, 'Auth/login-1.html')


def step2(request):
    # greyscal.grey_image(2)
    return render(request, 'Steps/configure.html', {"emp": EmployeeModel.objects.get(id=request.session['user_id'])}, )


def step3(request):
    return HttpResponse()


def cong(request):
    return render(request, 'Steps/Configure_tiles.html',
                  {"emp": EmployeeModel.objects.get(id=request.session['user_id'])})


def camera(request):
    context = {"Inspection": InspectionModel.objects.get(id=request.session['inspection_id']),
               "emp": EmployeeModel.objects.get(id=request.session['user_id'])}
    return render(request, 'steps/debugging.html', context)


def register(request):
    if request.method == 'POST':
        if request.POST['names'] is None or request.POST['email'] is None or request.POST[
            'password'] is None or request.FILES.get('image') is None or request.POST['phone'] is None:
            return render(request, 'Auth/register.html')
        detail = EmployeeModel(
            name=request.POST['names'],
            email=request.POST['email'],
            password=request.POST['password'],
            image=request.FILES.get('image'),
            phone=request.POST['phone']
        )
        detail.save()
        return render(request, 'Auth/login-1.html')
    else:
        return render(request, 'Auth/register.html')


def sigin(request):
    if request.method == 'POST':
        if EmployeeModel.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            data1 = EmployeeModel.objects.get(email=request.POST['email'])
            # data = serializers.serialize("json", Employee.objects.get(name=request.POST['names']))
            # request.session['name']=data1

            request.session['user_id'] = data1.id

            return redirect('/cong')
        else:
            return redirect('/')  # validation if pass username is incorrect
    return redirect('/')
