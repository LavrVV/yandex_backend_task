from datetime import datetime, timezone
import json
from dateutil.parser import parse
from django.test import TestCase
from main import models

def generate_couriers():
    for i in range(1, 20):
        models.Region.objects.get_or_create(id=i)
    courier = models.Courier.objects.create(id=1, courier_type='foot', working_hours='10:20-11:40')
    courier.regions.set([4])
    courier = models.Courier.objects.create(id=2, courier_type='foot', working_hours='11:15-14:20 16:40-17:30')
    courier.regions.set([8, 13])
    courier = models.Courier.objects.create(id=3, courier_type='foot', working_hours='09:10-10:50 14:30-15:10 17:00-18:40')
    courier.regions.set([1, 3, 17])
    courier = models.Courier.objects.create(id=4, courier_type='foot', working_hours='11:35-14:05 09:00-11:00')
    courier.regions.set([3, 6, 13])
    courier = models.Courier.objects.create(id=5, courier_type='bike', working_hours='14:35-17:18')
    courier.regions.set([3, 8, 11])
    courier = models.Courier.objects.create(id=6, courier_type='bike', working_hours='10:05-12:25 14:40-15:50')
    courier.regions.set([2, 8, 16])
    courier = models.Courier.objects.create(id=7, courier_type='bike', working_hours='08:35-09:45 13:00-14:10 15:10-16:10')
    courier.regions.set([3, 7, 15])
    courier = models.Courier.objects.create(id=8, courier_type='car', working_hours='11:30-15:05')#assign oreders
    courier.regions.set([3, 5, 10])
    courier = models.Courier.objects.create(id=9, courier_type='car', working_hours='10:25-15:15 17:00-18:00')
    courier.regions.set([13, 16, 18])
    courier = models.Courier.objects.create(id=10, courier_type='car', working_hours='08:17-09:55 12:00-15:00 17:00-19:00')
    courier.regions.set([4, 7, 15])

def generate_orders():
    for i in range(1, 20):
        models.Region.objects.get_or_create(id=i)
    order = models.Order.objects.create(id=1, weight=5.1, region_id=3, delivery_hours='11:50-16:05')
    order = models.Order.objects.create(id=2, weight=7.1, region_id=1, delivery_hours='09:35-10:50')
    order = models.Order.objects.create(id=3, weight=9.1, region_id=3, delivery_hours='10:35-14:05')
    order = models.Order.objects.create(id=4, weight=11.1, region_id=3, delivery_hours='10:50-16:15')
    order = models.Order.objects.create(id=5, weight=13.1, region_id=4, delivery_hours='12:10-17:05')
    order = models.Order.objects.create(id=6, weight=14.1, region_id=5, delivery_hours='14:00-16:00')
    order = models.Order.objects.create(id=7, weight=15.0, region_id=8, delivery_hours='11:55-14:45')
    order = models.Order.objects.create(id=8, weight=19.1, region_id=5, delivery_hours='17:00-18:00')
    order = models.Order.objects.create(id=9, weight=21.1, region_id=16, delivery_hours='09:00-12:00')
    order = models.Order.objects.create(id=10, weight=23.1, region_id=10, delivery_hours='12:40-14:10')
#8
# Create your tests here.
class CourierModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        generate_couriers()
        generate_orders()
        
    
    def setUp(self):
        '''Run once for every test method to setup clean data.'''
        pass

    def test_create(self):
        json_data = {
        "courier_id": 11, 
        "courier_type": "foot", 
        "regions": [1, 12, 20],
        "working_hours": ["11:35-14:05", "09:00-11:00"]
        }
        courier = models.Courier.create(json_data)
        self.assertEqual(courier.id, 11)
        self.assertEqual(courier.get_maxweight(), 10)
        regions = [i.id for i in courier.regions.all()]
        self.assertEqual(regions, [1, 12, 20])
        self.assertEqual(len(courier.get_working_hours()), 2)
        
        json_data = {
        "courier_id": 11, 
        "courier_type": "foot", 
        "regions": [1, 12, 20],
        "working_hours": ["11:35-14:05", "09:00-11:00"]
        }
        try:
            courier = models.Courier.create(json_data)
            self.assertFalse(True, 'Validation fault: existing id')
        except:
            pass
        
        json_data = {
        "courier_id": -11, 
        "courier_type": "foot", 
        "regions": [1, 12, 20],
        "working_hours": ["11:35-14:05", "09:00-11:00"]
        }
        try:
            courier = models.Courier.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong id value')
        except ValueError as v:
            self.assertEquals(v.args[0], -11)
        
        json_data = {
        "courier_id": '12', 
        "courier_type": "foot", 
        "regions": [1, 12, 20],
        "working_hours": ["11:35-14:05", "09:00-11:00"]
        }
        try:
            courier = models.Courier.create(json_data)
            self.assertFalse(True, 'Validation fault: with wrong id type')
        except ValueError as v:
            self.assertEquals(v.args[0], '12')

        json_data = {
        "courier_id": 12, 
        "courier_type": "fuck you", 
        "regions": [1, 12, 20],
        "working_hours": ["11:35-14:05", "09:00-11:00"]
        }
        try:
            courier = models.Courier.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong courier_type value')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "courier_id": 12, 
        "courier_type": 16, 
        "regions": [1, 12, 20],
        "working_hours": ["11:35-14:05", "09:00-11:00"]
        }
        try:
            courier = models.Courier.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong courier_type type')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "courier_id": 12, 
        "courier_type": "car", 
        "regions": 14,
        "working_hours": ["11:35-14:05", "09:00-11:00"]
        }
        try:
            courier = models.Courier.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong regions type')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)
        
        json_data = {
        "courier_id": 12, 
        "courier_type": "car", 
        "regions": [1, -12, '-20'],
        "working_hours": ["11:35-14:05", "09:00-11:00"]
        }
        try:
            courier = models.Courier.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong regions value')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "courier_id": 12, 
        "courier_type": "car", 
        "regions": [1, 12, 20],
        "working_hours": ["look at this dude", 256]
        }
        try:
            courier = models.Courier.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong working_hours value')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "courier_id": 12, 
        "courier_type": "car", 
        "regions": "[1, 12, 20]",
        "working_hours": [" 11::35 - 14::05 "]
        }
        try:
            courier = models.Courier.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong working_hours format')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "courier_id": 12, 
        "courier_type": "car", 
        "regions": "[1, 12, 20]",
        "working_hours": "11:35-14:05"
        }
        try:
            courier = models.Courier.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong working_hours type')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "courier_id": 12, 
        "courier_type": "car", 
        "regions": [1, 12, 20]
        }
        try:
            courier = models.Courier.create(json_data)
            self.assertFalse(True, 'Validation fault: not enough arguments')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "courier_id": 12, 
        "courier_type": "car", 
        "regions": [1, 12, 20],
        "working_hours": ["11:35-14:05", "09:00-11:00"],
        "some_shit": 322
        }
        try:
            courier = models.Courier.create(json_data)
            self.assertFalse(True, 'Validation fault: unknown arguments')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)
        
        json_data = {
        "courier_id": 12, 
        "courier_type": "car", 
        "regions": "[1, 12, 20]",
        "some_shit": 322
        }
        try:
            courier = models.Courier.create(json_data)
            self.assertFalse(True, 'Validation fault: not enough arguments and exist unknown argument')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

    def test_update(self):
        courier = models.Courier.objects.get(id=4)
        json_data = { 
        "courier_type": "car", 
        }
        courier.update(json_data)
        self.assertEquals(courier.get_maxweight(), 50)
        self.assertEquals(courier.courier_type, 'car')

        json_data = { 
        "regions": [1, 12, 20],
        }
        courier.update(json_data)
        regions = [i.id for i in courier.regions.all()]
        self.assertEquals(regions, [1, 12, 20])
        
        json_data = { 
        "working_hours": ["11:35-14:05", "09:00-11:00"]
        }
        courier.update(json_data)
        self.assertEquals(courier.working_hours, '11:35-14:05 09:00-11:00')
        working_hours = courier.get_working_hours()
        self.assertEquals(working_hours[0].hour_start, 11)
        self.assertEquals(working_hours[0].hour_end, 14)
        self.assertEquals(working_hours[0].minute_start, 35)
        self.assertEquals(working_hours[0].minute_end, 5)
        self.assertEquals(working_hours[1].hour_start, 9)
        self.assertEquals(working_hours[1].hour_end, 11)
        self.assertEquals(working_hours[1].minute_start, 0)
        self.assertEquals(working_hours[1].minute_end, 0)
        self.assertEquals(len(working_hours), 2)
        
        json_data = {
        "courier_type": "foot", 
        "regions": [1, 12, 20],
        "working_hours": ["11:35-14:05", "09:00-11:00"],
        "some_shit": 322
        }
        try:
            courier.update(json_data)
            self.assertFalse(True, 'updated with unknown argument')
        except ValueError as er:
            pass
        
        json_data = {
        "courier_type": "fuck you", 
        }
        try:
            courier.update(json_data)
            self.assertFalse(True, 'updated with wrong courier_type value')
        except ValueError as er:
            pass
        
        json_data = {
        "courier_type": 322
        }
        try:
            courier.update(json_data)
            self.assertFalse(True, 'updated with wrong courier_type type')
        except ValueError as er:
            pass
        
        json_data = {
        "regions": [1, '12', -20]
        }
        try:
            courier.update(json_data)
            self.assertFalse(True, 'updated with wrong regions value')
        except ValueError as er:
            pass
        
        json_data = { 
        "regions": '[1, 12, 20]'
        }
        try:
            courier.update(json_data)
            self.assertFalse(True, 'updated with wrong region type')
        except ValueError as er:
            pass
        
        json_data = {
        "working_hours": "11:35-14:05",
        }
        try:
            courier.update(json_data)
            self.assertFalse(True, 'updated with wrong working_hours type')
        except ValueError as er:
            pass
        
        json_data = {
        "working_hours": ["11::35 - 14::05", "09:00-11:00"],
        }
        try:
            courier.update(json_data)
            self.assertFalse(True, 'updated with wrong working_hours value')
        except ValueError as er:
            pass

    def test_assign(self):
        courier = models.Courier.objects.get(id=8)
        orders, ass_time = courier.assign_orders()
        order_ids = [i['id'] for i in orders]
        self.assertEquals(order_ids, [1, 3, 4, 6])

        courier1 = models.Courier.objects.get(id=5)
        orders, ass_time = courier1.assign_orders()
        order_ids = [i['id'] for i in orders]
        self.assertEquals(order_ids, [7])

        orders, ass_time = courier.assign_orders()
        order_ids = [i['id'] for i in orders]
        self.assertEquals(order_ids, [1, 3, 4, 6])

        order = models.Order.objects.get(id=3)
        dt = datetime.now(tz=timezone.utc)
        dt = dt.replace(hour=11, minute=50)
        order.complete(dt)
        self.assertEquals(order.courier.id, 8)
        self.assertEquals(order.complete_time, dt)

        orders, ass_time = courier.assign_orders()
        order_ids = [i['id'] for i in orders]
        self.assertEquals(order_ids, [1, 4, 6])

        order = models.Order.objects.get(id=1)
        dt = dt.replace(hour=12, minute=20)
        order.complete(dt)
        self.assertEquals(order.courier.id, 8)
        self.assertEquals(order.complete_time, dt)
        order = models.Order.objects.get(id=4)
        dt = dt.replace(hour=12, minute=40)
        order.complete(dt)
        self.assertEquals(order.courier.id, 8)
        self.assertEquals(order.complete_time, dt)
        order = models.Order.objects.get(id=6)
        dt = dt.replace(hour=14, minute=10)
        order.complete(dt)
        self.assertEquals(order.courier.id, 8)
        self.assertEquals(order.complete_time, dt)

        courier = models.Courier.objects.get(id=8)
        orders, ass_time = courier.assign_orders()
        order_ids = [i['id'] for i in orders]
        self.assertEquals(order_ids, [10])


class OrderModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        generate_couriers()
        generate_orders()

    def test_create(self):
        json_data = {
        "order_id": 11,
        "weight": 1,
        "region": 20,
        "delivery_hours": ["09:00-12:00", "16:00-21:30"]
        }
        order = models.Order.create(json_data)
        self.assertEqual(order.id, 11)
        self.assertEqual(order.weight, 1.0)
        self.assertEqual(order.region_id, 20)
        self.assertEqual(len(order.get_delivery_hours()), 2)
        
        json_data = {
        "order_id": 11,
        "weight": 0.01,
        "region": 20,
        "delivery_hours": ["09:00-12:00", "16:00-21:30"]
        }
        try:
            order = models.Order.create(json_data)
            self.assertFalse(True, 'Validation fault: existing id')
        except:
            pass
        
        json_data = {
        "order_id": -11,
        "weight": 0.01,
        "region": 20,
        "delivery_hours": ["09:00-12:00", "16:00-21:30"]
        }
        try:
            order = models.Order.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong id value')
        except ValueError as v:
            self.assertEquals(v.args[0], -11)
        
        json_data = {
        "order_id": '11',
        "weight": 0.01,
        "region": 20,
        "delivery_hours": ["09:00-12:00", "16:00-21:30"]
        }
        try:
            order = models.Order.create(json_data)
            self.assertFalse(True, 'Validation fault: with wrong id type')
        except ValueError as v:
            self.assertEquals(v.args[0], '11')

        json_data = {
        "order_id": 12,
        "weight": 0,
        "region": 20,
        "delivery_hours": ["09:00-12:00", "16:00-21:30"]
        }
        try:
            for i in [0.0, 0.01, 55, -10]:
                json_data['weight'] = i
                order = models.Order.create(json_data)
                self.assertFalse(True, 'Validation fault: wrong weight value')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "order_id": 12,
        "weight": '0.01',
        "region": 20,
        "delivery_hours": ["09:00-12:00", "16:00-21:30"]
        }
        try:
            order = models.Order.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong weight type')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "order_id": 12,
        "weight": 0.01,
        "region": '20',
        "delivery_hours": ["09:00-12:00", "16:00-21:30"]
        }
        try:
            order = models.Order.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong region type')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)
        
        json_data = {
        "order_id": 12,
        "weight": 0.01,
        "region": -20,
        "delivery_hours": ["09:00-12:00", "16:00-21:30"]
        }
        try:
            order = models.Order.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong region value')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "order_id": 12,
        "weight": 0.01,
        "region": 20,
        "delivery_hours": ["look at this dude", 256]
        }
        try:
            order = models.Order.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong delivery_hours value')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "order_id": 12,
        "weight": 0.01,
        "region": 20,
        "delivery_hours": [" 11::35 - 14::05 "]
        }
        try:
            order = models.Order.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong delivery_hours format')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "order_id": 12,
        "weight": 0.01,
        "region": 20,
        "delivery_hours": "11:35-14:05"
        }
        try:
            order = models.Order.create(json_data)
            self.assertFalse(True, 'Validation fault: wrong delivery_hours type')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "order_id": 12,
        "weight": 0.01,
        "region": 20
        }
        try:
            order = models.Order.create(json_data)
            self.assertFalse(True, 'Validation fault: not enough arguments')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

        json_data = {
        "order_id": 12,
        "weight": 0.01,
        "region": 20,
        "delivery_hours": ["09:00-12:00", "16:00-21:30"],
        "some_shit": 322
        }
        try:
            order = models.Order.create(json_data)
            self.assertFalse(True, 'Validation fault: unknown arguments')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)
        
        json_data = {
        "order_id": 12,
        "weight": 0.01,
        "region": 20,
        "some_shit": 322
        }
        try:
            order = models.Order.create(json_data)
            self.assertFalse(True, 'Validation fault: not enough arguments and exist unknown argument')
        except ValueError as v:
            self.assertEquals(v.args[0], 12)

    def test_complete(self):
        courier = models.Courier.objects.get(id=8)
        courier.assign_orders()
        order = models.Order.objects.get(id=1)
        dt = datetime.now(tz=timezone.utc)
        dt = dt.replace(hour=12, minute=20)
        order.complete(dt)
        self.assertEquals(order.courier.id, 8)
        self.assertEquals(order.complete_time, dt)
        order.save()
        dt = dt.replace(hour=12, minute=30)
        order.complete(dt)
        dt = dt.replace(minute=20)
        self.assertEquals(order.courier.id, 8)
        self.assertEquals(order.complete_time, dt)
        

class CourierRequestTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        generate_couriers()
        generate_orders()
    
    def test_get(self):
        courier = models.Courier.objects.get(id=8)
        orders, ass_time1 = courier.assign_orders()
        ass_time1 = parse(ass_time1)
        rating3 = 0
        order = models.Order.objects.get(id=3)#3
        dt = datetime.now(tz=timezone.utc)
        dt1 = dt.replace(hour=11, minute=50)
        order.complete(dt1)
        rating3 += abs((ass_time1 - dt1).total_seconds())
        order = models.Order.objects.get(id=1)#3
        dt2 = dt.replace(hour=12, minute=20)
        order.complete(dt2)
        rating3 += abs((dt1 - dt2).total_seconds())
        order = models.Order.objects.get(id=4)#3
        dt3 = dt.replace(hour=12, minute=40)
        order.complete(dt3)
        rating3 += abs((dt2 - dt3).total_seconds())
        rating3 /= 3.0

        order = models.Order.objects.get(id=6)#5
        dt4 = dt.replace(hour=14, minute=10)
        order.complete(dt4)
        rating5 = abs((dt3 - dt4).total_seconds())

        courier = models.Courier.objects.get(id=8)
        orders, ass_time2 = courier.assign_orders()#10
        ass_time2 = parse(ass_time2)
        order = models.Order.objects.get(id=10)#10
        dt5 = dt.replace(hour=12, minute=50)
        order.complete(dt5)
        rating10 = abs((ass_time2 - dt5).total_seconds())
        rating = min(rating3, rating5, rating10)
        rating = (60*60 - min(rating, 60*60))/(60*60) * 5
        earnings = (500 * 9) * 2
        resp = self.client.get('/couriers/8', content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(resp_data['courier_id'], 8)
        self.assertCountEqual(resp_data['regions'], [3, 5, 10])
        self.assertEquals(resp_data['courier_type'], 'car')
        self.assertEquals(resp_data['earnings'], earnings)
        self.assertEquals(resp_data['rating'], rating)

    def test_patch(self):
        data = {
            "courier_type": "car",
            "regions": [1, 12, 22],
            "working_hours": ["11:35-14:05", "09:00-11:00"]
        }
        resp = self.client.patch('/couriers/1', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertCountEqual(list(resp_data.keys()), ['courier_id', 'regions', 'courier_type', 'working_hours'])
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.reason_phrase, 'OK')
        self.assertEquals(resp_data['courier_id'], 1)
        self.assertCountEqual(resp_data['regions'], [1, 12, 22])
        self.assertEquals(resp_data['courier_type'], 'car')
        self.assertCountEqual(resp_data['working_hours'], ["11:35-14:05", "09:00-11:00"])

        data ={
            "courier_type": "some_shit",
        }
        resp = self.client.patch('/couriers/1', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')

        data = {
            "regions": [1, -12, '22'],
        }
        resp = self.client.patch('/couriers/1', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')

        data = {
            "working_hours": "11:35-14:05"
        }
        resp = self.client.patch('/couriers/1', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')

        data = {
            "working_hours": ["11:35-14:05", " 09 : 00 - 11 : 00"]
        }
        resp = self.client.patch('/couriers/1', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')

        data = {
            "working_hours": ["11:35-14:05", "09:00-11:00"],
            'some_shit': 'lalka'
        }
        resp = self.client.patch('/couriers/1', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')

    def test_other(self):
        data = {
            "courier_type": "car",
            "regions": [1, 12, 22],
            "working_hours": ["11:35-14:05", "09:00-11:00"]
        }
        resp = self.client.post('/couriers/1', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 404)
        resp = self.client.delete('/couriers/1', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 404)


class SetCouriersRequestTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        generate_couriers()
        generate_orders()
    
    def test_post(self):
        data = {
        "data": [        
            {
            "courier_id": 11,
            "courier_type": "foot",
            "regions": [1, 12, 22],
            "working_hours": ["11:35-14:05", "09:00-11:00"]
            },        
            {
            "courier_id": 12,
            "courier_type": "bike",
            "regions": [22],
            "working_hours": ["09:00-18:00"]        
            },       
            {
            "courier_id": 13,
            "courier_type": "car",
            "regions": [12, 22, 23, 33],
            "working_hours": ["09:00-18:00"]       
            }
        ]}
        resp = self.client.post('/couriers', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['couriers'])
        self.assertEquals(resp.status_code, 201)
        self.assertEquals(resp.reason_phrase, 'Created')
        self.assertCountEqual(resp_data['couriers'], [{'id':11}, {'id':12}, {'id':13}])

        data = {
        "data": [        
            {
            "courier_id": 14,
            "courier_type": "shit",
            "regions": [1, 12, 22],
            "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]}
        resp = self.client.post('/couriers', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['validation_error'])
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')
        self.assertCountEqual(resp_data['validation_error']['couriers'], [{'id':14}])

        data = {
        "data": [        
            {
            "courier_id": 14,
            "courier_type": "car",
            "regions": [1, 12, -22],
            "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]}
        resp = self.client.post('/couriers', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['validation_error'])
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')
        self.assertCountEqual(resp_data['validation_error']['couriers'], [{'id':14}])

        data = {
        "data": [        
            {
            "courier_id": 14,
            "courier_type": "car",
            "regions": [1, 12, 22],
            "working_hours": ["11:35 - 14:j5", "09:00-11:00"]
            }
        ]}
        resp = self.client.post('/couriers', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['validation_error'])
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')
        self.assertCountEqual(resp_data['validation_error']['couriers'], [{'id':14}])

        data = {
        "data": [        
            {
            "courier_id": 14,
            "courier_type": "car",
            "regions": [1, 12, 22],
            "working_hours": "11:35-14:05"
            }
        ]}
        resp = self.client.post('/couriers', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['validation_error'])
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')
        self.assertCountEqual(resp_data['validation_error']['couriers'], [{'id':14}])

        data = {
        "data": [        
            {
            "courier_id": 14,
            "courier_type": "car",
            "regions": 22,
            "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]}
        resp = self.client.post('/couriers', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['validation_error'])
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')
        self.assertCountEqual(resp_data['validation_error']['couriers'], [{'id':14}])

        data = {
        "data": [        
            {
            "courier_id": 14,
            "courier_type": "car",
            "regions": [1, 12, 22],
            "some_shit": ["11:35-14:05", "09:00-11:00"]
            },
            {
            "courier_id": 15,
            "courier_type": "car",
            "regions": [22],
            "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]}
        resp = self.client.post('/couriers', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['validation_error'])
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')
        self.assertCountEqual(resp_data['validation_error']['couriers'], [{'id':14}])
     
    def test_other(self):
        data = {
        "data": [        
            {
            "courier_id": 14,
            "courier_type": "shit",
            "regions": [1, 12, 22],
            "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]}
        resp = self.client.get('/couriers', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 404)
        resp = self.client.patch('/couriers', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 404)
        

class OrdersRequestTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        generate_couriers()
        generate_orders()
    
    def test_post(self):
        data = {
        "data": [        
            {
            "order_id": 11,
            "weight": 0.23,
            "region": 12,
            "delivery_hours": ["09:00-18:00"]        
            },        
            {
            "order_id": 12,
            "weight": 15,
            "region": 1,
            "delivery_hours": ["09:00-18:00"]        
            },        
            {
            "order_id": 13,
            "weight": 0.01,
            "region": 22,
            "delivery_hours": ["09:00-12:00", "16:00-21:30"]        
            }
        ]}
        resp = self.client.post('/orders', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['orders'])
        self.assertEquals(resp.status_code, 201)
        self.assertEquals(resp.reason_phrase, 'Created')
        self.assertCountEqual(resp_data['orders'], [{'id':11}, {'id':12}, {'id':13}])

        data = {
        "data": [        
            {
            "order_id": 14,
            "weight": -0.01,
            "region": 22,
            "delivery_hours": ["09:00-12:00", "16:00-21:30"]        
            }
        ]}
        resp = self.client.post('/orders', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['validation_error'])
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')
        self.assertCountEqual(resp_data['validation_error']['orders'], [{'id':14}])

        data = {
        "data": [        
            {
           "order_id": 14,
            "weight": 55,
            "region": 22,
            "delivery_hours": ["09:00-12:00", "16:00-21:30"]
            }
        ]}
        resp = self.client.post('/orders', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['validation_error'])
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')
        self.assertCountEqual(resp_data['validation_error']['orders'], [{'id':14}])

        data = {
        "data": [        
            {
            "order_id": 14,
            "weight": 10,
            "region": "22",
            "delivery_hours": ["09:00-12:00", "16:00-21:30"]
            }
        ]}
        resp = self.client.post('/orders', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['validation_error'])
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')
        self.assertCountEqual(resp_data['validation_error']['orders'], [{'id':14}])

        data = {
        "data": [        
            {
            "order_id": 14,
            "weight": 0.01,
            "region": 22,
            "delivery_hours": "09:00-12:00"
            }
        ]}
        resp = self.client.post('/orders', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['validation_error'])
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')
        self.assertCountEqual(resp_data['validation_error']['orders'], [{'id':14}])

        data = {
        "data": [        
            {
            "order_id": 14,
            "weight": 0.01,
            "region": 22,
            "delivery_hours": ["09 : 00 - 12 : 00", "16:00-21:30"]
            }
        ]}
        resp = self.client.post('/orders', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['validation_error'])
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')
        self.assertCountEqual(resp_data['validation_error']['orders'], [{'id':14}])   
        
        data = {
        "data": [        
            {
            "order_id": 14,
            "weight": 0.01,
            "region": 22,
            "some_shit": ["09:00-12:00", "16:00-21:30"]
            },
            {
            "order_id": 14,
            "weight": 0.01,
            "region": 22,
            "delivery_hours": ["09:00-12:00", "16:00-21:30"]
            }
        ]}
        resp = self.client.post('/orders', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['validation_error'])
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')
        self.assertCountEqual(resp_data['validation_error']['orders'], [{'id':14}])
        #resp = self.client.patch()
    
    def test_other(self):
        data = {
        "data": [        
            {
            "order_id": 11,
            "weight": 0.23,
            "region": 12,
            "delivery_hours": ["09:00-18:00"]        
            }
        ]}
        resp = self.client.get('/orders', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 404)
        resp = self.client.patch('/orders', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 404)

class OrdersAssignRequestTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        generate_couriers()
        generate_orders()
    
    def test_post(self):
        data = {"courier_id": 8}
        resp = self.client.post('/orders/assign', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['orders', 'assign_time'])
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.reason_phrase, 'OK')
        self.assertCountEqual(resp_data['orders'], [{'id':1}, {'id':3}, {'id':4}, {'id':6}])

        data = {"courier_id": 5}
        resp = self.client.post('/orders/assign', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['orders', 'assign_time'])
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.reason_phrase, 'OK')
        self.assertCountEqual(resp_data['orders'], [{'id':7}])

        data = {"courier_id": 8}
        resp = self.client.post('/orders/assign', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['orders', 'assign_time'])
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.reason_phrase, 'OK')
        self.assertCountEqual(resp_data['orders'], [{'id':1}, {'id':3}, {'id':4}, {'id':6}])

        order = models.Order.objects.get(id=3)
        dt = datetime.now(tz=timezone.utc)
        dt = dt.replace(hour=11, minute=50)
        order.complete(dt)
        resp = self.client.post('/orders/assign', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['orders', 'assign_time'])
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.reason_phrase, 'OK')
        self.assertCountEqual(resp_data['orders'], [{'id':1}, {'id':4}, {'id':6}])

        order = models.Order.objects.get(id=1)
        dt = dt.replace(hour=12, minute=20)
        order.complete(dt)
        order = models.Order.objects.get(id=4)
        dt = dt.replace(hour=12, minute=40)
        order.complete(dt)
        order = models.Order.objects.get(id=6)
        dt = dt.replace(hour=14, minute=10)
        order.complete(dt)
        resp = self.client.post('/orders/assign', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEquals(list(resp_data.keys()), ['orders', 'assign_time'])
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.reason_phrase, 'OK')
        self.assertCountEqual(resp_data['orders'], [{'id':10}])

        data = {"courier_id": 11}
        resp = self.client.post('/orders/assign', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.reason_phrase, 'Bad Request')

    def test_other(self):
        data = {"courier_id": 8}
        resp = self.client.get('/orders/assign', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 404)
        resp = self.client.patch('/orders/assign', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 404)


class OrdersCompleteRequestTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        generate_couriers()
        generate_orders()
    
    def test_post(self):
        courier = models.Courier.objects.get(id=8)
        courier.assign_orders()
        data = {
            "courier_id": 8,
            'order_id': 1,
            'complete_time': '2021-01-10T12:20:01.42Z'
        }
        resp = self.client.post('/orders/complete', data=data, content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEqual(resp_data['order_id'], 1)
        orders, gg = courier.assign_orders()
        self.assertCountEqual(orders, [{'id': 3},{'id': 4},{'id': 6}])

    def test_other(self):
        data = {
            "courier_id": 8,
            'order_id': 1,
            'complete_time': '2021-01-10T12:20:01.42Z'
        }
        resp = self.client.get('/orders/complete', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 404)
        resp = self.client.patch('/orders/complete', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, 404)