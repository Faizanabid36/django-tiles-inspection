from django.shortcuts import render, redirect
from django.http import HttpResponse
from inspection.models import EmployeeModel, InspectionModel, ReportModel, UserInspectionModel
from .algorithm import Inspection
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.template import RequestContext

# from django.utils import simplejson
# from django.http import HttpResponse

# Create your views here. Business logics

def home(request):
    return render(request, 'main-content.html', {"emp": EmployeeModel.objects.get(id=request.session['user_id'])})


def start_inspection(request):
    emp = EmployeeModel.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        if request.POST['radio2'] == 'yes':
            generate_report = True

        else:
            generate_report = False
        userInspection = UserInspectionModel(
            user_id=emp,
            type=request.POST['type'],
            generate_report=generate_report
        )
        userInspection.save()

        # request.session['inspection_id'] = detail.id
        request.session['user_inspection_id'] = userInspection.id
        inspection = Inspection(emp, r'inspection/svm.cpickle',
                                userInspection.type, request.session['user_inspection_id'], request)
        inspection.start_inspection()

        # multiple, use filter for that
        debug = InspectionModel.objects.get(id=request.session['user_inspection_id'])
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



def cong(request):
    return render(request, 'Steps/Configure_tiles.html',
                  {"emp": EmployeeModel.objects.get(id=request.session['user_id'])})



def register(request):
    request.session['message'] = ''
    if request.method == 'POST':
        if request.POST['names'] is None or request.POST['email'] is None or request.POST[
            'password'] is None or request.FILES.get('image') is None or request.POST['phone'] is None:
            return render(request, 'Auth/register.html')
        user = EmployeeModel.objects.get(email=request.POST['email'])
        if user:
            request.session['message'] = 'Email already exists'
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


def signin(request):
    if request.session['user_id']:
        return redirect('/dashboard')
    request.session['message'] = ''
    if request.method == 'POST':
        if EmployeeModel.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            data1 = EmployeeModel.objects.get(email=request.POST['email'])
            request.session['user_id'] = data1.id
            return redirect('/cong')
        else:
            request.session['message'] = 'Given Credentials do no match our records'
            return render(request, 'Auth/login-1.html')  # validation if pass username is incorrect
    return render(request, 'Auth/login-1.html')


def reportlist(request):
    li = []
    inspections=[]
    from django.db.models import Sum, Count
    item = UserInspectionModel.objects.all().values().distinct()
    for i in range(len(item)):
        li=[]
        inspection = InspectionModel.objects.filter(user_inspection_id=item[i]['id']).values()
        li.append(inspection.values_list().aggregate(Sum('cracks')))
        li.append(inspection.values_list().aggregate(Sum('pinhole')))
        li.append(inspection.values_list().aggregate(Sum('spot')))
        li.append(inspection.values_list().aggregate(Sum('number_of_defects')))
        li.append({'images_inspected':inspection.values_list().count()})
        li.append({'inspection_type':item[i]['type'].capitalize().replace("_", " ")})
        li.append({'inspection_id':'INSPECT-'+str(item[i]['id'])})
        inspections.append(li)
    return render(request, 'report/reportlist.html', {"reportlist": inspections, "list": li})


def report(request):
    item = UserInspectionModel.objects.filter(id=20).values()
    inspections = InspectionModel.objects.filter(user_inspection_id=item[0]['id']).values()
    # report = ReportModel.objects.filter(id=20).values()
    return render(request, 'report/report.html', {"report": inspections, "inspection": item})


def test(request):
    # inspection_items = UserInspectionModel.objects.all().values().order_by('-id')
    # item = inspection_items[1]
    import json
    from django.core import serializers
    from django.forms.models import model_to_dict
    from pprint import pprint
    inspections={}
    li=[]
    item = UserInspectionModel.objects.all().values().distinct()
    # for i in range(len(item)):
    #
    #     inspections.append(InspectionModel.objects.filter(user_inspection_id=item[i]['id']).values().distinct())
    # li=list(inspections)


    pprint(inspections)
    # li[inspections.user_inspection_id] = (inspections.values_list().aggregate(Sum('cracks')))


    # ins = inspections.values_list('id', flat=True).distinct()
    # inspection_items=serializers.serialize('json', InspectionModel.objects.all())
    # return JsonResponse(json.dumps(item), safe=False)
    from django.core.serializers import serialize
    # data = serializers.serialize('json', item)
    # return HttpResponse(list(item), content_type='application/json')
    # return JsonResponse({"test": list(inspections)})

    return JsonResponse([list(item),list(inspections)], safe=False)

    # return request.json(item)
