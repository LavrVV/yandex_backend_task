from datetime import datetime
from django.http.response import HttpResponseNotFound, JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from main import models
from dateutil.parser import parse
import json


def courier(request, courier_id):
    if request.method == 'PATCH':
        try:
            courier = models.Courier.objects.get(id=courier_id)
            data = json.loads(request.body)
            courier.update(data)
            res = {}
            res['courier_id'] = courier.id
            res['courier_type'] = courier.courier_type
            regions = [i.id for i in courier.regions.all()]
            res['regions'] = regions
            res['working_hours'] = courier.working_hours.split(' ')
            return JsonResponse(res, status=200, reason='OK')
        except:
            return HttpResponseBadRequest()
    elif request.method == 'GET':
        try:
            res = {}
            courier = models.Courier.objects.get(id=courier_id)
            res['courier_id'] = courier.id
            res['courier_type'] = courier.courier_type
            regions = [i.id for i in courier.regions.all()]
            res['regions'] = regions
            res['working_hours'] = courier.working_hours.split(' ')
            res['rating'] = courier.get_rating()
            res['earnings'] = courier.get_earnings()
            return JsonResponse(res, status=200, reason='OK')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotFound()


def set_couriers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data = data['data']
        ok = []
        notok = []
        for courier in data:
            try:
                c = models.Courier.create(courier)
                ok.append({'id': c.id})
            except:
                notok.append({'id': courier['courier_id']})
        if len(notok) > 0:
            notok = {'validation_error': {'couriers': notok}}
            return JsonResponse(notok, status=400, reason='Bad Request')
        else:
            return JsonResponse({'couriers': ok}, status=201, reason='Created')
    else:
        return HttpResponseNotFound()


def assign_orders(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            courier = models.Courier.objects.get(id=data['courier_id'])
            res, assign_time = courier.assign_orders()
            if len(res) != 0:
                return JsonResponse({'orders': res, 'assign_time': assign_time}, status=200, reason='OK')
            else:
                return JsonResponse({'orders': res}, status=200, reason='OK')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotFound()


def complete_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order = models.Order.objects.get(id=data['order_id'])
            if order.courier.id != data['courier_id']:
                raise ValueError()
            order.complete(parse(data['complete_time']))
            return JsonResponse({'order_id': data['order_id']}, status=200, reason='OK')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotFound()


def orders(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data = data['data']
        ok = []
        notok = []
        for order in data:
            try:
                o = models.Order.create(order)
                ok.append({'id': o.id})
            except:
                notok.append({'id': order['order_id']})
        if len(notok) > 0:
            notok = {'validation_error': {'orders': notok}}
            return JsonResponse(notok, status=400, reason='Bad Request')
        else:
            return JsonResponse({'orders': ok}, status=201, reason='Created')
    else:
        return HttpResponseNotFound()
