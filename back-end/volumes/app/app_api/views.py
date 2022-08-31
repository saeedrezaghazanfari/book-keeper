import csv
import os
import datetime
import random
from django.shortcuts import render
from django.http import HttpResponse
from persiantools.jdatetime import JalaliDate
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.views import generic
from Extentions.utils import get_client_ip
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from .serializers import (
    BankSerializer
)
from app_auth.models import User 
from .models import BankModel, TransactionModel, VersionsModel, ProfileCollectorModel



# url: notfound pages
def error_404_view(request, exception):
    return render(request, '404.html')


# url: /api/v1/get-user-data/
class GetUserData(APIView):
    def get(self, request):
        data = {
            'is_superuser': request.user.is_superuser,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'username': request.user.username,
            'profile': str(request.user.profile),
            'is_guest': request.user.is_guest
        }

        # get user ip
        ip = get_client_ip(request=request)
        if ip != request.user.ip_address:
            request.user.ip_address = ip
            request.user.save()

        return Response({'data': data, 'status': 200})


# url: /api/v1/create-guest/
class CreateGuestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.GET.get('un'):
            User.objects.get(username=request.GET.get('un')).delete()
            return Response({'status': 200})

    def post(self, request):
        all_chars = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
            's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
            'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
            '1', '2', '3', '4', '5', '6', '7', '8', '9'
        ]
        password_gen = ''
        for _ in range(1, 11):
            password_gen += random.choice(all_chars)
        username_gen = f'{random.randint(1000, 9999)}{random.choice(all_chars)}{random.choice(all_chars)}{random.choice(all_chars)}{random.choice(all_chars)}'
        user = User.objects.create(
            first_name = 'مهمان',
            username = username_gen,
            is_guest=True
        )
        user.set_password(password_gen)
        user.save()

        mellat_card = BankModel.objects.create(
            user=user,
            name='بانک ملت',
            card_number=f'{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}',
            stock=150000
        )
        melli_card = BankModel.objects.create(
            user=user,
            name='بانک ملی',
            card_number=f'{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}',
            stock=250000
        )
        refah_card = BankModel.objects.create(
            user=user,
            name='بانک رفاه',
            card_number=f'{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}',
            stock=310000
        )
        for _ in range(1, 16):
            cards = [mellat_card, melli_card, refah_card]
            types = ['withdrawal', 'deposit']
            type_choosed = random.choice(types)
            if type_choosed == 'withdrawal':
                descs = ['خرید بستنی', 'خرید لباس', 'خرید کیک و نوشابه', 'خرید سبزیجات', 'خرید لبنیات', 'خرید شارژر موبایل', 'خرید کتاب', 'خرید پیتزا']
            elif type_choosed == 'deposit':
                descs = ['فروش بستنی', 'فروش لباس', 'فروش کیک و نوشابه', 'فروش سبزیجات', 'فروش لبنیات', 'فروش شارژر موبایل', 'فروش کتاب', 'فروش پیتزا']
            TransactionModel.objects.create(
                user=user,
                card=random.choice(cards),
                price=random.randint(100, 999) * 1000,
                in_out=type_choosed,
                description=random.choice(descs),
                time=f'{random.randint(1, 23)}:{random.randint(10, 59)}:00',
                date=datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
            )

        if user:
            return Response({'status': 200, 'user': username_gen, 'pw': password_gen})


# url: /api/v1/card-management/
class CardManagement(APIView):
    def get(self, request):
        banks = BankModel.objects.filter(
            user=request.user
        ).values('name')
        return Response({'data': banks, 'status': 200})

    def post(self, request):
        if request.user:
            serializer = BankSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            if BankModel.objects.filter(user=request.user, card_number=request.data['card_number']).first():
                return Response({'status': 400, 'msg': 'c'})

            if BankModel.objects.filter(user=request.user, name=request.data['name']).first():
                return Response({'status': 400, 'msg': 'n'})

            BankModel.objects.create(
                user=request.user,
                name=request.data['name'],
                card_number=request.data['card_number'], 
                stock=request.data['stock']
            )
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
                user=request.user,
                description__icontains=request.GET.get('query')
            ).all().values('card__name', 'price', 'in_out', 'description', 'time', 'date')
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
            if profile:
                for i in extesion_allowed:
                    if extesion == i:
                        ProfileCollectorModel.objects.filter(
                            user=request.user
                        ).delete()
                        saved_pro = ProfileCollectorModel.objects.create(
                            user=request.user,
                            profile=profile
                        )
                        return Response({'status': 200, 'profile': str(saved_pro.profile)})
                return Response({'status': 400})
            return Response({'status': 400})


# url: /api/v1/info-update/
class InfoUpdateView(APIView):
    def post(self, request):
        if request.user:
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            if first_name:
                request.user.first_name = first_name
            if last_name:
                request.user.last_name = last_name
            if ProfileCollectorModel.objects.filter(user=request.user).first():
                profile_ex = ProfileCollectorModel.objects.get(user=request.user).profile
                profile_ex = str(profile_ex).split('/')
                request.user.profile = '/profiles/' + profile_ex[1]
            request.user.save()
            return Response({'status': 200})


# url: /api/v1/get-last-version/
class GetLastVersion(APIView):
    def get(self, request):
        v = VersionsModel.objects.last()
        if not v:
            v = VersionsModel.objects.create(version='0.0.0', description='0.0.0')
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