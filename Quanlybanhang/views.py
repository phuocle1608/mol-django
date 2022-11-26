from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from . import models
from django.views import View
from django.db import connection
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import pytz
# Create your views here.


connection.force_debug_cursor = True

def handle_not_found(request, exception):
    return render(request, 'QLBH/404.html')

def func_convert_local_time(xdate):
    try:
        mytimezone = pytz.timezone("Etc/GMT")
        dtobj4 = mytimezone.localize(xdate)
        dt_final = dtobj4.astimezone(pytz.timezone("Etc/GMT-7"))
        return dt_final.replace(tzinfo=None)
    except Exception as e:
        return str(e)

def cursorbyname(rawsql):
    
    cursor = connection.cursor()
    cursor.execute(rawsql)
    result = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    result = [dict(zip(column_names, item)) for item in result]
    return result

# def view_donhang_info(request):
#     donhang = models.Donhang.objects.all()
#     list_donhang = models.Donhang.objects.raw('''select *, Donhang_Price_Combo + Donhang_Price_Upsale - Donhang_Price_Discount as Total from Quanlybanhang_donhang''')
#     print(donhang.query)
#     print(list_donhang)
#     # for item in list_donhang:
#
#     return render(request, 'html/danhsachdonhang.html', {'list_donhang': list_donhang})

class Homepage(View):
    def get(self, request):
        return redirect('/donhang/')

class Login(View):
    def get(self, request):
        return render(request, 'QLBH/login.html')
    def post(self, request):
        login_user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if login_user is None:
            return self.get(request)
        else:
            login(request, login_user)
            return redirect('../donhang/')


class CursorByName():
    def __init__(self, cursor):
        self._cursor = cursor

    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()
        return {description[0]: row[col] for col, description in enumerate(self._cursor.description)}

class DonhangTonghop(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        # call danh_sach_don_hang()
        list_donhang = cursorbyname("""
            select 
                a.Donhang_Id, a.Donhang_Name, case a.FlashDesign_Flag when 1 then 'Flash Design' else '' end Flash_Flag, DATE_ADD(a.CreatedDate, INTERVAL a.Deadline DAY) as Deadline,
                d.Workingstatus_Name, a.CreatedDate, c.Customer_Name, c.Customer_Phone, a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount as Total, 
                a.Donhang_Price_Payment, a.Workingstatus_Id, b.Product_Name, e.Source_Name,
                case 
                    when a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment > 0 then a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment
                    else 0 
                end as Deft,
                case
                    when a.Workingstatus_Id = 8 then -999
                    else
                        datediff(CURDATE(), DATE_ADD(CreatedDate, INTERVAL Deadline DAY))
                end as DeadlineList                       
            from Quanlybanhang_donhang a 
                left join Quanlybanhang_product b on a.Product_Id = b.Product_Id 
                left join Quanlybanhang_customer c on c.Customer_Id = a.Customer_Id
                left join Quanlybanhang_workingstatus d on d.Workingstatus_Id = a.Workingstatus_Id
                left join Quanlybanhang_source e on e.Source_Id = c.Source_Id
            where a.IsDelete = 0 and a.CreatedDate > DATE_ADD(CURDATE(), INTERVAL -30 DAY)
            order by a.Donhang_Id desc
        """)

        list_working = cursorbyname("""
            select *     
            from Quanlybanhang_workingstatus 
            order by Workingstatus_Id asc
        """)

        list_donhang_final = {
            'all': list_donhang
        }
        # by working status
        for item in list_working:
            list_donhang_final['working-{}'.format(item['Workingstatus_Id'])] = list(filter(lambda x: x['Workingstatus_Id'] == item['Workingstatus_Id'], list_donhang))

        # close deadline
        list_donhang_final['close_deadline'] = list(filter(lambda x: x['DeadlineList'] >= -1, list_donhang))

        # chua thanh toan
        list_donhang_final['notpayment'] = list(filter(lambda x: x['Deft'] > 0, list_donhang))
        return render(request, 'QLBH/tong_hop_don_hang.html', {'list_donhang_final': list_donhang_final, 'filteroption': 'Last 30 Days', 'list_working': list_working, 'start_date': '2022-01-01', 'start_end': '2022-12-31'})

    def post(self, request):
        print(request.POST['daterangepicker_type'])
        list_donhang = cursorbyname("""
                select 
                    a.Donhang_Id, a.Donhang_Name, case a.FlashDesign_Flag when 1 then 'Flash Design' else '' end Flash_Flag, DATE_ADD(a.CreatedDate, INTERVAL a.Deadline DAY) as Deadline,
                    d.Workingstatus_Name, a.CreatedDate, c.Customer_Name, c.Customer_Phone, a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount as Total, 
                    a.Donhang_Price_Payment, a.Workingstatus_Id, b.Product_Name, e.Source_Name,
                    case 
                        when a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment > 0 then a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment
                        else 0 
                    end as Deft,
                    case
                        when a.Workingstatus_Id = 8 then -999
                        else
                            datediff(CURDATE(), DATE_ADD(CreatedDate, INTERVAL Deadline DAY))
                    end as DeadlineList     
                from Quanlybanhang_donhang a 
                    left join Quanlybanhang_product b on a.Product_Id = b.Product_Id 
                    left join Quanlybanhang_customer c on c.Customer_Id = a.Customer_Id
                    left join Quanlybanhang_workingstatus d on d.Workingstatus_Id = a.Workingstatus_Id
                    left join Quanlybanhang_source e on e.Source_Id = c.Source_Id
                where a.IsDelete = 0 and a.CreatedDate >= '{}' and a.CreatedDate <= '{}'
                order by a.Donhang_Id desc
            """.format(request.POST['daterangepicker_start'], request.POST['daterangepicker_end'])
            )
        
        list_working = cursorbyname("""
                    select *     
                    from Quanlybanhang_workingstatus 
                    order by Workingstatus_Id asc
                """)

        list_donhang_final = {
            'all': list_donhang
        }
        # by working status
        for item in list_working:
            list_donhang_final['working-{}'.format(item['Workingstatus_Id'])] = list(filter(lambda x: x['Workingstatus_Id'] == item['Workingstatus_Id'], list_donhang))

        # close deadline
        list_donhang_final['close_deadline'] = list(filter(lambda x: x['DeadlineList'] >= -1, list_donhang))

        # chua thanh toan
        list_donhang_final['notpayment'] = list(filter(lambda x: x['Deft'] > 0, list_donhang))
        # 'filteroption': request.POST['inputState']
        start_date = datetime.datetime.strptime(request.POST['daterangepicker_start'], '%Y-%m-%d').strftime('%d/%m/%Y')
        end_date = datetime.datetime.strptime(request.POST['daterangepicker_end'], '%Y-%m-%d').strftime('%d/%m/%Y')

        return render(request, 'QLBH/tong_hop_don_hang.html', {'list_donhang_final': list_donhang_final, 'filteroption': request.POST['daterangepicker_type'], 'list_working': list_working, 'start_date': start_date, 'end_date': end_date})



# <th>Mã đơn</th>
# <th>Tên logo</th>
# <th>Loại đơn</th>
# <th>Deadline</th>
# <th>Tiến độ thực hiện</th>
# <th>Ngày tạo đơn</th>
# <th>Tên khách hàng</th>
# <th>Số điện thoại</th>
# <th>Tổng giá trị</th>
# <th>Đã thanh toán</th>
# <th>Chưa thanh toán</th>
# <th>Ghi chú</th>

class DonhangDetail(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, donhang_id):
        list_donhang = models.Donhang.objects.raw("""
            select 
                a.Donhang_Id, a.Donhang_Name, case a.FlashDesign_Flag when 1 then 'Flash Design' else '' end Flash_Flag, date_add(a.CreatedDate, INTERVAL a.Deadline DAY) as Deadline, 
                d.Workingstatus_Name, a.CreatedDate, a.Image1, a.Image2, a.Image3, a.Image4, a.Image5, a.Image6,
                a.Donhang_Price_Combo, a.Donhang_Price_Upsale, a.Donhang_Price_Discount, b.Product_Name, a.Donhang_Require,
                a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount as Total, 
                case 
                    when a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment > 0 then a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment
                    else 0 
                end as Deft, c.*, e.Source_Name
            from Quanlybanhang_donhang a 
                left join Quanlybanhang_product b on a.Product_Id = b.Product_Id 
                left join Quanlybanhang_customer c on c.Customer_Id = a.Customer_Id
                left join Quanlybanhang_workingstatus d on d.Workingstatus_Id = a.Workingstatus_Id
                left join Quanlybanhang_source e on e.Source_Id = c.Source_Id
            where a.Donhang_Id = {}
            """.format(donhang_id))
        if len(list_donhang) > 0:
            donhang = list_donhang[0]
            return render(request, 'QLBH/chi_tiet_don_hang.html', {'donhang': donhang})
        else:
            return handle_not_found(request, '404')

    def post(self, request, donhang_id):
        a = Updatedonhang()
        a.post(request, donhang_id)
        if request.POST['button'] == 'update':
            return self.get(request, donhang_id)
        elif request.POST['button'] == 'delete':
            return redirect('/donhang/')

class Updatedonhang(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, donhang_id):
        customer = models.Customer.objects.all()
        product = models.Product.objects.all()
        working = models.Workingstatus.objects.all()
        try:
            # update_don_hang
            donhang = cursorbyname("""
                select 
                    a.*, b.Product_Name, d.Workingstatus_Name, e.Source_Name, c.*
                from Quanlybanhang_donhang a 
                    left join Quanlybanhang_product b on a.Product_Id = b.Product_Id 
                    left join Quanlybanhang_customer c on c.Customer_Id = a.Customer_Id
                    left join Quanlybanhang_workingstatus d on d.Workingstatus_Id = a.Workingstatus_Id
                    left join Quanlybanhang_source e on e.Source_Id = c.Source_Id
                where a.Donhang_Id = {} and a.IsDelete = 0
            """.format(donhang_id))[0]
        except:
            return handle_not_found(request, '404')
        # print(donhang)
        return render(request, 'QLBH/sua_don_hang.html', {'donhang': donhang, 'customer': customer, 'product': product, 'working': working})
    def post(self, request, donhang_id):
        if request.POST['button'] == 'update':
            models.Donhang.objects.filter(pk=donhang_id).update(
                Donhang_Name=request.POST['Donhang_Name'],
                FlashDesign_Flag=request.POST['FlashDesign_Flag'],  # 1 if request.POST['FlashDesign_Flag'] == 'on' else 0,
                Workingstatus_Id=models.Workingstatus.objects.get(pk=request.POST['Workingstatus_Id']),
                Product_Id=models.Product.objects.get(pk=request.POST['Product_Id']),
                Customer_Id=models.Customer.objects.get(pk=request.POST['Customer_Id']),
                Deadline=request.POST['Deadline'],
                Donhang_Require=request.POST['Donhang_Require'],
                Donhang_Price_Combo=request.POST['Donhang_Price_Combo'],
                Donhang_Price_Discount=request.POST['Donhang_Price_Discount'],
                Donhang_Price_Upsale=request.POST['Donhang_Price_Upsale'],
                Donhang_Price_Payment=request.POST['Donhang_Price_Payment'],
                LastUpdate=func_convert_local_time(datetime.datetime.utcnow()),
                Username=request.user,
                Image1=request.POST['Image1'],
                Image2=request.POST['Image2'],
                Image3=request.POST['Image3'],
                Image4=request.POST['Image4'],
                Image5=request.POST['Image5'],
                Image6=request.POST['Image6'],
            )
            return redirect('../../donhang/{}/'.format(donhang_id), )

        elif request.POST['button'] == 'delete':
            models.Donhang.objects.filter(pk=donhang_id).update(
                IsDelete=1
            )
            return redirect('/donhang/')

class NhapDonHang(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        customer = models.Customer.objects.all().order_by('-Customer_Id')
        product = models.Product.objects.all()
        working = models.Workingstatus.objects.all()
        # selected_customer = 0
        return render(request, 'QLBH/nhap_don_hang.html', {'customer': customer, 'product': product, 'working': working})

    def post(self, request):
        # print(1/0)
        # return HttpResponse(self.func_convert_local_time(datetime.datetime.utcnow()))
        donhang = models.Donhang.objects.create(
            Donhang_Name=request.POST['Donhang_Name'],
            FlashDesign_Flag = request.POST['FlashDesign_Flag'], #1 if request.POST['FlashDesign_Flag'] == 'on' else 0,
            Workingstatus_Id = models.Workingstatus.objects.get(pk=1),
            Product_Id = models.Product.objects.get(pk=request.POST['Product_Id']),
            Customer_Id = models.Customer.objects.get(pk=request.POST['Customer_Id']),
            CreatedDateOrigin = func_convert_local_time(datetime.datetime.utcnow()), # adjust 12h because of local timezone in heroku
            CreatedDate = request.POST['CreatedDate'],
            Deadline = request.POST['Deadline'],
            Donhang_Require = request.POST['Donhang_Require'],
            Donhang_Price_Combo = request.POST['Donhang_Price_Combo'],
            Donhang_Price_Discount = request.POST['Donhang_Price_Discount'],
            Donhang_Price_Upsale = request.POST['Donhang_Price_Upsale'],
            Donhang_Price_Payment = request.POST['Donhang_Price_Payment'],
            LastUpdate = func_convert_local_time(datetime.datetime.utcnow()),
            Username = request.user,
            Image1 = request.POST['Image1'],
            Image2=request.POST['Image2'],
            Image3=request.POST['Image3'],
            Image4=request.POST['Image4'],
            Image5=request.POST['Image5'],
            Image6=request.POST['Image6'],

            # PaymentStatus_Id = models.Paymentstatus.objects.get(pk=1),
        )
        # print(1 / 0)
        customer = models.Customer.objects.all().order_by('-Customer_Id')
        product = models.Product.objects.all()
        working = models.Workingstatus.objects.all()
        return render(request, 'QLBH/nhap_don_hang.html', {'customer': customer, 'product': product, 'working': working})


class NhapKhachHang(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        source = models.Source.objects.all()
        return render(request, 'QLBH/nhap_khach_hang.html', {'source': source})

    def post(self, request):
        cus = models.Customer.objects.create(
            Customer_Name=request.POST['Customer_Name'],
            Customer_Facebook = request.POST['Customer_Facebook'],
            Customer_Phone = request.POST['Customer_Phone'],
            Customer_ZaloName = request.POST['Customer_ZaloName'],
            Customer_Address = request.POST['Customer_Address'],
            Source_Id = models.Source.objects.get(pk=request.POST['Source_Id']),
        )
        # cus.save()
        # return render(request, 'QLBH/nhap_khach_hang.html', {'source': models.Source.objects.all()})
        # print(cus.pk)

        customer = models.Customer.objects.all()
        product = models.Product.objects.all()
        working = models.Workingstatus.objects.all()
        return render(request, 'QLBH/nhap_don_hang.html', {'customer': customer, 'product': product, 'working': working, 'selected_customer': cus.pk})



class AjaxUpdateDatabase(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request):
        if request.POST['post-type'] == 'deal__workingstatus':
            obj = models.Donhang.objects.get(pk=request.POST['donhang_id'])
            # print(obj.Workingstatus_Id)
            # print(models.Workingstatus.objects.get(pk = 2))
            obj.Workingstatus_Id = models.Workingstatus.objects.get(pk = request.POST['value'])
            obj.save()

            return HttpResponse("ok")

        elif request.POST['post-type'] == 'deal__payment':
            obj = models.Donhang.objects.get(pk=request.POST['donhang_id'])
            obj.Donhang_Price_Payment = request.POST['value']
            obj.save()
            return HttpResponse("ok")

class Dashboard(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        donhang_info = cursorbyname("""
            select
                a.Revenue, 
                a.Claim, 
                a.TongDonHang, 
                a.Working, 
                abs(round(100*(a.Revenue/a.Revenue_prev - 1), 0)) as Revenue_per, 
                abs(a.TongDonHang - a.TongDonHang_prev) as TongDonHang_per,
                case
                    when round(100*(a.Revenue/a.Revenue_prev - 1), 0) > 0 then 1
                    when round(100*(a.Revenue/a.Revenue_prev - 1), 0) < 0 then -1
                    else 0 
                end Revenue_sign,
                case
                    when a.TongDonHang - a.TongDonHang_prev > 0 then 1
                    when a.TongDonHang - a.TongDonHang_prev < 0 then -1
                    else 0 
                end TongDonHang_sign
            from (
                select
                (
                    select sum(a.Donhang_Price_Combo - a.Donhang_Price_Discount+ a.Donhang_Price_Upsale)
                    from Quanlybanhang_donhang a 
                    where a.IsDelete = 0 and a.CreatedDate > DATE_ADD(CURDATE(), INTERVAL -30 DAY)
                ) as Revenue,
                (
                    select sum(a.Donhang_Price_Combo - a.Donhang_Price_Discount+ a.Donhang_Price_Upsale - a.Donhang_Price_Payment)
                    from Quanlybanhang_donhang a 
                    where a.IsDelete = 0 and a.CreatedDate > DATE_ADD(CURDATE(), INTERVAL -30 DAY)
                ) as Claim,
                (
                    select count(a.Donhang_Id)
                    from Quanlybanhang_donhang a 
                    where a.IsDelete = 0 and a.CreatedDate > DATE_ADD(CURDATE(), INTERVAL -30 DAY)
                ) as TongDonHang,
                (
                    select count(a.Donhang_Id)
                    from Quanlybanhang_donhang a 
                    where a.IsDelete = 0 and a.CreatedDate > DATE_ADD(CURDATE(), INTERVAL -30 DAY) and a.Workingstatus_Id <= 7
                ) as Working,
                (
                    select sum(a.Donhang_Price_Combo - a.Donhang_Price_Discount+ a.Donhang_Price_Upsale)
                    from Quanlybanhang_donhang a 
                    where a.IsDelete = 0 and a.CreatedDate <= DATE_ADD(CURDATE(), INTERVAL -30 DAY) and a.CreatedDate > DATE_ADD(CURDATE(), INTERVAL -60 DAY)
                ) as Revenue_prev,
                (
                    select count(a.Donhang_Id)
                    from Quanlybanhang_donhang a 
                    where a.IsDelete = 0 and a.CreatedDate <= DATE_ADD(CURDATE(), INTERVAL -30 DAY) and a.CreatedDate > DATE_ADD(CURDATE(), INTERVAL -60 DAY)
                ) as TongDonHang_prev
            ) as a
        """)

        revenue_by_source = cursorbyname("""
            select c.Source_Name, sum(Donhang_Price_Combo - Donhang_Price_Discount+ Donhang_Price_Upsale) Revenue
            from Quanlybanhang_donhang a 
            left join Quanlybanhang_customer b on a.Customer_Id = b.Customer_Id
            left join Quanlybanhang_source c on b.Source_Id = c.Source_Id
            where a.IsDelete = 0 and a.CreatedDate > DATE_ADD(CURDATE(), INTERVAL -30 DAY)
            group by c.Source_Name
            order by c.Source_Name
        """)

        revenue_by_product = cursorbyname("""
            select b.Product_Name, sum(Donhang_Price_Combo - Donhang_Price_Discount+ Donhang_Price_Upsale) Revenue
            from Quanlybanhang_donhang a 
            left join Quanlybanhang_product b on a.Product_Id = b.Product_Id
            where a.IsDelete = 0 and a.CreatedDate > DATE_ADD(CURDATE(), INTERVAL -30 DAY)
            group by b.Product_Name
            order by b.Product_Name
        """)

        revenue_by_source = {
            'label': [i['Source_Name'] for i in revenue_by_source],
            'value': [int(i['Revenue']) for i in revenue_by_source],
        }

        revenue_by_product = {
            'label': [i['Product_Name'] for i in revenue_by_product],
            'value': [int(i['Revenue']) for i in revenue_by_product],
        }

        # donhang_info = donhang_info[0]
        # donhang_info['Revenue_sign'] = (1 if float(donhang_info['Revenue_per']) > 0 else -1) if float(donhang_info['Revenue_per']) != 0 else 0
        # donhang_info['TongDonHang_sign'] = (1 if float(donhang_info['TongDonHang_per']) > 0 else -1) if float(donhang_info['TongDonHang_per']) != 0 else 0
        return render(request, 'QLBH/dashboard.html', {'filteroption': 'Last 30 Days' , 'info': donhang_info[0], 'revenue_by_source': revenue_by_source, 'revenue_by_product': revenue_by_product})


class Test(LoginRequiredMixin, View):
    login_url = '/login/'
    # def post(self, request):
    #     print("ASKJD SKANDJKSN KJASDN JKSADN JKSAD")
    #     print(request.POST['daterangepicker_type'])
    #     return  HttpResponse(request.POST['input__daterangepicker'])

    def post(self, request):
        print(request.POST['daterangepicker_start'])
        print(request.POST['daterangepicker_end'])
        # if request.POST['inputState'] == 'thismonth':
        #     add_to_sql = "and YEAR(a.CreatedDate)=YEAR(CURDATE()) and MONTH(a.CreatedDate)=MONTH(CURDATE())"
        # elif request.POST['inputState'] == 'last30day':
        #     add_to_sql = "and a.CreatedDate > DATE_ADD(curdate(), INTERVAL -30 DAY)"
        # elif request.POST['inputState'] == 'all':
        #     add_to_sql = ""

        list_donhang = cursorbyname("""
                    select 
                        a.Donhang_Id, a.Donhang_Name, case a.FlashDesign_Flag when 1 then 'Flash Design' else '' end Flash_Flag, DATE_ADD(a.CreatedDate, INTERVAL a.Deadline DAY) as Deadline,
                        d.Workingstatus_Name, a.CreatedDate, c.Customer_Name, c.Customer_Phone, a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount as Total, 
                        a.Donhang_Price_Payment, a.Workingstatus_Id, b.Product_Name, e.Source_Name,
                        case 
                            when a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment > 0 then a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment
                            else 0 
                        end as Deft,
                        case
                            when a.Workingstatus_Id = 8 then -999
                            else
                                datediff(CURDATE(), DATE_ADD(CreatedDate, INTERVAL Deadline DAY))
                        end as DeadlineList     
                    from Quanlybanhang_donhang a 
                        left join Quanlybanhang_product b on a.Product_Id = b.Product_Id 
                        left join Quanlybanhang_customer c on c.Customer_Id = a.Customer_Id
                        left join Quanlybanhang_workingstatus d on d.Workingstatus_Id = a.Workingstatus_Id
                        left join Quanlybanhang_source e on e.Source_Id = c.Source_Id
                    where a.IsDelete = 0 and a.CreatedDate >= '{}' and a.CreatedDate <= '{}'
                    order by a.Donhang_Id desc
                """.format(request.POST['daterangepicker_start'], request.POST['daterangepicker_end'])
                )
        
        list_working = cursorbyname("""
                    select *     
                    from Quanlybanhang_workingstatus 
                    order by Workingstatus_Id asc
                """)

        list_donhang_final = {
            'all': list_donhang
        }
        # by working status
        for item in list_working:
            list_donhang_final['working-{}'.format(item['Workingstatus_Id'])] = list(filter(lambda x: x['Workingstatus_Id'] == item['Workingstatus_Id'], list_donhang))

        # close deadline
        list_donhang_final['close_deadline'] = list(filter(lambda x: x['DeadlineList'] >= -1, list_donhang))

        # chua thanh toan
        list_donhang_final['notpayment'] = list(filter(lambda x: x['Deft'] > 0, list_donhang))
        # 'filteroption': request.POST['inputState']
        return render(request, 'QLBH/tong_hop_don_hang.html', {'list_donhang_final': list_donhang_final, 'list_working': list_working})