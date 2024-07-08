from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Category, Products, Sales, salesItems, supplier, martDataSales,incomingGoodsItems,incomingGoods, tableTrans,outletProudct,outletProudctItem,bast,bastItem
from django.contrib import messages
import json, sys
from datetime import datetime, date, timedelta
from django.db.models import Sum, Avg
from django.db import connection as conn
import math
from django.contrib.auth.models import Group
from Auth.models import User

# Helper Function
def generateId(mods):
    cur_date = int(datetime.today().strftime('%Y%m%d'))
    prev_id = mods.objects.filter(id__startswith=cur_date).values('id')

    if len(prev_id) == 0:
        cek_id = int(str(cur_date)+'000')
        id = cek_id + 1

    elif len(prev_id) == 1:
        id = prev_id[0]['id'] + 1
    
    else:
        id = prev_id.last()['id'] + 1
    
    return id

def getdataHarian(param,grop,super,group_filter):
    startdate = date.today()
    enddate = startdate - timedelta(days=15)
    if super =='ya':
        if group_filter !='None':
            total = int(Sales.objects.filter(group_id=group_filter).aggregate(Sum(param))[param+'__sum'])
            aver = int(Sales.objects.filter(group_id=group_filter).aggregate(Avg(param))[param+'__avg'])
            dataInfoSales = Sales.objects.filter(date_invoice__range=[enddate, startdate],group_id=group_filter,statusRetur__isnull=True).values('date_invoice').order_by('date_invoice').annotate(sum=Sum(param))

        else:
            total = int(Sales.objects.aggregate(Sum(param))[param+'__sum'])
            aver = int(Sales.objects.aggregate(Avg(param))[param+'__avg'])
            dataInfoSales = Sales.objects.filter(date_invoice__range=[enddate, startdate],statusRetur__isnull=True).values('date_invoice').order_by('date_invoice').annotate(sum=Sum(param))
    else :
        
        total = int(Sales.objects.filter(group_id=grop).aggregate(Sum(param))[param+'__sum'])
        aver = int(Sales.objects.filter(group_id=grop).aggregate(Avg(param))[param+'__avg'])
        dataInfoSales = Sales.objects.filter(date_invoice__range=[enddate, startdate],group_id=grop,statusRetur__isnull=True).values('date_invoice').order_by('date_invoice').annotate(sum=Sum(param))

    ind = []
    label = []
    data_ = []
    avg_ = []
        
    for n,i in enumerate(dataInfoSales):
        
        lb = i['date_invoice'].strftime('%d-%m-%Y')
        dt = i['sum']
        
        label.append(lb)
        data_.append(dt)
        
        if n == 0:
            avg_.append(int(dt))
        elif n == 1:
            av = int(sum(data_[-2:])/2)
            avg_.append(av)
        else:
            av = int(sum(data_[-3:])/3)
            avg_.append(av)
            
    res = {
        'total' : total,
        'aver'  : aver,
        'label' : label,
        'data_' : data_,
        'avg_'  : avg_
        
    }
    
    return res


def getDataBulanan(param):
    query_set = Group.objects.filter(user = request.user).first()
    with conn.cursor() as dataMon:
        dataMon.execute("""
                        SELECT TO_CHAR(date_trunc('month', date_invoice), 'MON-YYYY') AS month, sum("""+param+""") as total
                        FROM "APPS_sales" where group_id_id = """+query_set+"""
                        GROUP BY date_trunc('month', date_invoice) ORDER BY date_trunc('month', date_invoice) ASC limit 15""")
        dataMonth = dataMon.fetchall()
    
    # for i in dataMonth:
    label = []
    data_ = []
    avg_ = []
    
    for n,i in enumerate(dataMonth):
        
        lb = i[0]
        dt = i[1]
        
        label.append(lb)
        data_.append(dt)
        
        if n == 0:
            avg_.append(int(dt))
        elif n == 1:
            av = int(sum(data_[-2:])/2)
            avg_.append(av)
        else:
            av = int(sum(data_[-3:])/3)
            avg_.append(av)

    res = {
        'label' : label,
        'data_' : data_,
        'avg_'  : avg_
        
    }
    
    return res

# / Helper Function

# Category
# @login_required
def manage_category(request):
    category = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            category = Category.objects.filter(id=id).first()
    
    context = {
        'category' : category,
        'layout'   : 'layout/layout_content.html'
    }
    return render(request, 'helper/manage_category.html',context)

def createInvoiceByBast(request):
    category = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            category = bastItem.objects.filter(bast_id=id)
    
    context = {
        'category' : category,
        'layout'   : 'layout/layout_content.html'
    }
    return render(request, 'helper/createInvoiceByBast.html',context)

def manage_change_sn(request):
    category = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            incomingGoodsItemsdata = incomingGoodsItems.objects.filter(id=id).first()
    query_set = Group.objects.filter(user = request.user).first()
    context = {
        'category' : incomingGoodsItemsdata,
        # 'group_id' : query_set.id,
        'layout'   : 'layout/layout_content.html'
    }
    return render(request, 'helper/manage_change_sn.html',context)

# @login_required
def save_category(request):
    data =  request.POST
    resp = {'status':'failed'}
    
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            # print(request.user)
            save_category = Category.objects.filter(id = data['id']).update(name=data['name'].upper(), description = data['description'],status = data['status'])
        else:
            save_category = Category(name=data['name'].upper(), description = data['description'],status = data['status'], created_by = 'user')
            save_category.save()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

def updatesn(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_category = incomingGoodsItems.objects.filter(id = data['id']).update(serial_number=data['name'].upper())
        resp['status'] = 'success'
        messages.success(request, 'Serial Number Successfully Updated.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# @login_required
def delete_category(request):
    data =  request.GET
    resp = {'status':''}
    try:
        Category.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


# Products
# @login_required
def manage_products(request):
    product = {}
    categories = Category.objects.filter(status = 1).all()
    suppliers = supplier.objects.all()
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()
    
    context = {
        'product' : product,
        'suppliers' : suppliers,
        'categories' : categories
    }
    return render(request, 'helper/manage_product.html',context)

# @login_required
def save_product(request):
    data =  request.POST
    resp = {'status':'failed'}
    dataimage = request.FILES 
    # print(request.FILES['image'])
    id= ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=id).all()
    else:
        check = Products.objects.filter(code=id).all()
    if len(check) > 0 :
        resp['msg'] = "Product Code Already Exists in the database"
    else:
        category = Category.objects.filter(id = data['category_id']).first()
        suppliers = supplier.objects.filter(id = data['supplier_id']).first()
        
        sell_price = data['price']
        # print(float(data['selling_price'])/100, type(data['selling_price']))
        if data['selling_price_id'] == 'nominal':
            sell_price = data['selling_price']
        
        if data['selling_price_id'] == 'percent':
            
            sell_price = float(data['price'])+((float(data['selling_price'])/100)*float(data['price']))
        
        if data['selling_price_id'] == 'margin':
            sell_price = float(data['price'])+float(data['selling_price'])
        
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                save_product = Products.objects.filter(id = data['id']).update(code=id,supplier_id=suppliers, category_id=category, name=data['name'].upper(), description = data['description'], price = float(data['price']), selling_price = sell_price,status = data['status'],image=request.FILES['image'])
            else:
                # print(generateId(Products))
                dataID=generateId(Products)
                save_product = Products(id= dataID,code= str(dataID), category_id=category, supplier_id=suppliers, name=data['name'].upper(), description = data['description'], price = float(data['price']), selling_price = sell_price, status = data['status'],image=request.FILES['image'])
                # print(save_product)
                save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Product Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# @login_required
def delete_product(request):
    data =  request.GET
    resp = {'status':''}
    # try:
    dataDelete = Products.objects.filter(id = data['id']).delete()
    print('asdsadasd')
    resp['status'] = 'success'
    messages.success(request, 'Product Successfully deleted.')
    # except:
        # resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


# Supplier
# @login_required
def manage_supplier(request):
    Supplier = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            Supplier = supplier.objects.filter(id=id).first()
    
    context = {
        'supplier' : Supplier,
        'layout'   : 'layout/layout_content.html'
    }
    return render(request, 'helper/manage_supplier.html',context)

# @login_required
def save_supplier(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_supplier = supplier.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
        else:
            save_supplier = supplier(name=data['name'], description = data['description'],status = data['status'], created_by = request.user)
            save_supplier.save()
        resp['status'] = 'success'
        messages.success(request, 'Supplier Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# @login_required
def delete_supplier(request):
    data =  request.GET
    resp = {'status':''}
    try:
        supplier.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# @login_required
def checkout_modal(request):
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total' : grand_total,
    }
    return render(request, 'helper/checkout.html',context)

# @login_required
def save_cashier(request):
    resp = {'status':'failed','msg':''}
    data = request.POST
    momok = json.loads(data['data'])
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = Sales.objects.filter(code = str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)
    # try:
    dataPPNTotal=0
    getPPN=0
    if data['statusPPN'] == "Ya":
        getPPN = int(data['subtotal'])*float(0.11)
        dataPPNTotal = int(data['subtotal']) + float(getPPN)
        
    else:
        dataPPNTotal = data['grandtotal']
        
    
    # print('momok')
    query_set = Group.objects.filter(user = request.user).first()
    sales = Sales(code=code, sub_total = data['subtotal'], tax = 0, tax_amount = 0, grand_total = float(dataPPNTotal), tendered_amount = data['tendered_amount'], amount_change = data['amount_change'], created_by_id = data['id_user'],nameCustomer=data['nameCustomer'],phoneCustomer=data['phoneCustomer'],statusPPN=data['statusPPN'],npwp=data['npwp'],ppn=int(getPPN),group_id = query_set,date_invoice=data['date'],typePayment=data['typePayment']).save()
    sale_id = Sales.objects.last().pk
    
    i = 0
    for prod in momok:
        # print(range(momok[0]['qty']))
        zvx = 0
        sale = Sales.objects.filter(id=sale_id).first()
        product = Products.objects.filter(id=momok[i]['id']).first()
        # productGet = Products.objects.filter(id=momok[i]['id']).all().values('stock')
        for x in range(momok[i]['qty']):
            query_set = Group.objects.filter(user = request.user).first()
            if momok[i]['dataSerialNumberzzzzxxx'] == 0 :
                incomingGoodsItemsdata = incomingGoodsItems.objects.filter(group_id = query_set,statusPayment = "Belum",product_id = product).all()
            else :    
                incomingGoodsItemsdata = incomingGoodsItems.objects.filter(group_id = query_set,statusPayment = "Belum",product_id = product,serial_number = momok[i]['dataSerialNumberzzzzxxx'][zvx]).all()
            salesItems(sale_id = sale, product_id = product, qty =1 ,serial_number=incomingGoodsItemsdata[0].serial_number, price =momok[i]['selling_price'] , total = momok[i]['total'], incomingGoodsItems_id= incomingGoodsItemsdata[0]).save()
            # print('asdasdada')
            incomingGoodsItems.objects.filter(id = incomingGoodsItemsdata[0].id).update(statusPayment = "Sudah")
            zvx += int(1)
        i += int(1)
    resp['status'] = 'success'
    resp['sale_id'] = sale_id
    messages.success(request, "Sale Record has been saved.")
    # except:
    #     resp['msg'] = "An error occured"
    #     print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp),content_type="application/json")
def save_cardStok(request):
    resp = {'status':'failed','msg':''}
    data = request.POST
    momok = json.loads(data['data'])
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = outletProudct.objects.filter(code = str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)
    # try:
    incomingGoodss = outletProudct(code=code, sub_total = data['subtotal'], tax = 0, tax_amount = 0, grand_total = data['grandtotal'], tendered_amount = data['tendered_amount'], amount_change = data['amount_change'], created_by = request.user.id,date_invoice=data['date_invoice']).save()
    incomingGoods_id = outletProudct.objects.last().pk
    
    i = 0
    for prod in momok:
        zvx = 0
        incoming = outletProudct.objects.filter(id=incomingGoods_id).first()
        product = Products.objects.filter(id=momok[i]['id']).first()
        productGet = Products.objects.filter(id=momok[i]['id']).all().values('stock')
        productId = Products.objects.filter(id=momok[i]['id']).all().values('id')
        for x in range(momok[i]['qty']):
            if momok[i]['dataSerialNumberzzzzxxx'] == 0 :
                query_set = Group.objects.filter(user = request.user).first()
                incomingGoodsItemsdata = incomingGoodsItems.objects.filter(product_id = momok[i]['id'], group_id=query_set, statusPayment="Belum").all()
            else :    
                incomingGoodsItemsdata = incomingGoodsItems.objects.filter(product_id = momok[i]['id'],serial_number = momok[i]['dataSerialNumberzzzzxxx'][zvx],statusPayment="Belum").all()

            save_producxts = Products.objects.filter(id = momok[i]['id']).update(stock=(productGet[0]['stock'] - 1))
            query_set2 = Group.objects.filter(id = data['id_user']).first()

            outletProudctItem(outletProduct_id = incoming, product_id = product, qty =1 ,serial_number=incomingGoodsItemsdata[0].serial_number, price =momok[i]['selling_price'] , total = momok[i]['total'], incomingGoodsItems_id= incomingGoodsItemsdata[0],group_id=query_set2).save()

            save_products = incomingGoodsItems.objects.filter(id = incomingGoodsItemsdata[0].id).update(group_id=query_set2,outletProduct_id = incoming)
            
            
            zvx +=int(1)
        i += int(1)
    resp['status'] = 'success'
    resp['sale_id'] = incomingGoods_id
    messages.success(request, "Sale Record has been saved.")
    # except:
    #     resp['msg'] = "An error occured"
        # print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp),content_type="application/json")

def save_bast(request):
    resp = {'status':'failed','msg':''}
    data = request.POST
    momok = json.loads(data['data'])
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = bast.objects.filter(code = str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)
    # try:
    incomingGoodss = bast(code=code, sub_total = data['subtotal'], tax = 0, tax_amount = 0, grand_total = data['grandtotal'], tendered_amount = data['tendered_amount'], amount_change = data['amount_change'], created_by = request.user.id,date_invoice=data['date_invoice'],nameCustomer=data['nameCustomer'],phoneCustomer=data['phoneCustomer'],address=data['address']).save()
    incomingGoods_id = bast.objects.last().pk
    
    i = 0
    for prod in momok:
        zvx = 0
        incoming = bast.objects.filter(id=incomingGoods_id).first()
        product = Products.objects.filter(id=momok[i]['id']).first()
        productGet = Products.objects.filter(id=momok[i]['id']).all().values('stock')
        productId = Products.objects.filter(id=momok[i]['id']).all().values('id')
        for x in range(momok[i]['qty']):
            if momok[i]['dataSerialNumberzzzzxxx'] == 0 :
                query_set = Group.objects.filter(user = request.user).first()
                incomingGoodsItemsdata = incomingGoodsItems.objects.filter(product_id = momok[i]['id'],group_id=query_set).all()
            else :    
                incomingGoodsItemsdata = incomingGoodsItems.objects.filter(product_id = momok[i]['id'],serial_number = momok[i]['dataSerialNumberzzzzxxx'][zvx]).all()

            # save_producxts = Products.objects.filter(id = momok[i]['id']).update(stock=(productGet[0]['stock'] - 1))

            bastItem(bast_id = incoming, product_id = product, qty =1 ,serial_number=incomingGoodsItemsdata[0].serial_number, price =momok[i]['selling_price'] , total = momok[i]['total'], incomingGoodsItems_id= incomingGoodsItemsdata[0]).save()

            save_products = incomingGoodsItems.objects.filter(id = incomingGoodsItemsdata[0].id).update(statusPayment = "BAST")
            
            
            zvx +=int(1)
        i += int(1)
    resp['status'] = 'success'
    resp['sale_id'] = incomingGoods_id
    messages.success(request, "Sale Record has been saved.")
    # except:
    #     resp['msg'] = "An error occured"
        # print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp),content_type="application/json")

def save_incoming_goods(request):
    resp = {'status':'failed','msg':''}
    data = request.POST
    momok = json.loads(data['data'])
    dataSerial = json.loads(data['serialNumber'])
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = incomingGoods.objects.filter(code = str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)
    
    # try:
    incomingGoodss = incomingGoods(code=code, sub_total = data['subtotal'], tax = 0, tax_amount = 0, grand_total = data['grandtotal'], tendered_amount = data['tendered_amount'], amount_change = data['amount_change']).save()
    incomingGoods_id = incomingGoods.objects.last().pk
    
    i = 0
    for prod in momok:
        incoming = incomingGoods.objects.filter(id=incomingGoods_id).first()
        product = Products.objects.filter(id=momok[i]['id']).first()
        
        productGet = Products.objects.filter(id=momok[i]['id']).all().values('stock')
        productId = Products.objects.filter(id=momok[i]['id']).all().values('id')

        # print(incoming);
        
        save_products = Products.objects.filter(id = momok[i]['id']).update(stock=(productGet[0]['stock'] + momok[i]['qty']))
        # print('masukpak')
        query_set = Group.objects.filter(user = request.user).first()
        if dataSerial[i] != "" :
            incomingGoodsItems(incomingGoods_id = incoming, product_id = product, qty =momok[i]['qty'] , price =momok[i]['price'] , total =momok[i]['total'],serial_number=dataSerial[i], group_id = query_set).save()
        else :
             for x in range(momok[i]['qty']):
                incomingGoodsItems(incomingGoods_id = incoming, product_id = product, qty =1 , price =momok[i]['price'] , total =momok[i]['total'], group_id = query_set).save()
        
        i += 1
        
    resp['status'] = 'success'
    resp['sale_id'] = incomingGoods_id
    messages.success(request, "Sale Record has been saved.")
    # except:
    #     resp['msg'] = "An error occured"
    #     print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp),content_type="application/json")

# @login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id = id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales,field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemLists = salesItems.objects.filter(sale_id = sales,serial_number__isnull=True).all().distinct('product_id')
    ItemListsSerial = salesItems.objects.filter(sale_id = sales,serial_number__isnull=False).all().distinct('product_id')
    ItemList=[];
    for datalist2 in ItemListsSerial : 
        dataSerialNumber=[]
        ItemListsSerialQty = salesItems.objects.filter(sale_id = sales,product_id=datalist2.product_id).all()
        print(len(ItemListsSerialQty))
        for dataListSerialNumber in ItemListsSerialQty:
            dataSerialNumber.append(dataListSerialNumber.serial_number)
        ItemList.append({"product_id":datalist2.product_id,"qty":int(len(ItemListsSerialQty)),"serial_number":dataSerialNumber,"price":datalist2.price,"total":datalist2.total})
    for datalist in ItemLists : 
        itemFirst = salesItems.objects.filter(sale_id = sales,product_id = datalist.product_id,serial_number__isnull=True).all().count()
        ItemList.append({"product_id":datalist.product_id,"qty":itemFirst,"serial_number":"","price":datalist.price,"total":datalist.price * itemFirst})
   
    print(sales.created_by.phone)
    # datauser = User.objects.filter(username = sales.created_by).first()
    # print(sales.created_by.first_name)
    context = {
        "transaction" : transaction,
        "salesItems" : ItemList,
        "nameSales": sales.created_by.first_name,
        "phoneSales": sales.created_by.phone
    }

    return render(request, 'helper/receipt.html',context)
def kwitansi(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id = id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales,field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = salesItems.objects.filter(sale_id = sales).all()
    # datauser = User.objects.filter(username = sales.created_by).first()
    # print(sales.created_by.first_name)
    context = {
        "transaction" : transaction,
        "salesItems" : ItemList,
        "nameSales": sales.created_by.first_name
    }

    return render(request, 'helper/kwitansi.html',context)
    
def receipt_outletProduct(request):
    id = request.GET.get('id')
    outletProudctx = outletProudct.objects.filter(id = id).first()
    transaction = {}
    for field in outletProudctx._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(outletProudctx,field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    # ItemLists = incomingGoodsItems.objects.filter(outletProduct_id = outletProudctx).all().distinct('product_id')
    ItemLists = outletProudctItem.objects.filter(outletProduct_id = outletProudctx,serial_number__isnull=True).all().distinct('product_id')
    ItemListsSerial = outletProudctItem.objects.filter(outletProduct_id = outletProudctx,serial_number__isnull=False).all()
    ItemList=[];
    for datalist2 in ItemListsSerial : 
        ItemList.append({"product_id":datalist2.product_id,"qty":int(datalist2.qty),"serial_number":datalist2.serial_number,"price":datalist2.price,"total":datalist2.total,"group_id":datalist2.group_id})
        
    for datalist in ItemLists : 
        itemFirst = outletProudctItem.objects.filter(outletProduct_id = outletProudctx,product_id = datalist.product_id,serial_number__isnull=True).all().count()
        ItemList.append({"product_id":datalist.product_id,"qty":itemFirst,"serial_number":"","price":datalist.price,"total":datalist.price * itemFirst,"group_id":datalist.group_id})
    context = {
        "transaction" : transaction,
        "salesItems" : ItemList,
        "namaOutlet":ItemList[0]['group_id']
    }

    return render(request, 'helper/receiptOutlet.html',context)

def receipt_bast(request):
    id = request.GET.get('id')
    outletProudctx = bast.objects.filter(id = id).first()
    transaction = {}
    for field in outletProudctx._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(outletProudctx,field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    # ItemLists = incomingGoodsItems.objects.filter(outletProduct_id = outletProudctx).all().distinct('product_id')
    ItemLists = bastItem.objects.filter(bast_id = outletProudctx,serial_number__isnull=True).all().distinct('product_id')
    ItemListsSerial = bastItem.objects.filter(bast_id = outletProudctx,serial_number__isnull=False).all()
    ItemList=[];
    for datalist2 in ItemListsSerial : 
        ItemList.append({"product_id":datalist2.product_id,"qty":int(datalist2.qty),"serial_number":datalist2.serial_number,"price":datalist2.price,"total":datalist2.total})
        
    for datalist in ItemLists : 
        itemFirst = bastItem.objects.filter(bast_id = outletProudctx,product_id = datalist.product_id,serial_number__isnull=True).all().count()
        ItemList.append({"product_id":datalist.product_id,"qty":itemFirst,"serial_number":"","price":datalist.price,"total":datalist.price * itemFirst})
    context = {
        "transaction" : transaction,
        "salesItems" : ItemList
    }

    return render(request, 'helper/receiptBast.html',context)

def receipt_incoming_goods(request):
    id = request.GET.get('id')
    incomingGoodsx = incomingGoods.objects.filter(id = id).first()
    transaction = {}
    for field in incomingGoodsx._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(incomingGoodsx,field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    # ItemList = incomingGoodsItems.objects.filter(incomingGoods_id = incomingGoodsx).all()
    ItemLists = incomingGoodsItems.objects.filter(incomingGoods_id = incomingGoodsx,serial_number__isnull=True).all().distinct('product_id')
    ItemListsSerial = incomingGoodsItems.objects.filter(incomingGoods_id = incomingGoodsx,serial_number__isnull=False).all()
    ItemList=[];
    for datalist2 in ItemListsSerial : 
        ItemList.append({"product_id":datalist2.product_id,"qty":int(datalist2.qty),"serial_number":datalist2.serial_number,"price":datalist2.price,"total":datalist2.total,"group_id":datalist2.group_id})
        
    for datalist in ItemLists : 
        itemFirst = incomingGoodsItems.objects.filter(incomingGoods_id = incomingGoodsx,product_id = datalist.product_id,serial_number__isnull=True).all().count()
        ItemList.append({"product_id":datalist.product_id,"qty":itemFirst,"serial_number":"","price":datalist.price,"total":datalist.price * itemFirst,"group_id":datalist.group_id})
    context = {
        "transaction" : transaction,
        "salesItems" : ItemList,
        "namaOutlet":ItemList[0]['group_id']
    }

    return render(request, 'helper/receiptIncomingGoods.html',context)
    # return HttpResponse('')

# @login_required
def delete_sale(request):
    resp = {'status':'failed', 'msg':''}
    id = request.GET.get('id')
    try:
        delete = Sales.objects.filter(id = id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Sale Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')

def retur_sale(request):
    resp = {'status':'failed', 'msg':''}
    id = request.GET.get('id')
    print(id)
    try:
        delete = Sales.objects.filter(id = id).update(statusRetur="Retur")
        salesItem2s = salesItems.objects.filter(sale_id = id).all()
        for field in salesItem2s:
            # print(field.incomingGoodsItems_id.id)
            incomingGoodsItems.objects.filter(id = field.incomingGoodsItems_id.id).update(statusPayment = "Belum")
            #  incomingGoodsItemsdata = incomingGoodsItems.objects.filter(group_id = query_set,statusPayment = "Belum").all()
        # print(salesItem2s)
        resp['status'] = 'success'
        messages.success(request, 'Sale Record has been retur.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')

# Dashboard

def infoDataSales(request):
    opts = request.GET.get('id') 
    # print(opts)
    context = {
        "info_1" : 'Total Sales',
        "info_2" : 'Average',
        "func_name" : 'getDataInfoSales',
        'nameSeries' : 'Total Sales',
        'dataGroup':opts
    }
    return render(request, 'helper/info_sales.html', context)

def infoDataTransaksi(request):
    context = {
        "info_1" : 'Total Transaction',
        "info_2" : 'Average',
        "func_name" : 'getDataInfoTransaction',
        'nameSeries' : 'Total Transaction'
    }
    return render(request, 'helper/info_sales.html', context)

def infoDataProductSold(request):
    
    context = {
        "info_1" : 'Total Product Sold',
        "info_2" : 'Average',
        "func_name" : 'getDataInfoProductSold',
        'nameSeries' : 'Total Product Sold'
    }
    return render(request, 'helper/info_sales.html', context)
    

def getDataInfoSales(request):
    resp = {'status':'failed', 'msg':''}
    
    opts = request.GET.get('opts')        
    grup_id = request.GET.get('grup_id')        
        
    if opts == 'harian':
        
        try:
            query_set = Group.objects.filter(user = request.user).first()
            if request.user.is_superuser :
                data = getdataHarian('grand_total',query_set,'ya',grup_id)
            else :
                data = getdataHarian('grand_total',query_set,'tidak',grup_id)

            resp['status'] = 'success'
            resp['data_all'] = data['data_']
            resp['data_ave'] = data['avg_']
            resp['lbl'] = data['label']
            resp['total_all'] = 'Rp. {:,},-'.format(data['total']).replace(',','.')
            resp['avg_all'] = 'Rp. {:,},-'.format(data['aver']).replace(',','.')
            
            messages.success(request, 'Sale Record has been deleted.')
            
        except:
            resp['msg'] = "An error occured"
            print("Unexpected error:", sys.exc_info()[0])

    
    if opts == 'bulanan':
        try:
            data = getDataBulanan('grand_total')
                
            resp['status'] = 'success'
            resp['data_all'] = data['data_']
            resp['data_ave'] = data['avg_']
            resp['lbl'] = data['label']
            messages.success(request, 'Sale Record has been deleted.')
        except:
            resp['msg'] = "An error occured"
            print("Unexpected error:", sys.exc_info()[0])
                    
    return HttpResponse(json.dumps(resp), content_type='application/json')

def getDataInfoTransaction(request):
    resp = {'status':'failed', 'msg':''}
    
    opts = request.GET.get('opts')        
        
    if opts == 'harian':

        try:
            data = getdataHarian('transact')

            resp['status'] = 'success'
            resp['data_all'] = data['data_']
            resp['data_ave'] = data['avg_']
            resp['lbl'] = data['label']

            resp['total_all'] = '{:,}'.format(data['total']).replace(',','.')
            resp['avg_all'] = '{:,}'.format(data['aver']).replace(',','.')
            
            messages.success(request, 'Sale Record has been deleted.')
            
        except:
            resp['msg'] = "An error occured"
            print("Unexpected error:", sys.exc_info()[0])

    
    if opts == 'bulanan':
        try:
            data = getDataBulanan('transact')
                
            resp['status'] = 'success'
            resp['data_all'] = data['data_']
            resp['data_ave'] = data['avg_']
            resp['lbl'] = data['label']
            
            messages.success(request, 'Sale Record has been deleted.')
        except:
            resp['msg'] = "An error occured"
            print("Unexpected error:", sys.exc_info()[0])
                    
    return HttpResponse(json.dumps(resp), content_type='application/json')

def getDataInfoProductSold(request):
    resp = {'status':'failed', 'msg':''}
    
    opts = request.GET.get('opts')        
        
    if opts == 'harian':

        try:
            data = getdataHarian('qty')

            resp['status'] = 'success'
            resp['data_all'] = data['data_']
            resp['data_ave'] = data['avg_']
            resp['lbl'] = data['label']

            resp['total_all'] = '{:,}'.format(data['total']).replace(',','.')
            resp['avg_all'] = '{:,}'.format(data['aver']).replace(',','.')

            
            messages.success(request, 'Sale Record has been deleted.')
            
        except:
            resp['msg'] = "An error occured"
            print("Unexpected error:", sys.exc_info()[0])

    
    if opts == 'bulanan':
        try:
            data = getDataBulanan('qty')
                
            resp['status'] = 'success'
            resp['data_all'] = data['data_']
            resp['data_ave'] = data['avg_']
            resp['lbl'] = data['label']

            messages.success(request, 'Sale Record has been deleted.')
        except:
            resp['msg'] = "An error occured"
            print("Unexpected error:", sys.exc_info()[0])
                    
    return HttpResponse(json.dumps(resp), content_type='application/json')

import pandas as pd

def getDataCategory(request):
    resp = {'status':'failed', 'msg':''}
    
    id_cat = request.GET.get('id_cat')        
    if id_cat == 'all':
        try:
            all_category = Products.objects.all().values('id', 'code', 'name', 'stock', 'selling_price', 'price','image')
            query_set = Group.objects.filter(user = request.user).first()
            # if query_set == "adminGudang":
            #     incomingGoodsItemsdata = incomingGoodsItems.objects.filter(group_id__isnull=True,statusPayment = "Belum").all().count()
            # else : 
            data = []
            data2 = [] 
            
            for i in all_category:
                # print(i)
                data.append(i)
            for x in data:
                if query_set.id ==2:
                    # print('masuk');
                    incomingGoodsItemsdata = incomingGoodsItems.objects.filter(group_id=query_set,product_id = x['id'],statusPayment = "Belum").all().count()
                    if(incomingGoodsItemsdata != 0):
                        data2.append({'id':x['id'], 'code':x['code'], 'name':x['name'], 'stock':incomingGoodsItemsdata, 'selling_price':x['selling_price'], 'price':x['price'],'image':x['image']})
                else : 
                    # print(query_set.id ==2)
                    incomingGoodsItemsdata = incomingGoodsItems.objects.filter(group_id=query_set,product_id = x['id'],statusPayment = "Belum").all().count()
                    if(incomingGoodsItemsdata != 0):
                        data2.append({'id':x['id'], 'code':x['code'], 'name':x['name'], 'stock':incomingGoodsItemsdata, 'selling_price':x['price'], 'price':x['price'],'image':x['image']})
                # print(x['id'])
                # x['stock'] = data2
                
            resp['status']  = 'success'
            resp['data']    = data2        
            messages.success(request, 'Sale Record has been deleted.')
            
        except:
            resp['msg'] = "An error occured"
        
    else:
        try:
            all_category = Products.objects.filter(category_id = id_cat).values('id', 'code', 'name', 'stock', 'price')
            
            data = []
            
            for i in all_category:
                data.append(i)

            resp['status']  = 'success'
            resp['data']    = data        
            messages.success(request, 'Sale Record has been deleted.')
            
        except:
            resp['msg'] = "An error occured"
                    
    return HttpResponse(json.dumps(resp), content_type='application/json')

def getDataCategoryCashier(request):
    resp = {'status':'failed', 'msg':''}
    
    id_cat = request.GET.get('id_cat')        
    # print(request.user)
    if id_cat == 'all':
        try:
            all_category = Products.objects.all().values('id', 'code', 'name', 'stock', 'selling_price', 'price','image')
            query_set = Group.objects.filter(user = request.user).first()
            # incomingGoodsItemsdata = incomingGoodsItems.objects.filter(group_id = query_set,statusPayment = "Belum").all().count()
            # print(incomingGoodsItemsdata)
            data = []
            data2 = [] 
            for i in all_category:
                data.append(i);
            for x in data:
                incomingGoodsItemsdata = incomingGoodsItems.objects.filter(group_id = query_set,product_id = x['id'],statusPayment = "Belum").all().count()
                if(incomingGoodsItemsdata != 0):
                    data2.append({'id':x['id'], 'code':x['code'], 'name':x['name'], 'stock':incomingGoodsItemsdata, 'selling_price':x['selling_price'], 'price':x['price'],'image':x['image']})
                # x['stock'] = incomingGoodsItemsdata
                
            resp['status']  = 'success'
            resp['data']    = data2        
            messages.success(request, 'Sale Record has been deleted.')
            
        except:
            resp['msg'] = "An error occured"
        
    else:
        try:
            all_category = Products.objects.filter(category_id = id_cat).values('id', 'code', 'name', 'stock', 'price')
            
            data = []
            
            for i in all_category:
                data.append(i)
            
                
            resp['status']  = 'success'
            resp['data']    = data        
            messages.success(request, 'Sale Record has been deleted.')
            
        except:
            resp['msg'] = "An error occured"
                    
    return HttpResponse(json.dumps(resp), content_type='application/json')

def getRecomendationProduct(request):
    df_product = pd.read_csv('static/csv/produk.csv')
    df_pembelian = pd.read_csv('static/csv/pembelian.csv')
    
    resp = {'status':'failed', 'msg':''}
    
    name_prod = request.GET.get('name_prod')
    # print(name_prod)
    try:
        df = df_product.merge(df_pembelian, on='id_p')
        
        pvt_p = df.pivot_table(index = 'user', columns = 'id_p', values='coun').fillna(0)

        similarity = pvt_p.corr(method='pearson')
        
        recommender = pvt_p[name_prod]
        similar = pvt_p.corrwith(recommender)
        corr = pd.DataFrame(similar, columns=['Correlation'])
        corr.dropna(inplace=True)

        ratings = pd.DataFrame(df.groupby('id_p')['coun'].mean())
        ratings['num of ratings'] = pd.DataFrame(df.groupby('id_p')['coun'].count())
        corr = corr.join(ratings['num of ratings'])

        corr_result = corr['Correlation'].sort_values(ascending = False).head(9)
        # print(corr_result)

        data = corr_result.drop(corr_result.loc[corr_result.index==name_prod].index)
        # print(data)
        json_data = json.loads(data.to_json())
        # print(json_data)
        l_data = []
        for i in json_data:
            d = [i, math.floor(abs(json_data[i]*100))]
            l_data.append(d)
        
        print(l_data)    

        resp['status']  = 'success'
        resp['data']    = l_data        
        messages.success(request, 'Sale Record has been deleted.')
        
    except:
        resp['msg'] = "An error occured"
    
                    
    return HttpResponse(json.dumps(resp), content_type='application/json')


def totalStockData(request):
    resp = {'status':'failed', 'msg':''}
    data2 =  request.POST
    if data2['nameProduct'] ==  'false':
        if data2['idkategori'] == 'false':
            products = Products.objects.filter(status = 1).order_by('category_id','name')
            # products = Products.objects.filter(status = 1,name__contains = data2['nameProduct'].upper())
        else:
            products = Products.objects.filter(status = 1,category_id=data2['idkategori']).order_by('category_id','name')
            # products = Products.objects.filter(status = 1,name__contains = data2['nameProduct'].upper(),category_id=data2['idkategori'])
    else:
        if data2['idkategori'] == 'false':
            products = Products.objects.filter(status = 1,name__contains = data2['nameProduct'].upper()).order_by('category_id','name')
        else:
            products = Products.objects.filter(status = 1,name__contains = data2['nameProduct'].upper(),category_id=data2['idkategori']).order_by('category_id','name')
    kategori = Category.objects.filter(status = 1)
    all_users = Group.objects.all()
    product_json = []
    user_json = []
    query_set = Group.objects.filter(user = request.user).first()
    print(products)
    for product in products:
        # print(product.price)
        # product_json.append({'id':product.id, 'name':product.name, 'price':product.price, 'selling_price':product.selling_price,'stock':product.stock})
        # print(product.price)
        # if query_set.id == 2: 
        #     incomingGoodsItemsdata = incomingGoodsItems.objects.filter(product_id = product.id,statusPayment = "Belum").all().count()
        #     dataSerialNumberArr=[]
        #     incomingGoodsItemsdata2 = incomingGoodsItems.objects.filter(product_id = product.id,statusPayment = "Belum").all()
        #     for incomingGoodsItemsdatalop in incomingGoodsItemsdata2:
        #         if incomingGoodsItemsdatalop.serial_number is not None:
        #             dataSerialNumberArr.append({'serial_number':incomingGoodsItemsdatalop.serial_number})
        # else : 
        
        if data2['idtoko'] ==  'false':
            incomingGoodsItemsdata = incomingGoodsItems.objects.filter(product_id = product.id,statusPayment = data2['status']).all().count()
            incomingGoodsItemsdata2 = incomingGoodsItems.objects.filter(product_id = product.id,statusPayment = data2['status']).all()
            
        else :
            
            incomingGoodsItemsdata = incomingGoodsItems.objects.filter(product_id = product.id,statusPayment = data2['status'],group_id = data2['idtoko']).all().count()
            incomingGoodsItemsdata2 = incomingGoodsItems.objects.filter(product_id = product.id,statusPayment = data2['status'],group_id = data2['idtoko']).all()
            
        dataSerialNumberArr=[]
        for incomingGoodsItemsdatalop in incomingGoodsItemsdata2:
            if incomingGoodsItemsdatalop.serial_number is not None:
                # print(incomingGoodsItemsdatalop.group_id);
                if incomingGoodsItemsdatalop.group_id is None:
                    dataSerialNumberArr.append({'serial_number':incomingGoodsItemsdatalop.serial_number,'outlet':'Gudang','statusPayment':incomingGoodsItemsdatalop.statusPayment,'category_id':product.category_id.name,'modal':product.price,'idItem':incomingGoodsItemsdatalop.id})
                else :
                    dataSerialNumberArr.append({'serial_number':incomingGoodsItemsdatalop.serial_number,'outlet':incomingGoodsItemsdatalop.group_id.name,'statusPayment':incomingGoodsItemsdatalop.statusPayment,'category_id':product.category_id.name,'modal':product.price,'idItem':incomingGoodsItemsdatalop.id})
            else:
                if incomingGoodsItemsdatalop.group_id is None:
                    dataSerialNumberArr.append({'serial_number':incomingGoodsItemsdatalop.serial_number,'outlet':'Gudang','statusPayment':incomingGoodsItemsdatalop.statusPayment,'category_id':product.category_id.name,'modal':product.price,'idItem':incomingGoodsItemsdatalop.id})
                else :
                    dataSerialNumberArr.append({'serial_number':'-','outlet':incomingGoodsItemsdatalop.group_id.name,'statusPayment':incomingGoodsItemsdatalop.statusPayment,'category_id':product.category_id.name,'modal':product.price,'idItem':incomingGoodsItemsdatalop.id}) 
        if incomingGoodsItemsdata != 0:      
            product_json.append({'id':product.id,'category_id':product.category_id.name,'modal':product.price, 'name':product.name, 'price':product.price, 'selling_price':product.selling_price,'stock':incomingGoodsItemsdata,'dataSerialNumber':dataSerialNumberArr})
    # list_code = incomingGoodsItems.objects.all()
    # # if data2['search[value]'] == None:
    # # else :
    # #     list_code = incomingGoodsItems.objects.filter(product_id__name__icontains = data2['search[value]'] ).all()
    # data = []
    
    # for i in list_code:
    #     if i.group_id is None :
    #         data.append({
    #             'serial_number':i.serial_number,
    #             'product_name':i.product_id.name,
    #             'product_code':i.product_id.code,
    #             'outlet':'Gudang',
    #             'statusPayment':i.statusPayment
    #         })
    #     else:
    #         data.append({
    #             'serial_number':i.serial_number,
    #             'product_name':i.product_id.name,
    #             'product_code':i.product_id.code,
    #             'outlet':i.group_id.name,
    #             'statusPayment':i.statusPayment
    #         })
        

    # tmpJson = serializers.serialize("json",data)
    
    resp['status']  = "Success"
    resp['data']    = (product_json)
    return HttpResponse(json.dumps(resp), content_type='application/json')

def checkTableTransisi(request):
    resp = {'status':'failed', 'msg':''}

    list_code = tableTrans.objects.filter(user_id_trans = 0).values('code_trans')
    
    data = []
    
    for i in list_code:
        data.append(i)
    
    if list_code:
        resp['status']  = "Success"
        resp['data']    = data
    return HttpResponse(json.dumps(resp), content_type='application/json')

def inputTableTransisi(request):
    resp = {'status':'failed', 'msg':''}
    
    current_user = request.user.id
    # print(current_user)
    
    code_prod = request.GET.get('id')
    
    tableTrans(code_trans = code_prod, user_id_trans = 0).save()

    if tableTrans:
        
        resp['status']  = "Success"
    
    return HttpResponse(json.dumps(resp), content_type='application/json')

def resetTableTransisi(request):
    resp = {'status':'failed', 'msg':''}
    
    current_user = request.user.id
    # print(current_user)
    
    tableTrans.objects.filter(user_id_trans = 0).delete()
    
    if tableTrans:
        
        resp['status']  = "Success"
    
    return HttpResponse(json.dumps(resp), content_type='application/json')