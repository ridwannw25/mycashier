jQuery.fn.dataTable.Api.register( 'sum()', function ( ) {
    return this.flatten().reduce( function ( a, b ) {
        if ( typeof a === 'string' ) {
            a = a.replace(/[^\d.-]/g, '') * 1;
        }
        if ( typeof b === 'string' ) {
            b = b.replace(/[^\d.-]/g, '') * 1;
        }
 
        return a + b;
    }, 0 );
} );

$("#infoTodaySold").on('click', function(){
    dashboard_modal('Product Sold', 'infoDataProductSold')
})

$("#infoTodayTransac").on('click', function(){
    dashboard_modal('Transaction', 'infoDataTransaksi')
})

$("#infoTodaySales").on('click', function(){
    dashboard_modal('Data Sales', 'infoDataSales')
})
$(".filterGroup").on('click', function(){
    data=$(this).data('id');
    // alert(data);
    dashboard_modal('Data Sales', 'infoDataSales?id='+data)
})

$("#infoTodaySales").on('click', function(){
    dashboard_modal('Data Sales', 'infoDataSales')
})

$("#closeDashModal").on('click', function(){
    $("#dashboard_modal").modal('toggle')
})