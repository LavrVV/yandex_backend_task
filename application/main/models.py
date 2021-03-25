from django.db import models
import json
import re
import datetime
# Create your models here.
class TimeInterval:
    def __init__(self, s) -> None:
        if re.match(r'^\d{2}:\d{2}-\d{2}:\d{2}$', s):
            t1, t2 = s.split('-')
            self.hour_start, self.minute_start = t1.split(':')
            self.hour_start = int(self.hour_start)
            self.minute_start = int(self.minute_start)
            self.hour_end, self.minute_end = t2.split(':')
            self.hour_end = int(self.hour_end)
            self.minute_end = int(self.minute_end)
            self.delta = (self.hour_end * 60 + self.minute_end) - (self.hour_start * 60 + self.minute_start)
            if self.delta < 0:
                raise ValueError('wrong_format')
        else:
            raise ValueError('wrong_format')
    
    def intersection(self, other):
        if self.hour_start * 60 + self.minute_start < other.hour_end * 60 + other.minute_end and \
        self.hour_end * 60 + self.minute_end > other.hour_start * 60 + other.minute_start:
            return True
        else:
            return False

class Region(models.Model):
    def __str__(self) -> str:
        return str(self.id)


#TODO: weight variable, json_shema, fields settings
class Courier(models.Model):
    courier_type = models.TextField(default='foot')
    regions = models.ManyToManyField(Region)
    working_hours = models.TextField()
    rating = models.FloatField(default=0.0)
    earning = models.IntegerField(default=0)
    current_unfinished_orders = models.IntegerField(default=0)
    
    @classmethod
    def create(cls, json_data):
        try:
            cls._validate(json_data)
            if len(json_data.keys()) != 4:
                raise ValueError(json_data['courier_id'])   
        except KeyError:
            raise ValueError('no id field')
        except:
            raise ValueError(json_data['courier_id'])
        
        try:
            working_hours = json_data['working_hours'][0]
            for i in json_data['working_hours'][1:]:
                working_hours += ' '
                working_hours += i
            res = cls(id=json_data['courier_id'], working_hours=working_hours, courier_type=json_data['courier_type'])
            for i in json_data['regions']:
                r = Region.objects.get_or_create(id=i)
                r[0].save()
            res.save()
            res.regions.set(json_data['regions'])
            res.save()
        except Exception as e:
            print(e)
            raise ValueError(json_data['courier_id'])
        return res
    
    @classmethod
    def _validate(cls, json_data):
        for key, value in json_data.items():
            if key == 'courier_type':
                if value not in ['foot', 'bike', 'car']:
                    raise ValueError('courier_type')

            elif key == 'regions':
                if type(value) != list:
                    raise ValueError('regions')
                else:
                    for i in value:
                        if type(i) != int or i <= 0:
                            raise ValueError('regions')

            elif key == 'courier_id':
                if type(value) != int or value <= 0:
                    raise ValueError('courier_id')

            elif key == 'working_hours':
                if type(value) != list:
                    raise ValueError('working_hours')
                else:
                    for i in value:
                        try: 
                            TimeInterval(i)
                        except:
                            raise ValueError('workig_hours')
                    
            else:
                raise ValueError('Unknown argument ' + key)
        return True

    def update(self, json_data):
        Courier._validate(json_data)
        for key, value in json_data.items():
            if key == 'courier_type':
                self.courier_type = value
            elif key == 'regions':
                for i in value:
                    Region.objects.get_or_create(id=i)
                self.regions.set(value)
            elif key == 'working_hours':
                self.set_working_hours(value)
        self.save()
        self._reassign_orders()

    def _reassign_orders(self):
        orders = Order.objects.filter(courier=self, complete_time=None).order_by('weight')
        w = 0.0
        for order in orders:
            if (w + order.weight <= self.get_maxweight() and
                    order.region in self.regions.all() and
                    self._intersection(order.get_delivery_hours())):
                w += order.weight
            else:
                order.assign_time = None
                order.courier = None
                order.save()
                self.current_unfinished_orders -= 1
    
    def _intersection(self, delivery_hours):
        found = False
        for w_hours in self.get_working_hours():
            for d_hours in delivery_hours:
                if w_hours.intersection(d_hours):
                    found = True
            if found:
                break
        return found

    def get_maxweight(self):
        weight = {'foot': 10.0, 'bike': 15.0, 'car': 50.0}
        return weight[self.courier_type]

    def assign_orders(self):
        if self.current_unfinished_orders > 0:
            res = []
            orders = Order.objects.filter(courier=self, complete_time=None).order_by('id')
            for i in orders:
                res.append({'id': i.id})
            return res, orders[0].assign_time.isoformat(timespec='milliseconds')[:22] + 'Z'
        elif self.current_unfinished_orders < 0:
            raise ValueError('i don\'t know what happend')
        orders = Order.objects.filter(region__in=self.regions.all(), courier=None).order_by('weight')
        w = 0.0
        res = []
        assign_time = datetime.datetime.now(tz=datetime.timezone.utc)#NOW
        for order in orders:
            if w + order.weight <= self.get_maxweight():
                found = self._intersection(order.get_delivery_hours())
                if not found:
                    continue
                w += order.weight
                order.assign_time = assign_time.isoformat()
                order.courier = self
                order.cost = self.courier_type
                order.save()
                self.current_unfinished_orders += 1
                res.append({'id': order.id})
            else:
                break
        self.save()
        return res, assign_time.isoformat(timespec='milliseconds')[:22] + 'Z'

    def set_working_hours(self, data):
        TimeInterval(data[0])
        working_hours = data[0]
        for i in data[1:]:
            TimeInterval(i)
            working_hours += ' '
            working_hours += i
        self.working_hours = working_hours

    def get_working_hours(self):
        res = []
        for i in self.working_hours.split(' '):
            res.append(TimeInterval(i))
        return res

    def get_rating(self):
        td = {}
        orders = Order.objects.filter(courier=self, complete_time__isnull=False).order_by('assign_time', 'complete_time')
        if orders.count() == 0:
            return 0
        curr_assign_time = 0
        prev_complete_time = 0
        for order in orders:
            try:
                td[order.region.id]['value']
            except:
                td[order.region.id] = {'value': 0.0, 'count': 0}
            if order.assign_time == curr_assign_time:
                td[order.region.id]['count'] += 1
                td[order.region.id]['value'] += abs((order.complete_time - prev_complete_time).total_seconds())
            else:
                curr_assign_time = order.assign_time
                td[order.region.id]['count'] += 1
                td[order.region.id]['value'] += abs((order.complete_time - order.assign_time).total_seconds())
            prev_complete_time = order.complete_time
        tm = -1
        for i in td.values():
            if tm > i['value'] / i['count'] or tm < 0:
                tm = i['value'] / i['count']
        return (60*60 - min(tm, 60*60))/(60*60) * 5

    def get_delivery_count(self):
        if self.current_unfinished_orders > 0:
            return self.delivery_count - 1
        else:
            return self.delivery_count 

    def get_earnings(self):
        return self.earning


class Order(models.Model):
    weight = models.FloatField()
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    delivery_hours = models.TextField()
    courier = models.ForeignKey(Courier, on_delete=models.PROTECT, null=True)
    complete_time = models.DateTimeField(null=True)
    assign_time = models.DateTimeField(null=True)
    cost = models.TextField(default='foot')

    @classmethod
    def create(cls, json_data):
        try:
            cls._validate(json_data)
            if len(json_data.keys()) != 4:
                raise ValueError(json_data['order_id'])
        except KeyError:
            raise ValueError('no id field')  
        except:
            raise ValueError(json_data['order_id'])
        try:
            delivery_hours = json_data['delivery_hours'][0]
            for i in json_data['delivery_hours'][1:]:
                delivery_hours += ' '
                delivery_hours += i
            Region.objects.get_or_create(id=json_data['region'])
            res = cls(id=json_data['order_id'], delivery_hours=delivery_hours, weight=json_data['weight'], region_id=json_data['region'])
            res.save()
        except:
            raise ValueError(json_data['order_id'])
        return res
    
    @classmethod
    def _validate(cls, json_data):
        for key, value in json_data.items():
            if key == 'weight':
                if (type(value) != float and type(value) != int) or value < 0.01 or value > 50:
                    raise ValueError('weight')

            elif key == 'region':
                if type(value) != int or value <= 0:
                    raise ValueError('region')

            elif key == 'order_id':
                if type(value) != int or value <= 0:
                    raise ValueError('order_id')

            elif key == 'delivery_hours':
                if type(value) != list:
                    raise ValueError('delivery_hours')
                else:
                    for i in value:
                        try: 
                            TimeInterval(i)
                        except:
                            raise ValueError('delivery_hours')
                    
            else:
                raise ValueError('Unknown argument ' + key)
        return json_data

    def set_delivery_hours(self, data):
        TimeInterval(data[0])
        delivery_hours = data[0]
        for i in data[1:]:
            TimeInterval(i)
            delivery_hours += ' '
            delivery_hours += i
        self.working_hours = delivery_hours

    def get_delivery_hours(self):
        res = []
        for i in self.delivery_hours.split(' '):
            res.append(TimeInterval(i))
        return res

    def complete(self, complete_time):
        if type(complete_time) != datetime.datetime:
            raise ValueError('wrong complete time')
        ok = False
        for i in self.get_delivery_hours():
            if (i.hour_start * 60 + i.minute_start <= complete_time.hour * 60 + complete_time.minute and
                    i.hour_end * 60 + i.minute_end >= complete_time.hour * 60 + complete_time.minute):
                ok = True
                break
        if not ok:
            raise ValueError('wrong complete time')
        if self.assign_time != None and self.courier != None and self.complete_time == None:
            if self.courier.current_unfinished_orders <= 0:
                raise ValueError(self.courier.current_unfinished_orders)
            self.complete_time = complete_time
            self.courier.current_unfinished_orders -= 1
            self.save()
            if self.courier.current_unfinished_orders == 0:
                self.courier.earning += 500 * self.get_cost()
            self.courier.save()

    def get_cost(self):
        cost = {'foot': 2, 'bike': 5, 'car': 9}
        return cost[self.cost]