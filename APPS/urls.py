import json
from .views import Views
from . import jsonapi
from django.urls import path

urlpatterns = [
    path('', Views.home),
    path('dashboard', Views.dashboard),
    path('categoryList', Views.categoryList),
    path('productList', Views.productList),
    path('cashier', Views.cashier),
    path('createCardStok', Views.createCardStok),
    path('createBast', Views.createBast),
    path('sales', Views.sales),
    path('outletProudct', Views.outletProudct),
    path('bast', Views.bast),
    path('detailPajak', Views.detailPajak),
    path('invoice', Views.invoice),
    path('supplierList', Views.supplierList),
    path('totalStock', Views.totalStock),
    path('incomingGoods', Views.incomingGoods),
    path('cash', Views.cash),

    
    
    
    # json api for CRUD Category
    path('manage_category', jsonapi.manage_category),
    path('createInvoiceByBast', jsonapi.createInvoiceByBast),
    path('save_category', jsonapi.save_category),
    path('delete_category', jsonapi.delete_category),
    
    # json api for CRUD Product
    path('manage_products', jsonapi.manage_products),
    path('manage_change_sn', jsonapi.manage_change_sn),
    path('save_product', jsonapi.save_product),
    path('delete_product', jsonapi.delete_product),
    
    # json api for CRUD Product
    path('manage_supplier', jsonapi.manage_supplier),
    path('save_supplier', jsonapi.save_supplier),
    path('delete_supplier', jsonapi.delete_supplier),
    
    # Cashier
    path('checkout_modal', jsonapi.checkout_modal),
    path('save_cashier', jsonapi.save_cashier),
    path('save_cardStok', jsonapi.save_cardStok),    
    path('save_bast', jsonapi.save_bast), 
    path('receipt', jsonapi.receipt),
    path('kwitansi', jsonapi.kwitansi),
    path('receipt_outletProduct', jsonapi.receipt_outletProduct),
    path('receipt_bast', jsonapi.receipt_bast),
    path('getDataCategory', jsonapi.getDataCategory),
    path('getDataCategoryCashier', jsonapi.getDataCategoryCashier),
    path('getRecomendationProduct', jsonapi.getRecomendationProduct),
    path('checkTableTransisi', jsonapi.checkTableTransisi),
    path('inputTableTransisi', jsonapi.inputTableTransisi),
    path('resetTableTransisi', jsonapi.resetTableTransisi),

    # add Stock
    path('save_incoming_goods', jsonapi.save_incoming_goods),
    path('receipt_incoming_goods', jsonapi.receipt_incoming_goods),
    path('totalStockData', jsonapi.totalStockData),
    path('updatesn', jsonapi.updatesn),
    
    # Sales
    path('delete_sale', jsonapi.delete_sale),
    path('delete_retur', jsonapi.retur_sale),
    
    
    # infodashboard
    path('infoDataSales', jsonapi.infoDataSales),
    path('infoDataTransaksi', jsonapi.infoDataTransaksi),
    path('infoDataProductSold', jsonapi.infoDataProductSold),
    
    # getDataForInfo
    path('getDataInfoSales', jsonapi.getDataInfoSales),
    path('getDataInfoTransaction', jsonapi.getDataInfoTransaction),
    path('getDataInfoProductSold', jsonapi.getDataInfoProductSold),

    # get User 
    # path('getAllUser', jsonapi.getAllUser),

    

]