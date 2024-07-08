$('.select2').select2()
var prod_save = [];
var subtotal = 0;
var grandtotal = 0;
var diskon = 0;
var product_json = JSON.parse(document.getElementById('product_json').textContent);

var prod_arr = {}
if (Object.keys(product_json).length > 0) {
    Object.keys(product_json).map(k => {
        prod_arr[product_json[k].id] = product_json[k]
    })
}
// $('#clickData').click(function() {
//     var id = $('#product-id').val();
//     console.log(prod_arr);

//     var getIndex =  prod_save.findIndex(item => item.id == id)
//     if (getIndex == -1) {
//         prod_save.push(prod_arr[id]);
//     $('#listView').append(
//         `<div class="col-md-1 col-sm-6 col-12" style="margin-top: 10px;" id="parentTable`+id+`">
//             <button type="button" class="btn btn-outline-danger btn-block"><i class="fa fa-times"></i></button>
//         </div>
//         <div class="col-md-4 col-sm-6 col-12" style="margin-top: 10px;">
//             <p style="margin-bottom: 0px;">
//                 `+prod_arr[id].name+`
//             </p>
//             <p>
//                 `+"Rp."+parseFloat(prod_arr[id].price).toLocaleString('en-US')+`
//             </p>
//         </div>
//         <div class="col-md-4 col-sm-6 col-12" style="margin-top: 10px;">
//             <div class="input-group" >
//                 <input type="button" id="button-minus" value="-" class="button-minus" data-field="quantity[]" data-idProd = "`+prod_arr[id].id+`">
//                 <input type="number" id="qty`+prod_arr[id].id+`" step="1" max="" value="1" name="quantity[]" class="quantity-field">
//                 <input type="button" value="+" class="button-plus" data-field="quantity[]" data-idProd = "`+prod_arr[id].id+`">
//             </div>                              
//         </div>
//         <div class="col-md-3 col-sm-6 col-12" style="margin-top: 10px;text-align: right;">
//             <p id="total`+prod_arr[id].id+`">
//                 `+"Rp."+parseFloat(prod_arr[id].price).toLocaleString('en-US')+`
//             </p>
//         </div>
//         <div style="border-bottom: 1px solid #B0B0B0; width: 100%;"></div>
//     `);
//     var getIndex =  prod_save.findIndex(item => item.id == id)
//         prod_save[getIndex].qty = 1;
//         prod_save[getIndex].total = prod_arr[id].price;
//     }else{
//         var getIndex =  prod_save.findIndex(item => item.id == id)
//         prod_save[getIndex].qty += 1;
//         prod_save[getIndex].total = prod_save[getIndex].price * prod_save[getIndex].qty;
//         console.log(prod_save);
//         $('#total'+id).html("Rp."+parseFloat(prod_save[getIndex].total).toLocaleString('en-US'));
//         $('#qty'+id).val(prod_save[getIndex].qty);
//     }
//     calc();
// })
function incrementValue(e) {
e.preventDefault();
var fieldName = $(e.target).data('field');
var idProd = $(e.target).data('idprod');
var getIndex =  prod_save.findIndex(item => item.id == idProd)
console.log(idProd);
var parent = $(e.target).closest('div');

var currentVal = parseInt(parent.find('input[name="' + fieldName + '"]').val(), 10);
prod_save[getIndex].qty = currentVal + 1;
prod_save[getIndex].total = prod_save[getIndex].price * prod_save[getIndex].qty;
console.log(prod_save);
$('#total'+idProd).html("Rp."+parseFloat(prod_save[getIndex].total).toLocaleString('en-US'));
if (!isNaN(currentVal)) {
parent.find('input[name="' + fieldName + '"]').val(currentVal + 1);
} else {
parent.find('input[name="' + fieldName + '"]').val(0);
}
}

function decrementValue(e) {
e.preventDefault();
var fieldName = $(e.target).data('field');
var idProd = $(e.target).data('idprod');
var parent = $(e.target).closest('div');
var currentVal = parseInt(parent.find('input[name="' + fieldName + '"]').val(), 10);
var getIndex =  prod_save.findIndex(item => item.id == idProd)
prod_save[getIndex].qty = currentVal - 1;
prod_save[getIndex].total = prod_save[getIndex].price * prod_save[getIndex].qty;
console.log(prod_save);
$('#total'+idProd).html("Rp."+parseFloat(prod_save[getIndex].total).toLocaleString('en-US'));
if (!isNaN(currentVal) && currentVal > 0) {
parent.find('input[name="' + fieldName + '"]').val(currentVal - 1);
} else {
parent.find('input[name="' + fieldName + '"]').val(0);
}
}

$('body').on('click', '.button-plus', function(e) {
incrementValue(e);
calc();
});

$('body').on('click', '.button-minus', function(e) {
decrementValue(e);
calc();
});
function calc() {
subtotal = 0;
grandtotal = 0;
for (let i = 0; i < prod_save.length; i++) {
    subtotal += prod_save[i].total;  
    grandtotal = subtotal - diskon;
}
$('#subtotal').html("Rp."+parseFloat(subtotal).toLocaleString('en-US'));
$('#grandTotal').html("Rp."+parseFloat(grandtotal).toLocaleString('en-US'));
}
$('#discountInput').keyup(function () {
    var data = $(this).val();
    diskon = data;
    calc();
})
function postData(tendered_amountV2 = 0,change = 0) {
    var formData = new FormData();
    var el = $('<div>')
    formData.append('subtotal', subtotal);
    formData.append('grandtotal', grandtotal);
    formData.append('diskon', diskon);
    formData.append('diskon', diskon);
    formData.append('tendered_amount', tendered_amountV2);
    formData.append('amount_change', change);
    formData.append('data', JSON.stringify(prod_save));
    start_loader();
    $.ajax({
        headers: {
            "X-CSRFToken": '{{csrf_token}}'
        },
        url: "save_incoming_goods",
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        method: 'POST',
        type: 'POST',
        dataType: 'json',
        error: err => {
            console.log(err)
            end_loader();
        },
        success: function(resp) {
            if (typeof resp == 'object' && resp.status == 'success') {
                // el.removeClass("alert alert-danger err-msg")
                    // location.reload()
                uni_modal("Receipt", "receipt_incoming_goods?id=" + resp.sale_id)
                $('#uni_modal').on('hide.bs.modal', function() {
                    location.reload()
                })
            } else if (resp.status == 'failed' && !!resp.msg) {
                el.text(resp.msg)
            } else {
                el.text("An error occured", 'error');
                end_loader();
                console.err(resp)
            }
            _this.prepend(el)
            el.show('slow')
            $("html, body, .modal").scrollTop(0);
            end_loader()
        }
    })
}
$('#check_out').click(function() {
    postData();
})

function getByCategory(id_cat, name_cat){
    $.ajax({
        url: "getDataCategory",
        data: {"id_cat":id_cat},
        dataType: 'json',
        error: err => {
            console.log(err)
            end_loader();
        },
        success: function(resp) {
            console.log(resp)
            var tabHtml1 = `
                            <span>Category : `+name_cat+`</span>
                            <br>
                            <div class="table-responsive">
                            <table id="tableProductCashier" class="table table-striped table-bordered">
                                <colgroup>
                                    <col width="40%">
                                    <col width="30%">
                                    <col width="30%">
                                </colgroup>
                                <thead>
                                    <tr>
                                        <th class="text-center py-1">nama produk</th>
                                        <th class="text-center py-1">stock</th>
                                        <th class="text-center py-1">harga</th>
                                    </tr>
                                </thead>
                                <tbody>
                            `
            var tabHtml2 = ``
            for (i in resp['data']){
                tabHtml2 += `<tr onclick="checkOutProductId(`+resp['data'][i]['id']+`, '`+resp['data'][i]['name']+`')">
                                <td class="px-2 py-1 text-center">`+resp['data'][i]['name']+`</td>
                                <td class="px-2 py-1 text-start">`+resp['data'][i]['stock']+`</td>
                                <td class="px-2 py-1 text-start">Rp. `+resp['data'][i]['price']+`</td>
                            </tr>`
            }

            var tabHtml3 = `
                                </tbody>
                                </table>
                            </div>`
                        
            var tabHtml = tabHtml1+tabHtml2+tabHtml3
            $("#isiProduct").html(tabHtml)

            $('#tableProductCashier').DataTable();

        }
    })
}

function checkOutProductId(id_p, nam){
    var id = parseInt(id_p);

    $.ajax({
        url: "getRecomendationProduct",
        data: {"id_prod":id, "name_prod":nam},
        dataType: 'json',
        error: err => {
            console.log(err)
            end_loader();
        },
        success: function(resp) {
            console.log(resp)
            var isi_ = ``

            for (i in resp['data']){
                isi_ += `<div class="col-md-3">
                            <div class="row" style="border-radius: 10px;background-color: chartreuse;margin:5px;padding:5px;">
                                <div class="col-md-8">
                                `+resp['data'][i][0]+`
                                </div>
                                <div class="col-md-4">
                                `+resp['data'][i][1]+` %
                                </div>
                            </div>
                        </div>`
            }

            $("#isiRecomendation").html(isi_)

        }
    })


    var getIndex =  prod_save.findIndex(item => item.id == id)
    if (getIndex == -1) {
        prod_save.push(prod_arr[id]);
    $('#listView').append(
        `<div class="col-md-1 col-sm-6 col-12" style="margin-top: 10px;" id="parentTable`+id+`">
            <button type="button" class="btn btn-outline-danger btn-block"><i class="fa fa-times"></i></button>
        </div>
        <div class="col-md-4 col-sm-6 col-12" style="margin-top: 10px;">
            <p style="margin-bottom: 0px;">
                `+prod_arr[id].name+`
            </p>
            <p>
                `+"Rp."+parseFloat(prod_arr[id].price).toLocaleString('en-US')+`
            </p>
        </div>
        <div class="col-md-4 col-sm-6 col-12" style="margin-top: 10px;">
            <div class="input-group" >
                <input type="button" id="button-minus" value="-" class="button-minus" data-field="quantity[]" data-idProd = "`+prod_arr[id].id+`">
                <input type="number" id="qty`+prod_arr[id].id+`" step="1" max="" value="1" name="quantity[]" class="quantity-field">
                <input type="button" value="+" class="button-plus" data-field="quantity[]" data-idProd = "`+prod_arr[id].id+`">
            </div>                              
        </div>
        <div class="col-md-3 col-sm-6 col-12" style="margin-top: 10px;text-align: right;">
            <p id="total`+prod_arr[id].id+`">
                `+"Rp."+parseFloat(prod_arr[id].price).toLocaleString('en-US')+`
            </p>
        </div>
        <div style="border-bottom: 1px solid #B0B0B0; width: 100%;"></div>
    `);
    var getIndex =  prod_save.findIndex(item => item.id == id)
        prod_save[getIndex].qty = 1;
        prod_save[getIndex].total = prod_arr[id].price;
    }else{
        var getIndex =  prod_save.findIndex(item => item.id == id)
        prod_save[getIndex].qty += 1;
        prod_save[getIndex].total = prod_save[getIndex].price * prod_save[getIndex].qty;
        console.log(prod_save);
        $('#total'+id).html("Rp."+parseFloat(prod_save[getIndex].total).toLocaleString('en-US'));
        $('#qty'+id).val(prod_save[getIndex].qty);
    }
    calc();

}


$('#product-id').on('change', function(){
    var id = $('#product-id').val().split(",")[0];
    var nama = $('#product-id').val().split(",")[1];
    
    checkOutProductId(id, nama)
})

$(document).ready(function (e) {
    $('#allCategory').click();
});