import json
from django.shortcuts import render
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from APPS.models import Employees, Category, Products, Sales, salesItems, masterApps, supplier,incomingGoodsItems,outletProudct,bast,bastItem
from datetime import datetime, date, timedelta
from django.db.models import Sum, Count
from django.db import connection as conn
import pandas as pd
import math
from .master import Master
from POS import cron
from django.contrib.auth.models import Group
from Auth.models import User
from django.contrib.auth.decorators import login_required,permission_required
@xframe_options_exempt

# Create your views here.
class Views:
    
    @login_required(login_url='/login')
    def home(request):
        user = User.objects.get(username=request.user)

        momkdd = user.get_group_permissions()
        # print(momkdd)
        PRODUK = {}
        PEMBELIAN = {}

        product_list = Products.objects.all().values('id', 'name')
        id_ = {}
        id_p = {}
        for n,i in enumerate(product_list):
            id_[n] = i['id']
            id_p[n] = i['name']
            
        PRODUK['id'] = id_
        PRODUK['id_p'] = id_p
        
        sales = salesItems.objects.all()
        p_id_ = {}
        p_id_p = {}
        p_count = {}
        for n,i in enumerate(sales):
            p_id_[n] = i.sale_id.id
            p_id_p[n] = i.product_id.name
            p_count[n] = i.qty
        
        PEMBELIAN['user'] = p_id_
        PEMBELIAN['id_p'] = p_id_p
        PEMBELIAN['coun'] = p_count
        
        df_product = pd.DataFrame(PRODUK)
        df_pembelian = pd.DataFrame(PEMBELIAN)
        
        df_product.to_csv('static/csv/produk.csv')
        df_pembelian.to_csv('static/csv/pembelian.csv')
        
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'
        
        return render(request, 'home/index.html', app_content)
        
    def dashboard(request):
        product_sold = 0
        
        # products = incomingGoodsItems.objects.aggregate(Sum('qty'))['qty__sum']
        products = incomingGoodsItems.objects.filter(statusPayment = 'Belum').all().count()
        query_set = Group.objects.filter(user = request.user).first()
        statusGrup='';
        if products:
            products = int(products)
        else:
            products = 0
        if request.user.is_superuser :
            statusGrup=""
        else :
             statusGrup="and group_id_id ="+str(query_set.id)
        mostStock = Products.objects.all().order_by('-stock')[:10].values('name', 'stock')
        with conn.cursor() as getTotalSales:
            returdata=str("Retur")
            getTotalSales.execute("""SELECT sum(grand_total) FROM "public"."APPS_sales" WHERE "statusRetur" is null and date_invoice::date = NOW()::date """+statusGrup)
            total_sales = getTotalSales.fetchall()[0][0]
            
        with conn.cursor() as getTransaction:
            getTransaction.execute("""SELECT count(id) FROM "public"."APPS_sales" WHERE "statusRetur" is null and date_invoice::date = NOW()::date """+statusGrup)
            transaction = getTransaction.fetchall()[0][0]
            
        with conn.cursor() as getSale:
            getSale.execute("""SELECT ap.name, sum(ass.qty) as tot FROM "public"."APPS_salesitems" ass JOIN "public"."APPS_products" ap ON ass.product_id_id = ap.id GROUP BY ap.name ORDER BY tot DESC LIMIT 10""")
            getSales = getSale.fetchall()
            
            
        with conn.cursor() as getProfit:
            getProfit.execute("""SELECT apsi.price,"APPS_products".price FROM "APPS_salesitems" apsi JOIN "APPS_sales" aps ON apsi.sale_id_id = aps.id join "APPS_products" on apsi.product_id_id = "APPS_products".id WHERE aps."statusRetur" is null and aps.date_invoice::date = NOW()::date and group_id_id = 5 """+statusGrup)
            total_profit = getProfit.fetchall()
        
        
        # print(total_profit_by_user)
        mostSold = []
        for i in getSales:
            tot = i[1]
            product_sold += tot
            mostSold.append({'label':i[0], 'total':int(tot)})

        getTotalOutletData = []
        grupdata = Group.objects.all();
        for idatagrop in grupdata:
            with conn.cursor() as getTotalOutlet:
                getTotalOutlet.execute("""SELECT SUM(total), SUM(price),auth_group.name FROM "APPS_salesitems" apsi JOIN "APPS_sales" aps ON apsi.sale_id_id = aps.id join auth_group on aps.group_id_id = auth_group.id WHERE aps."statusRetur" is null and aps.date_invoice::date = NOW()::date and auth_group.id="""+str(idatagrop.id)+""" GROUP BY auth_group.name""")
                getTotalOutlets = getTotalOutlet.fetchall()
                print(getTotalOutlets)
            if idatagrop.name !="CIBOGO":
                if getTotalOutlets== []:
                    getTotalOutletData.append({'id':idatagrop.id,'label':idatagrop.name, 'total':'Rp.0'})
                else:
                    for i in getTotalOutlets:
                        tot = 'Rp. {:,},-'.format(math.floor(i[1])).replace(',','.')  
                        # product_sold += tot
                        getTotalOutletData.append({'id':idatagrop.id,'label':idatagrop.name, 'total':(tot)})
            
        all_users = User.objects.all()
        mostUser = []
        for dataUser in all_users:
            datatotal=0
            with conn.cursor() as getProfitByUser:
                startdate = date.today()
                lastMonth = date.today().replace(day=1) - timedelta(days=1)
                if lastMonth.month <= 9 :
                    validdateMonth = '0'+str(lastMonth.month)
                    
                else :
                    validdateMonth = lastMonth.month
                if startdate.month <= 9:
                    getMonth = '0'+str(startdate.month)
                else:
                    getMonth = startdate.month
                # getProfitByUser.execute('SELECT "APPS_sales".id, "APPS_sales".grand_total FROM "APPS_sales" where extract (month FROM date_added) = extract (month FROM CURRENT_DATE) '+statusGrup+' and "APPS_sales".created_by_id = %s ' , [dataUser.id])
                if startdate.day > 15:
                    getProfitByUser.execute("""SELECT "APPS_sales".id, "APPS_sales".grand_total,"APPS_salesitems".price,"APPS_products".price AS productPrice FROM "APPS_sales" JOIN "APPS_salesitems" ON "APPS_sales".ID = "APPS_salesitems".sale_id_id JOIN "APPS_products" ON "APPS_salesitems".product_id_id = "APPS_products".ID where (to_char(date_invoice, 'yyyymmdd')   >= '"""+str(startdate.year)+""""""+str(getMonth)+""""""+str(16)+"""' and to_char(date_invoice, 'yyyymmdd')   <=  '"""+str(startdate.year)+""""""+str(getMonth+1)+""""""+str(15)+"""'  """+statusGrup+""") and "APPS_sales".created_by_id = """+str(dataUser.id)+""" and "APPS_sales"."statusRetur" is null """)
                else:
                    getProfitByUser.execute("""SELECT "APPS_sales".id, "APPS_sales".grand_total,"APPS_salesitems".price,"APPS_products".price AS productPrice FROM "APPS_sales" JOIN "APPS_salesitems" ON "APPS_sales".ID = "APPS_salesitems".sale_id_id JOIN "APPS_products" ON "APPS_salesitems".product_id_id = "APPS_products".ID where (to_char(date_invoice, 'yyyymmdd')   >= '"""+str(startdate.year)+""""""+str(validdateMonth)+""""""+str(16)+"""' and to_char(date_invoice, 'yyyymmdd')   <=  '"""+str(startdate.year)+""""""+str(getMonth)+""""""+str(15)+"""'  """+statusGrup+""") and "APPS_sales".created_by_id = """+str(dataUser.id)+""" and "APPS_sales"."statusRetur" is null """)
                total_profit_by_user = getProfitByUser.fetchall()
                for i in total_profit_by_user:
                    tot = i[2] - i[3]
                    datatotal += (tot * 0.1)
            if datatotal != None: 
                hasil = 'Rp. {:,},-'.format(math.floor(datatotal)).replace(',','.') 
            else: 
                hasil = 'Rp 0,-'

            if datatotal != 0: 
                mostUser.append({'label':dataUser.first_name +' '+ dataUser.last_name,'total': hasil})
        # print(mostUser)  
        # 1500000 - 
        # 150000
        
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'               
        app_content['js_inc'].append("plugins/chart.js/Chart.min.js")
        app_content['js_inc'].append("mycashier/js/action_dashboard.js")
        
        if total_sales != None:
            total_sales = 'Rp. {:,},-'.format(math.floor(total_sales)).replace(',','.')
        else:
            total_sales = 'Rp. 0,-'
        
        print(total_profit)
        totalAllProfit=0
        for xt in total_profit:
            print(xt[0])
            getProfit = xt[0] - xt[1]
            getUntungKaryawan = getProfit * 0.1
            totalAllProfit += getProfit - getUntungKaryawan
        if total_profit != None:
            total_profit = 'Rp. {:,},-'.format(totalAllProfit).replace(',','.')
        else:
            total_profit = 'Rp. 0,-'
            
        
        
        # calculate
        # print(getTotalOutletData)
        app_content['product_sold'] = int(product_sold)
        app_content['products'] = products
        app_content['transaction'] = math.floor(transaction)
        app_content['total_sales'] = total_sales
        app_content['mostSold'] = mostSold
        app_content['mostStock'] = mostStock
        app_content['pendapatanKaryawan'] = mostUser
        app_content['getTotalOutletData'] = getTotalOutletData
        app_content['total_profit'] = total_profit
        
        return render(request, 'pages/dashboard.html', app_content)
    def categoryList(request):

        category_list = Category.objects.all()
        
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'        
        app_content['js_inc'].append("mycashier/js/action_category.js")
        app_content['category'] = category_list
        
        return render(request, 'pages/listCategory.html', app_content)
    
    def productList(request):
        product_list = Products.objects.all()
        product_json = []
        for product in product_list:
            incomingGoodsItemsdata = incomingGoodsItems.objects.filter(product_id = product.id,statusPayment = 'Belum').all().count()
            product_json.append({'id':product.id,'category_id':product.category_id.name,'modal':product.price,'status':product.status, 'name':product.name, 'price':product.price, 'selling_price':product.selling_price,'stock':incomingGoodsItemsdata})
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'
        app_content['js_inc'].append("mycashier/js/action_product.js")        
        app_content['products'] = product_json        
        
        return render(request, 'pages/listProduct.html', app_content)
    
    def cashier(request):
        cur_date = datetime.today().strftime('%A, %d/%m/%y')
        
        products = Products.objects.filter(status = 1)
        kategori = Category.objects.filter(status = 1)
        all_users = User.objects.filter(is_superuser = 0)
        product_json = []
        user_json = []
        query_set = Group.objects.filter(user = request.user).first()
        for product in products:
            # print(product.price)
            incomingGoodsItemsdata = incomingGoodsItems.objects.filter(group_id = query_set,product_id = product.id,statusPayment = "Belum").all().count()
            dataSerialNumberArr=[]
            incomingGoodsItemsdata2 = incomingGoodsItems.objects.filter(group_id = query_set,product_id = product.id,statusPayment = "Belum").all()
            for incomingGoodsItemsdatalop in incomingGoodsItemsdata2:
                if incomingGoodsItemsdatalop.serial_number is not None:
                    dataSerialNumberArr.append({'serial_number':incomingGoodsItemsdatalop.serial_number})
            if(incomingGoodsItemsdata != 0):
                product_json.append({'id':product.id, 'name':product.name, 'price':product.price, 'selling_price':product.selling_price,'stock':incomingGoodsItemsdata,'dataSerialNumber':dataSerialNumberArr})


        for all_user in all_users:
            user_json.append({'id':all_user.id,'name':all_user.first_name})
        dataTypePayment=[]
        dataTypePayment.append({'name':'CASH'})
        dataTypePayment.append({'name':'BRI'})
        dataTypePayment.append({'name':'MANDIRI'})
        dataTypePayment.append({'name':'BCA'})
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'    
        app_content['products'] = product_json
        app_content['all_users'] = all_users
        app_content['product_json'] = (product_json)
        app_content['user_json'] = (user_json)
        app_content['category'] = kategori
        app_content['dataTypePayment'] = dataTypePayment
        app_content['date'] = cur_date
        app_content['js_inc'].append("mycashier/js/action_cashier.js")
        
        return render(request, 'pages/cashier.html', app_content)
    
    def createCardStok(request):
        cur_date = datetime.today().strftime('%A, %d/%m/%y')
        products = Products.objects.filter(status = 1)
        kategori = Category.objects.filter(status = 1)
        all_users = Group.objects.all()
        product_json = []
        user_json = []
        query_set = Group.objects.filter(user = request.user).first()
        for product in products:
            # print(product.price)
            # product_json.append({'id':product.id, 'name':product.name, 'price':product.price, 'selling_price':product.selling_price,'stock':product.stock})
            if query_set.id == 2: 
                incomingGoodsItemsdata = incomingGoodsItems.objects.filter(group_id=query_set,product_id = product.id,statusPayment = "Belum").all().count()
                dataSerialNumberArr=[]
                incomingGoodsItemsdata2 = incomingGoodsItems.objects.filter(group_id=query_set,product_id = product.id,statusPayment = "Belum").all()
                for incomingGoodsItemsdatalop in incomingGoodsItemsdata2:
                    if incomingGoodsItemsdatalop.serial_number is not None:
                        dataSerialNumberArr.append({'serial_number':incomingGoodsItemsdatalop.serial_number})
            else : 
                incomingGoodsItemsdata = incomingGoodsItems.objects.filter(group_id=query_set,product_id = product.id,statusPayment = "Belum").all().count()
                dataSerialNumberArr=[]
                incomingGoodsItemsdata2 = incomingGoodsItems.objects.filter(group_id=query_set,product_id = product.id,statusPayment = "Belum").all()
                for incomingGoodsItemsdatalop in incomingGoodsItemsdata2:
                    if incomingGoodsItemsdatalop.serial_number is not None:
                        dataSerialNumberArr.append({'serial_number':incomingGoodsItemsdatalop.serial_number})
            if(incomingGoodsItemsdata != 0):
                product_json.append({'id':product.id, 'name':product.name, 'price':product.price, 'selling_price':product.price,'stock':incomingGoodsItemsdata,'dataSerialNumber':dataSerialNumberArr})

        for all_user in all_users:
            user_json.append({'id':all_user.id,'name':all_user.name})
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'    
        app_content['products'] = product_json
        app_content['all_users'] = all_users
        app_content['product_json'] = (product_json)
        app_content['user_json'] = (user_json)
        app_content['category'] = kategori
        app_content['category'] = kategori
        app_content['date'] = cur_date
        app_content['js_inc'].append("mycashier/js/action_cardStock.js")
        
        return render(request, 'pages/createCardStok.html', app_content)

    def incomingGoods(request):
        cur_date = datetime.today().strftime('%A, %d/%m/%y')

        products = Products.objects.filter(status = 1)
        kategori = Category.objects.filter(status = 1)
    
        product_json = []
        for product in products:
            product_json.append({'id':product.id, 'name':product.name, 'price':float(product.price),'code':product.code})

        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'    
        app_content['products'] = products
        app_content['product_json'] = (product_json)
        app_content['category'] = kategori
        app_content['date'] = cur_date
        app_content['js_inc'].append("mycashier/js/action_incomingGoods.js")

        return render(request, 'pages/incomingGoods.html', app_content)
    
    def sales(request):
        
        query_set = Group.objects.filter(user = request.user).first()
        # print(query_set)
        if query_set == None:
            
            sales = Sales.objects.all()
        else:
            
            sales = Sales.objects.filter(group_id = query_set).all()
        sale_data = []
        for sale in sales:
            
            data = {}
            data['first_name'] = sale.created_by.first_name
            data['last_name'] = sale.created_by.last_name
            # print(sale.created_by.last_name)
            for field in sale._meta.get_fields(include_parents=False):
                # all_users = User.objects.filter(id = field.created_by).all()
                # if field.created_by != "":
                

                if field.related_model is None:
                    data[field.name] = getattr(sale,field.name)
            data['items'] = salesItems.objects.filter(sale_id = sale).all()
            data['item_count'] = len(data['items'])
            if 'tax_amount' in data:
                data['tax_amount'] = format(float(data['tax_amount']),'.2f')
            # print(data)
            sale_data.append(data)
        
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'
        app_content['sale_data'] = sale_data
        
        app_content['js_inc'].append("mycashier/js/action_sales.js")


        return render(request, 'pages/sales.html', app_content)
    
    def outletProudct(request):
        # print(request.user.groups);
        # query_set = Group.objects.filter(user = request.user).first()
        outletProudcts = outletProudct.objects.filter(created_by = request.user.id).all()
        
        sale_data = []
        for sale in outletProudcts:
            
            data = {}
            # data['first_name'] = sale.created_by.first_name
            # data['last_name'] = sale.created_by.last_name
            # print(sale.created_by.last_name)
            for field in sale._meta.get_fields(include_parents=False):
                # all_users = User.objects.filter(id = field.created_by).all()
                # if field.created_by != "":
                

                if field.related_model is None:
                    data[field.name] = getattr(sale,field.name)
            data['items'] = incomingGoodsItems.objects.filter(outletProduct_id = sale).all()
            data['item_count'] = len(data['items'])
            # if 'tax_amount' in data:
            #     data['tax_amount'] = format(float(data['tax_amount']),'.2f')
            # print(data)
            sale_data.append(data)
        
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'
        app_content['sale_data'] = sale_data
        # print('asdasd')
        # print(sale_data)
        app_content['js_inc'].append("mycashier/js/action_outletProudct.js")


        return render(request, 'pages/outletProudct.html', app_content)

    def bast(request):
        # print(request.user.groups);
        # query_set = Group.objects.filter(user = request.user).first()
        basts = bast.objects.filter(created_by = request.user.id).all()
        
        sale_data = []
        for sale in basts:
            
            data = {}
            # data['first_name'] = sale.created_by.first_name
            # data['last_name'] = sale.created_by.last_name
            # print(sale.created_by.last_name)
            for field in sale._meta.get_fields(include_parents=False):
                # all_users = User.objects.filter(id = field.created_by).all()
                # if field.created_by != "":
                

                if field.related_model is None:
                    data[field.name] = getattr(sale,field.name)
            data['items'] = bastItem.objects.filter(bast_id = sale).all()
            data['item_count'] = len(data['items'])
            # if 'tax_amount' in data:
            #     data['tax_amount'] = format(float(data['tax_amount']),'.2f')
            # print(data)
            sale_data.append(data)
        
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'
        app_content['sale_data'] = sale_data
        # print('asdasd')
        # print(sale_data)
        app_content['js_inc'].append("mycashier/js/action_bast.js")


        return render(request, 'pages/bast.html', app_content)

    def invoice(request):
        
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'
 
        return render(request, 'pages/invoice.html', app_content)    
    
    
    def supplierList(request):
        supplier_list = supplier.objects.all()
        
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'        
        app_content['js_inc'].append("mycashier/js/action_supplier.js")
        app_content['supplier'] = supplier_list
        
        return render(request, 'pages/listSupplier.html', app_content)

    def totalStock(request):
        supplier_list = supplier.objects.all()
        products = Products.objects.filter(status = 1)
        grups = Group.objects.all()
        categorys = Category.objects.all()
        app_content = Master.getApps()
        query_set = Group.objects.filter(user = request.user).first()
        app_content['layout'] = 'layout/layout_content.html'        
        app_content['js_inc'].append("mycashier/js/action_totalStock.js")
        app_content['products'] = products
        app_content['group_id'] = query_set.id
        app_content['grups'] = grups
        app_content['categorys'] = categorys
        
        return render(request, 'pages/totalStock.html', app_content)

    def detailPajak(request):
        id = request.GET.get('id')
        # print(/)
        sale = Sales.objects.filter(id = 15)
        respone=[]
        totalProductQty = []
        for data in sale:
            respone.append({
                'FK':"FK",
                'KD_JENIS_TRANSAKSI':"",
                'FG_PENGGANTI':"",
                'NOMOR_FAKTUR':"",
                'MASA_PAJAK':data.date_added.strftime("%m"),
                'TAHUN_PAJAK':data.date_added.year,
                'TANGGAL_FAKTUR':data.date_added.strftime("%m")+"/"+data.date_added.strftime("%m")+"/"+data.date_added.strftime("%Y"),
                'NPWP':data.npwp,
                'NAMA':data.nameCustomer,
                'ALAMAT_LENGKAP':"",
                'JUMLAH_DPP':int(data.grand_total) - int(data.ppn),
                'JUMLAH_PPN':int(data.grand_total),
                'JUMLAH_PPNBM':"",
                'ID_KETERANGAN_TAMBAHAN':"",
                'FG_UANG_MUKA':"",
                'UANG_MUKA_DPP':"",
                'UANG_MUKA_PPN':"",
                'UANG_MUKA_PPNBM':"",
                'REFERENSI':"",
                'KDOE_DOKUMEN_PENDUKUNG':"",
                })
            with conn.cursor() as getTotalQty:
                getTotalQty.execute("""SELECT product_id_id,sale_id_id,"APPS_products".name,COUNT ( product_id_id ) as qty,SUM(total) AS sum_of_duplicates,"APPS_salesitems".price FROM "APPS_salesitems" JOIN "APPS_products" ON "APPS_products".id = "APPS_salesitems".product_id_id WHERE sale_id_id = 15 GROUP BY product_id_id, sale_id_id , "APPS_products".name,"APPS_salesitems".price HAVING COUNT ( product_id_id ) > 0 ORDER BY COUNT ( product_id_id );""")
                totalProductQty = getTotalQty.fetchall()
                    
            for dataItem in totalProductQty :
                # print(dataItem[2])
                total =dataItem[4] / 1.11
                totalPPn = round(total) * 0.11
                respone.append({
                    'FK':"OF",
                    'KD_JENIS_TRANSAKSI':"",
                    'FG_PENGGANTI':dataItem[2],
                    'NOMOR_FAKTUR':int(dataItem[5]),
                    'MASA_PAJAK':dataItem[3],
                    'TAHUN_PAJAK':int(dataItem[4]),
                    'TANGGAL_FAKTUR':0,
                    'NPWP':round(total),
                    'NAMA':int(totalPPn) + round(total),
                    'ALAMAT_LENGKAP':"",
                    'JUMLAH_DPP':"",
                    'JUMLAH_PPN':"",
                    'JUMLAH_PPNBM':"",
                    'ID_KETERANGAN_TAMBAHAN':"",
                    'FG_UANG_MUKA':"",
                    'UANG_MUKA_DPP':"",
                    'UANG_MUKA_PPN':"",
                    'UANG_MUKA_PPNBM':"",
                    'REFERENSI':"",
                    'KDOE_DOKUMEN_PENDUKUNG':"",
                    })
        # print(respone)
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'        
        app_content['js_inc'].append("mycashier/js/action_detailPajak.js")
        app_content['supplier'] = respone
        
        return render(request, 'pages/detailPajak.html', app_content)

    def cash(request):
        supplier_list = supplier.objects.all()
        
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'        
        app_content['js_inc'].append("mycashier/js/action_supplier.js")
        app_content['supplier'] = supplier_list
        
        return render(request, 'pages/cash.html', app_content)

    def createBast(request):
        cur_date = datetime.today().strftime('%A, %d/%m/%y')
        products = Products.objects.filter(status = 1)
        kategori = Category.objects.filter(status = 1)
        all_users = Group.objects.all()
        product_json = []
        user_json = []
        query_set = Group.objects.filter(user = request.user).first()
        for product in products:
            # print(product.price)
            # product_json.append({'id':product.id, 'name':product.name, 'price':product.price, 'selling_price':product.selling_price,'stock':product.stock})
            if query_set.id == 2: 
                incomingGoodsItemsdata = incomingGoodsItems.objects.filter(group_id=query_set,product_id = product.id,statusPayment = "Belum").all().count()
                dataSerialNumberArr=[]
                incomingGoodsItemsdata2 = incomingGoodsItems.objects.filter(group_id=query_set,product_id = product.id,statusPayment = "Belum").all()
                for incomingGoodsItemsdatalop in incomingGoodsItemsdata2:
                    if incomingGoodsItemsdatalop.serial_number is not None:
                        dataSerialNumberArr.append({'serial_number':incomingGoodsItemsdatalop.serial_number})
            else : 
                incomingGoodsItemsdata = incomingGoodsItems.objects.filter(group_id=query_set,product_id = product.id,statusPayment = "Belum").all().count()
                dataSerialNumberArr=[]
                incomingGoodsItemsdata2 = incomingGoodsItems.objects.filter(group_id=query_set,product_id = product.id,statusPayment = "Belum").all()
                for incomingGoodsItemsdatalop in incomingGoodsItemsdata2:
                    if incomingGoodsItemsdatalop.serial_number is not None:
                        dataSerialNumberArr.append({'serial_number':incomingGoodsItemsdatalop.serial_number})
            if(incomingGoodsItemsdata != 0):
                product_json.append({'id':product.id, 'name':product.name, 'price':product.price, 'selling_price':product.selling_price,'stock':incomingGoodsItemsdata,'dataSerialNumber':dataSerialNumberArr})

        for all_user in all_users:
            user_json.append({'id':all_user.id,'name':all_user.name})
        app_content = Master.getApps()
        app_content['layout'] = 'layout/layout_content.html'    
        app_content['products'] = product_json
        app_content['all_users'] = all_users
        app_content['product_json'] = (product_json)
        app_content['user_json'] = (user_json)
        app_content['category'] = kategori
        app_content['category'] = kategori
        app_content['date'] = cur_date
        app_content['js_inc'].append("mycashier/js/action_createBast.js")
        
        return render(request, 'pages/createBast.html', app_content)
