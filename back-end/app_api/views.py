import csv
import os
import datetime
from django.http import HttpResponse
from persiantools.jdatetime import JalaliDate
from rest_framework.views import APIView
from django.views import generic
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from .serializers import (
    BankSerializer
)
from app_auth.models import User 
from .models import BankModel, TransactionModel, VersionsModel, ProfileCollectorModel


# url: /api/v1/get-user-data/
class GetUserData(APIView):
    def get(self, request):
        data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'username': request.user.username
        }
        return Response({'data': data, 'status': 200})


# url: /api/v1/card-management/
class CardManagement(APIView):
    def get(self, request):
        return Response({'data': BankModel.objects.all().values('name'), 'status': 200})

    def post(self, request):
        if request.user:
            serializer = BankSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            obj = BankModel.objects.filter(
                card_number=request.data['card_number'], 
                name=request.data['name']
            ).first()
            obj.user = request.user
            obj.save()
            return Response({'status': 200})


# url: /api/v1/transaction-management/
class TransactionManagement(APIView):
    def get(self, request):
        if not request.GET.get('type'):
            bank = request.GET.get('bank')
            amount = int(request.GET.get('amount'))
            card = BankModel.objects.filter(user=request.user, name=bank).first()
            data = TransactionModel.objects.filter(
                user=request.user,
                card=card
            ).all()[:amount].values('price', 'in_out', 'description', 'time', 'date')
            last_stock = BankModel.objects.filter(user=request.user, name=bank).last().stock
            return Response({'data': data, 'last_stock': last_stock, 'status': 200})

        elif request.GET.get('type') and request.GET.get('type') == 'search':
            data = TransactionModel.objects.filter(
                card=BankModel.objects.filter(user=request.user).first(),
                description__icontains=request.GET.get('query')
            ).all().values('price', 'in_out', 'description', 'time', 'date')
            return Response({'data': data, 'status': 200})

    def post(self, request):
        if request.user:            
            date_arr = request.data['date'].split("/")
            obj = TransactionModel.objects.create(
                user=request.user,
                card=BankModel.objects.get(user=request.user, name=request.data['card']),
                price=request.data['price'],
                in_out=request.data['in_out'],
                description=request.data['description'],
                time=request.data['time'],
                date=JalaliDate(int(date_arr[0]), int(date_arr[1]), int(date_arr[2])).to_gregorian()
            )
            if obj:
                bank = BankModel.objects.filter(user=request.user, name=request.data['card']).first()
                if obj.in_out == 'withdrawal':
                    bank.stock -= float(obj.price)
                elif obj.in_out == 'deposit':
                    bank.stock += float(obj.price)
                bank.save()
            return Response({'status': 200})


# url: /api/v1/profile-collector/
class ProfileCollector(APIView):
    def post(self, request):
        if request.user:            
            profile = request.FILES['profile']
            extesion = os.path.splitext(str(profile))[1].lower()
            extesion_allowed = ['.png', '.jpg', '.jpeg']
            ProfileCollectorModel.objects.filter(
                user=request.user
            ).delete()
            for i in extesion_allowed:
                if extesion == i:
                    saved_pro = ProfileCollectorModel.objects.create(
                        user=request.user,
                        profile=profile
                    )
                    return Response({'status': 200, 'profile': str(saved_pro.profile)})
            return Response({'status': 400})


# url: /api/v1/info-update/
class InfoUpdateView(APIView):
    def post(self, request):
        if request.user:
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            if first_name and last_name:
                request.user.first_name = first_name
                request.user.last_name = last_name
                profile_ex = ProfileCollectorModel.objects.get(user=request.user).profile
                profile_ex = str(profile_ex).split('/')
                request.user.profile = '/profiles/' + profile_ex[1]
                request.user.save()
                return Response({'status': 200})
            return Response({'status': 400})


# url: /api/v1/get-last-version/
class GetLastVersion(APIView):
    def get(self, request):
        v = VersionsModel.objects.last()
        return Response({'version': v.version, 'description': v.description, 'status': 200})


# url: /api/v1/print-account/
class PrintAccount(generic.View):
    def get(self, request):
        if request.user:
            bank_name = request.GET.get('bank-name')
            un = request.GET.get('un')
            response = HttpResponse(content_type='text/csv')
            response.write(u'\ufeff'.encode('utf8'))
            writer = csv.writer(response)

            writer.writerow([
                _('نام بانک'),
                _('مبلغ'),
                _('نوع تراکنش'),
                _('توضیحات'),
                _('زمان'),
                _('تاریخ'),
            ])
            for item in TransactionModel.objects.filter(user=User.objects.get(username=un), card__name=bank_name).all():
                if item.in_out == 'withdrawal':
                    writer.writerow([
                        item.card.name,
                        item.price,
                        _('برداشت'),
                        item.description,
                        item.time,
                        item.date,
                    ])
                elif item.in_out == 'deposit':
                    writer.writerow([
                        item.card.name,
                        item.price,
                        _('واریز'),
                        item.description,
                        item.time,
                        item.date,
                    ])
            response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
            return response


# url: /api/v1/get-chart/
class GetChartApiView(APIView):
    def post(self, request):
        all_or_bank = request.data['all_or_bankname']
        period = request.data['period']  # 7 / 30 / 90 / 180 / 365
        type_tr = request.data['type_transactions']

        prices = []
        items = ''
        
        ## withdrawals and deposits
        if type_tr:
            if all_or_bank == 'all':
                
                # period 7 - 7
                if period == '7':
                    for i in range(1, 8):
                        objects = TransactionModel.objects.filter(
                            user=request.user,
                            in_out=type_tr,
                            date__gte=datetime.datetime.now() - datetime.timedelta(days=i),
                            date__lt=datetime.datetime.now() - datetime.timedelta(days=i-1),
                        ).all()
                        objects = list(objects.values('price'))
                        temp = 0
                        for i in objects:
                            temp += i['price']

                        prices.append(temp)
                        items = [_('دیروز'), _('دو روز گذشته'), _('سه روز گذشته'), _('چهار روز گذشته'), _('پنج روز گذشته'), _('شش روز گذشته'), _('هفت روز گذشته')]

                # period 30 - 4
                if period == '30':
                    for i in range(1, 5):
                        objects = TransactionModel.objects.filter(
                            user=request.user,
                            in_out=type_tr,
                            date__gte=datetime.datetime.now() - datetime.timedelta(days=i*7),
                            date__lt=datetime.datetime.now() - datetime.timedelta(days=(i*7)-7),
                        ).all()
                        objects = list(objects.values('price'))
                        temp = 0
                        for i in objects:
                            temp += i['price']
                        
                        prices.append(temp)
                        items = [_('هفت روز اخیر'), _('هفته‌ی گذشته'), _('سه هفته‌ی پیش'), _('چهار هفته‌ی پیش')]

                # period 90 - 3
                if period == '90':
                    for i in range(1, 4):
                        objects = TransactionModel.objects.filter(
                            user=request.user,
                            in_out=type_tr,
                            date__gte=datetime.datetime.now() - datetime.timedelta(days=i*30),
                            date__lt=datetime.datetime.now() - datetime.timedelta(days=(i*30)-30),
                        ).all()
                        objects = list(objects.values('price'))
                        temp = 0
                        for i in objects:
                            temp += i['price']
                        
                        prices.append(temp)
                        items = [_('یک ماه اخیر'), _('یک ماه گذشته'), _('سه ماه گذشته')]

                # period 180 - 6
                if period == '180':
                    for i in range(1, 7):
                        objects = TransactionModel.objects.filter(
                            user=request.user,
                            in_out=type_tr,
                            date__gte=datetime.datetime.now() - datetime.timedelta(days=i*30),
                            date__lt=datetime.datetime.now() - datetime.timedelta(days=(i*30)-30),
                        ).all()
                        objects = list(objects.values('price'))
                        temp = 0
                        for i in objects:
                            temp += i['price']
                        
                        prices.append(temp)
                        items = [_('یک ماه اخیر'), _('یک ماه گذشته'), _('سه ماه گذشته'), _('چهار ماه گذشته'), _('پنج ماه گذشته'), _('شش ماه گذشته')]

                # period 365 - 12
                if period == '365':
                    for i in range(1, 13):
                        objects = TransactionModel.objects.filter(
                            user=request.user,
                            in_out=type_tr,
                            date__gte=datetime.datetime.now() - datetime.timedelta(days=i*30),
                            date__lt=datetime.datetime.now() - datetime.timedelta(days=(i*30)-30),
                        ).all()
                        objects = list(objects.values('price'))
                        temp = 0
                        for i in objects:
                            temp += i['price']
                        
                        prices.append(temp)
                        items = [_('یک ماه اخیر'), _('یک ماه گذشته'), _('سه ماه گذشته'), _('چهار ماه گذشته'), _('پنج ماه گذشته'), _('شش ماه گذشته'), _('هفت ماه گذشته'), _('هشت ماه گذشته'), _('نه ماه گذشته'), _('ده ماه گذشته'), _('یازده ماه گذشته'), _('دوازده ماه گذشته')]

            else: 
                
                # period 7 - 7
                if period == '7':
                    for i in range(1, 8):
                        objects = TransactionModel.objects.filter(
                            user=request.user,
                            card=BankModel.objects.get(user=request.user, name=all_or_bank),
                            in_out=type_tr,
                            date__gte=datetime.datetime.now() - datetime.timedelta(days=i),
                            date__lt=datetime.datetime.now() - datetime.timedelta(days=i-1),
                        ).all()
                        objects = list(objects.values('price'))
                        temp = 0
                        for i in objects:
                            temp += i['price']

                        prices.append(temp)
                        items = [_('دیروز'), _('دو روز گذشته'), _('سه روز گذشته'), _('چهار روز گذشته'), _('پنج روز گذشته'), _('شش روز گذشته'), _('هفت روز گذشته')]

                # period 30 - 4
                if period == '30':
                    for i in range(1, 5):
                        objects = TransactionModel.objects.filter(
                            user=request.user,
                            card=BankModel.objects.get(user=request.user, name=all_or_bank),
                            in_out=type_tr,
                            date__gte=datetime.datetime.now() - datetime.timedelta(days=i*7),
                            date__lt=datetime.datetime.now() - datetime.timedelta(days=(i*7)-7),
                        ).all()
                        objects = list(objects.values('price'))
                        temp = 0
                        for i in objects:
                            temp += i['price']
                        
                        prices.append(temp)
                        items = [_('هفت روز اخیر'), _('هفته‌ی گذشته'), _('سه هفته‌ی پیش'), _('چهار هفته‌ی پیش')]

                # period 90 - 3
                if period == '90':
                    for i in range(1, 4):
                        objects = TransactionModel.objects.filter(
                            user=request.user,
                            card=BankModel.objects.get(user=request.user, name=all_or_bank),
                            in_out=type_tr,
                            date__gte=datetime.datetime.now() - datetime.timedelta(days=i*30),
                            date__lt=datetime.datetime.now() - datetime.timedelta(days=(i*30)-30),
                        ).all()
                        objects = list(objects.values('price'))
                        temp = 0
                        for i in objects:
                            temp += i['price']
                        
                        prices.append(temp)
                        items = [_('یک ماه اخیر'), _('یک ماه گذشته'), _('سه ماه گذشته')]

                # period 180 - 6
                if period == '180':
                    for i in range(1, 7):
                        objects = TransactionModel.objects.filter(
                            user=request.user,
                            card=BankModel.objects.get(user=request.user, name=all_or_bank),
                            in_out=type_tr,
                            date__gte=datetime.datetime.now() - datetime.timedelta(days=i*30),
                            date__lt=datetime.datetime.now() - datetime.timedelta(days=(i*30)-30),
                        ).all()
                        objects = list(objects.values('price'))
                        temp = 0
                        for i in objects:
                            temp += i['price']
                        
                        prices.append(temp)
                        items = [_('یک ماه اخیر'), _('یک ماه گذشته'), _('سه ماه گذشته'), _('چهار ماه گذشته'), _('پنج ماه گذشته'), _('شش ماه گذشته')]

                # period 365 - 12
                if period == '365':
                    for i in range(1, 13):
                        objects = TransactionModel.objects.filter(
                            user=request.user,
                            card=BankModel.objects.get(user=request.user, name=all_or_bank),
                            in_out=type_tr,
                            date__gte=datetime.datetime.now() - datetime.timedelta(days=i*30),
                            date__lt=datetime.datetime.now() - datetime.timedelta(days=(i*30)-30),
                        ).all()
                        objects = list(objects.values('price'))
                        temp = 0
                        for i in objects:
                            temp += i['price']
                        
                        prices.append(temp)
                        items = [_('یک ماه اخیر'), _('یک ماه گذشته'), _('سه ماه گذشته'), _('چهار ماه گذشته'), _('پنج ماه گذشته'), _('شش ماه گذشته'), _('هفت ماه گذشته'), _('هشت ماه گذشته'), _('نه ماه گذشته'), _('ده ماه گذشته'), _('یازده ماه گذشته'), _('دوازده ماه گذشته')]

        ## response
        return Response({'prices': prices, 'items': items, 'status': 200})