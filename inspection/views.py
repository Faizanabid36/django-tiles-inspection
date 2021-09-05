from django.db.models.aggregates import Avg
from django.shortcuts import render, redirect
from django.http import HttpResponse
from inspection.models import EmployeeModel, InspectionModel, ReportModel, UserInspectionModel
from .algorithm import Inspection
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.template import RequestContext
import json,statistics

# from django.utils import simplejson
# from django.http import HttpResponse

# Create your views here. Business logics

def home(request):
    if 'user_id' in request.session:
        return render(request, 'main-content.html', {"emp": EmployeeModel.objects.get(id=request.session['user_id'])})
    return redirect('/signin')

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
        request.session['user_inspection_id'] = userInspection.id
        inspection = Inspection(emp, r'inspection/svm.cpickle',
                                userInspection.type, request.session['user_inspection_id'], request)
        inspection.start_inspection()
        return redirect('inspection/'+ str(request.session['user_inspection_id'])+'/report')


def logout(request):
    request.session.flush()
    return redirect('/signin')

def configuration(request):
    return render(request, 'Steps/Configure_tiles.html',
                  {"emp": EmployeeModel.objects.get(id=request.session['user_id'])})



def register(request):
    request.session['message'] = ''
    if request.method == 'POST':
        if request.POST['names'] is None or request.POST['email'] is None or request.POST[
            'password'] is None or request.FILES.get('image') is None or request.POST['phone'] is None:
            return render(request, 'Auth/register.html')
        user = EmployeeModel.objects.filter(email=request.POST['email'])
        if len(user):
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
    if 'user_id' in request.session:
        return redirect('/dashboard')
    request.session['message'] = ''
    if request.method == 'POST':
        if EmployeeModel.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            data1 = EmployeeModel.objects.get(email=request.POST['email'])
            request.session['user_id'] = data1.id
            return redirect('/dashboard')
        else:
            request.session['message'] = 'Given Credentials do no match our records'
            return render(request, 'Auth/login-1.html')
    return render(request, 'Auth/login-1.html')


def reportlist(request):
    li = []
    inspections=[]
    from django.db.models import Sum, Count
    item = UserInspectionModel.objects.filter(is_completed = True).values().distinct()
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
        li.append({'user_inspection_id': item[i]['id']})
        inspections.append(li)
    # return JsonResponse([list(inspections)], safe=False)
    return render(request, 'report/reportlist.html', {"reportlist": inspections, "list": li})


def report(request, inspection_id):
    item = UserInspectionModel.objects.get(id=inspection_id, is_completed = True)
    inspections = InspectionModel.objects.filter(user_inspection_id=item.id,is_completed = True).values()
    ratio  = total_defects = 0
    for i in range(len(inspections)):
        ratio = inspections[i]['defect_ratio'].replace("\'", "\"")
        #trying to calculate average on print so check prints
        sums=Sum(json.loads(ratio).values())
        # return HttpResponse(json.loads(ratio).values())
        count=Count(json.loads(ratio).values())
        average=sums/count
        # ratiosum=Sum(json.loads(ratio).values())
        inspections[i]['avg_defects'] = average
        total_defects+=inspections[i]['number_of_defects']
    # return JsonResponse([list(item)], safe=False)
    return render(request, 'report/report.html', {"report": inspections, "inspection": item,"ratio":ratio,"total_defects":total_defects})


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
