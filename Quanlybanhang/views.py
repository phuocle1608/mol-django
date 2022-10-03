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

# Create your views here.


connection.force_debug_cursor = True

def handle_not_found(request, exception):
    return render(request, 'QLBH/404.html')

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
                a.Donhang_Price_Payment, 
                case 
                    when a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment > 0 then a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment
                    else 0 
                end as Deft       
            from Quanlybanhang_donhang a 
                left join Quanlybanhang_product b on a.Product_Id = b.Product_Id 
                left join Quanlybanhang_customer c on c.Customer_Id = a.Customer_Id
                left join Quanlybanhang_workingstatus d on d.Workingstatus_Id = a.Workingstatus_Id
            where a.IsDelete = 0 and YEAR(a.CreatedDate)=YEAR(CURDATE()) and MONTH(a.CreatedDate)=MONTH(CURDATE())
            order by a.Donhang_Id desc
        """)
        return render(request, 'QLBH/tong_hop_don_hang.html', {'list_donhang': list_donhang, 'filteroption': 'Tháng này'})
    def post(self, request):
        if request.POST['inputState'] == 'Tháng này':
            add_to_sql = "and YEAR(a.CreatedDate)=YEAR(CURDATE()) and MONTH(a.CreatedDate)=MONTH(CURDATE())"
        elif request.POST['inputState'] == 'Tiếp nhận đơn':
            add_to_sql = "and a.Workingstatus_Id=1"
        elif request.POST['inputState'] == 'Đang thực hiện':
            add_to_sql = "and a.Workingstatus_Id in (2, 3, 4, 5)"
        elif request.POST['inputState'] == 'Upsale':
            add_to_sql = "and a.Workingstatus_Id in (6, 7)"
        elif request.POST['inputState'] == 'Chưa thanh toán':
            add_to_sql = """ and 
                case 
                    when a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment > 0 then a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment
                    else 0 
                end > 0
            """
        elif request.POST['inputState'] == 'Tất cả đơn':
            add_to_sql = ""

        list_donhang = cursorbyname("""
                    select 
                        a.Donhang_Id, a.Donhang_Name, case a.FlashDesign_Flag when 1 then 'Flash Design' else '' end Flash_Flag, DATE_ADD(a.CreatedDate, INTERVAL a.Deadline DAY) as Deadline,
                        d.Workingstatus_Name, a.CreatedDate, c.Customer_Name, c.Customer_Phone, a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount as Total, 
                        a.Donhang_Price_Payment, 
                        case 
                            when a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment > 0 then a.Donhang_Price_Combo + a.Donhang_Price_Upsale - a.Donhang_Price_Discount - a.Donhang_Price_Payment
                            else 0 
                        end as Deft       
                    from Quanlybanhang_donhang a 
                        left join Quanlybanhang_product b on a.Product_Id = b.Product_Id 
                        left join Quanlybanhang_customer c on c.Customer_Id = a.Customer_Id
                        left join Quanlybanhang_workingstatus d on d.Workingstatus_Id = a.Workingstatus_Id
                    where a.IsDelete = 0 {}
                    order by a.Donhang_Id desc
                """.format(add_to_sql))
        return render(request, 'QLBH/tong_hop_don_hang.html', {'list_donhang': list_donhang, 'filteroption': request.POST['inputState']})



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
                d.Workingstatus_Name, a.CreatedDate,
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
                WorkingStatus_Id=models.Workingstatus.objects.get(pk=request.POST['Workingstatus_Id']),
                Product_Id=models.Product.objects.get(pk=request.POST['Product_Id']),
                Customer_Id=models.Customer.objects.get(pk=request.POST['Customer_Id']),
                Deadline=request.POST['Deadline'],
                Donhang_Require=request.POST['Donhang_Require'],
                Donhang_Price_Combo=request.POST['Donhang_Price_Combo'],
                Donhang_Price_Discount=request.POST['Donhang_Price_Discount'],
                Donhang_Price_Upsale=request.POST['Donhang_Price_Upsale'],
                Donhang_Price_Payment=request.POST['Donhang_Price_Payment'],
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
        customer = models.Customer.objects.all()
        product = models.Product.objects.all()
        working = models.Workingstatus.objects.all()
        # selected_customer = 0
        return render(request, 'QLBH/nhap_don_hang.html', {'customer': customer, 'product': product, 'working': working})

    def post(self, request):
        # print(1/0)
        donhang = models.Donhang.objects.create(
            Donhang_Name=request.POST['Donhang_Name'],
            FlashDesign_Flag = request.POST['FlashDesign_Flag'], #1 if request.POST['FlashDesign_Flag'] == 'on' else 0,
            WorkingStatus_Id = models.Workingstatus.objects.get(pk=1),
            Product_Id = models.Product.objects.get(pk=request.POST['Product_Id']),
            Customer_Id = models.Customer.objects.get(pk=request.POST['Customer_Id']),
            CreatedDate = timezone.now(),
            Deadline = request.POST['Deadline'],
            Donhang_Require = request.POST['Donhang_Require'],
            Donhang_Price_Combo = request.POST['Donhang_Price_Combo'],
            Donhang_Price_Discount = request.POST['Donhang_Price_Discount'],
            Donhang_Price_Upsale = request.POST['Donhang_Price_Upsale'],
            Donhang_Price_Payment = request.POST['Donhang_Price_Payment'],
            # PaymentStatus_Id = models.Paymentstatus.objects.get(pk=1),
        )
        # print(1 / 0)
        customer = models.Customer.objects.all()
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