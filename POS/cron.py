from django.db import connection as conn

def cronDaily():
    # with conn.cursor() as getTotalSales:
    #     getTotalSales.execute("""SELECT sum(grand_total) FROM "public"."APPS_sales" WHERE date_added::date = NOW()::date""")
    #     total_sales = getTotalSales.fetchall()
        
    # with conn.cursor() as getTransaction:
    #     getTransaction.execute("""SELECT sum(ass.qty) FROM "public"."APPS_sales" aps JOIN "public"."APPS_salesitems" ass on aps.id = ass.sale_id_id WHERE aps.date_added::date = NOW()::date""")
    #     qty = getTransaction.fetchall()
    
    # with conn.cursor() as getCount:
    #     getCount.execute("""SELECT count(ass.id) FROM "public"."APPS_sales" aps JOIN "public"."APPS_salesitems" ass on aps.id = ass.sale_id_id WHERE aps.date_added::date = NOW()::date""")
    #     transact = getCount.fetchall()
        
    # if total_sales == [] or total_sales == None:
    #     total_sales = 0
    # else:
    #     total_sales = total_sales[0][0]
        
    # if qty == [] or qty == None:
    #     qty = 0
    # else:
    #     qty = qty[0][0]
        
    # if transact == [] or transact == None:
    #     transact = 0
    # else:
    #     transact = transact[0][0]
        
    # with conn.cursor() as updateDataMart:
    #     updateDataMart.execute(f"INSERT INTO mart_data_sales (date, total, qty, transact) VALUES (NOW(), {total_sales}, {qty}, {transact})")
    #     conn.commit()
    
    pass