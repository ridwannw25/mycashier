$('.select2').select2({
    placeholder: 'Search product'
})
$('.select3').select2({
    placeholder: 'Search Karyawan'
})

$('#statusHide').hide()
var prod_save = [];
var subtotal = 0;
var grandtotal = 0;
var diskon = 0;
var product_json = JSON.parse(document.getElementById('product_json').textContent);
console.log(product_json)
$('#getPPN').on('change',function () {
    console.log($('#getPPN').val())
    if ($('#getPPN').val() == 'Ya') {
        $('#statusHide').show()
        
    } else {
        $('#statusHide').hide()
    }
    calc()
})
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
//                 `+"Rp."+parseFloat(prod_arr[id].selling_price).toLocaleString('en-US')+`
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
//                 `+"Rp."+parseFloat(prod_arr[id].selling_price).toLocaleString('en-US')+`
//             </p>
//         </div>
//         <div style="border-bottom: 1px solid #B0B0B0; width: 100%;"></div>
//     `);
//     var getIndex =  prod_save.findIndex(item => item.id == id)
//         prod_save[getIndex].qty = 1;
//         prod_save[getIndex].total = prod_arr[id].selling_price;
//     }else{
//         var getIndex =  prod_save.findIndex(item => item.id == id)
//         prod_save[getIndex].qty += 1;
//         prod_save[getIndex].total = prod_save[getIndex].selling_price * prod_save[getIndex].qty;
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
    var getIndex = prod_save.findIndex(item => item.id == idProd)
    console.log(idProd);
    var parent = $(e.target).closest('div');

    var currentVal = parseInt(parent.find('input[name="' + fieldName + '"]').val(), 10);
    prod_save[getIndex].qty = currentVal + 1;
    if (prod_save[getIndex].qty > prod_arr[idProd].stock) {
        alert('Stock Anda Abis');
        prod_save[getIndex].qty = prod_save[getIndex].qty - 1;
    }else{
        prod_save[getIndex].total = prod_save[getIndex].selling_price * prod_save[getIndex].qty;
        console.log(prod_save);
        $('#total' + idProd).html("Rp." + parseFloat(prod_save[getIndex].total).toLocaleString('en-US'));
        if (!isNaN(currentVal)) {
            parent.find('input[name="' + fieldName + '"]').val(currentVal + 1);
        } else {
            parent.find('input[name="' + fieldName + '"]').val(0);
        }
        
    }
}

function decrementValue(e) {
    e.preventDefault();
    var fieldName = $(e.target).data('field');
    var idProd = $(e.target).data('idprod');
    var parent = $(e.target).closest('div');
    var currentVal = parseInt(parent.find('input[name="' + fieldName + '"]').val(), 10);
    var getIndex = prod_save.findIndex(item => item.id == idProd)
    prod_save[getIndex].qty = currentVal - 1;
    prod_save[getIndex].total = prod_save[getIndex].selling_price * prod_save[getIndex].qty;
    console.log(prod_save);
    $('#total' + idProd).html("Rp." + parseFloat(prod_save[getIndex].total).toLocaleString('en-US'));
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

$('body').on('click', '.button-minus', function (e) {
    decrementValue(e);
    calc();
});
$('body').on('keyup', '.inputPrice', function (e) {
    var idProd = $(e.target).data('idprod');
    var getIndex = prod_save.findIndex(item => item.id == idProd)
    console.log($(e.target).val().replace(/\D/g,''));
    prod_save[getIndex].selling_price = $(e.target).val().replace(/\D/g,'');
    if (prod_save[getIndex].statusPrice != true) {
        if(prod_save[getIndex].selling_price < prod_save[getIndex].price){
            alert('harga jual di bawah harga beli');
            prod_save[getIndex].statusPrice = true;
            // alert(prod_save[getIndex].statusPrice);
        }
    }
    prod_save[getIndex].total = prod_save[getIndex].selling_price * prod_save[getIndex].qty;
    var kepo = parseFloat(prod_save[getIndex].selling_price).toLocaleString('en-US');
    $('#total' + idProd).html("Rp." + parseFloat(prod_save[getIndex].total).toLocaleString('en-US'));
    // decrementValue(e);
    $(e.target).val(kepo);
    // $(e.target).val("Rp." + parseFloat(prod_save[getIndex].selling_price).toLocaleString('en-US'));
    // alert(prod_save[getIndex].selling_price);
    
    calc();
});
function hapus(id) {
    var getIndex = prod_save.findIndex(item => item.id == id)
    if (getIndex != -1) {
        prod_save.splice(getIndex, 1);
        $('.parentTable' + id).remove();
    }
    calc();
}

function calc() {
    subtotal = 0;
    grandtotal = 0;
    for (let i = 0; i < prod_save.length; i++) {
        subtotal += prod_save[i].total;
        if ($('#getPPN').val() == 'Ya') {
            getGrandTotal = (subtotal - diskon) * 0.11;
            grandtotal = subtotal + getGrandTotal
        } else {
            grandtotal = subtotal - diskon;
        }
    }
    
    $('#subtotal').html("Rp." + parseFloat(subtotal).toLocaleString('en-US'));
    $('#grandTotal').html("Rp." + parseFloat(grandtotal).toLocaleString('en-US'));
}

$('#discountInput').keyup(function () {
    var data = $(this).val();
    diskon = data;
    calc();
})

function postData(tendered_amountV2, change) {
    var formData = new FormData();
    var el = $('<div>')
    formData.append('subtotal', subtotal);
    formData.append('grandtotal', grandtotal);
    formData.append('diskon', diskon);
    formData.append('diskon', diskon);
    formData.append('tendered_amount', tendered_amountV2);
    formData.append('amount_change', change);
    formData.append('nameCustomer', $('#name').val());
    formData.append('phoneCustomer', $('#phone').val());
    formData.append('statusPPN', $('#getPPN').val());
    formData.append('typePayment', $('#getTypePayment').val());
    formData.append('npwp', $('#npwp').val());
    formData.append('date', $('#date12').val());
    formData.append('id_user', $("#getuser").val());
    formData.append('data', JSON.stringify(prod_save));
    start_loader();
    $.ajax({
        headers: {
            "X-CSRFToken": '{{csrf_token}}'
        },
        url: "save_cashier",
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
        beforeSend: function() {
            // setting a timeout
            Swal.fire({
                title: 'Please Wait !',
                html: 'Loading...',// add html attribute if you want or remove
                allowOutsideClick: false,
                showCancelButton: false, // There won't be any cancel button
                showConfirmButton: false
               
            });
        },
        success: function (resp) {
            swal.close()
            if (typeof resp == 'object' && resp.status == 'success') {
                uni_modal("Receipt", "receipt?id=" + resp.sale_id)
                $('#uni_modal').on('hide.bs.modal', function () {
                    location.reload()
                    
                })
            } else if (resp.status == 'failed' && !!resp.msg) {
                el.text(resp.msg)
            } else {
                el.text("An error occured", 'error');
                end_loader();
                console.log(resp)
            }
            _this.prepend(el)
            el.show('slow')
            $("html, body, .modal").scrollTop(0);
            end_loader()
        }
    })
}
$('#check_out').click(function () {
    if($('#name').val() =='' || $('#phone').val() ==''|| $('#getPPN').val() == '' || $("#getuser").val() == '' || $("#date12").val() == ''){
        alert('Data Masih Kosong, Silahkan Cek Kembali');
        return '';
    }
    Swal.fire({
        title: 'Apakah anda sudah yakin?',
        text: "",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes'
      }).then((result) => {
        if (result.isConfirmed) {
            uni_modal("Checkout", "checkout_modal?grand_total=" + grandtotal)
        }
      })
})

function getByCategory(id_cat, name_cat) {
    $.ajax({
        url: "getDataCategoryCashier",
        data: {
            "id_cat": id_cat
        },
        dataType: 'json',
        error: err => {
            console.log(err)
            end_loader();
        },
        success: function (resp) {
            console.log(resp)
            var tabHtml1 = `
                            <span>Category : ` + name_cat + `</span>
                            <br>
                            <div class="table-responsive">
                            <table id="tableProductCashier" class="table table-striped table-bordered">
                                <colgroup>
                                    <col width="20%">
                                    <col width="40%">
                                    <col width="20%">
                                    <col width="20%">
                                </colgroup>
                                <thead>
                                    <tr>
                                        <th class="text-center py-1">kode produk</th>
                                        <th class="text-center py-1">nama produk</th>
                                        <th class="text-center py-1">stock</th>
                                        <th class="text-center py-1">harga</th>
                                    </tr>
                                </thead>
                                <tbody>
                            `
            var tabHtml2 = ``
            for (i in resp['data']) {
                dataArray = ['https://resource.logitech.com/w_800,c_lpad,ar_16:9,q_auto,f_auto,dpr_1.0/d_transparent.gif/content/dam/products/logitech/mice/m221-wireless-mouse/logitech-m220-silent33.png?v=1','https://lzd-img-global.slatic.net/g/p/d688f05199a9d4daf36d06240aa92459.jpg_2200x2200q80.jpg_.webp','https://i01.appmifile.com/webfile/globalimg/products/pc/mi-23-8-desktop-monitor-1c/overview-1.jpg','https://cf.shopee.co.id/file/90c8bf2192cdf9b8a384544afb1bc9d6','https://i0.wp.com/1.bp.blogspot.com/-O4sifmEYYgM/WEF1TwObq3I/AAAAAAAAAJ4/OTGzk7Pfqbk8WxVKBCOLZt13pir1LgkpgCLcB/s1600/Daftar-Harga-Laptop-Acer-Terbaru.jpg?ssl=1','https://resource.logitech.com/content/dam/logitech/en/products/keyboards/pop-keys-wireless-mechanical/gallery/pop-keys-gallery-blast-1.png'];
                // tabHtml2 += `<tr onclick="checkOutProductId(` + resp['data'][i]['id'] + `, '` + resp['data'][i]['name'] + `')">
                //                 <td class="px-2 py-1 text-start">` + resp['data'][i]['code'] + `</td>
                //                 <td class="px-2 py-1 text-center">` + resp['data'][i]['name'] + `</td>
                //                 <td class="px-2 py-1 text-start">` + resp['data'][i]['stock'] + `</td>
                //                 <td class="px-2 py-1 text-start">` + resp['data'][i]['price'] + `</td>
                //             </tr>`
                if (resp['data'][i]['image']==null) {
                    dataImage=`<img
                    src='http://127.0.0.1:8000/media/images/images.png' />`;
                    
                }else{
                    dataImage=` <img
                    src='http://127.0.0.1:8000/media/`+resp['data'][i]['image']+`' />`
                }
                if (resp['data'][i]['selling_price'] == null) {
                    dataPrice =0;
                } else {
                    dataPrice = parseFloat(resp['data'][i]['selling_price']).toLocaleString('en-US')
                }
                tabHtml2 += `<div class="col-md-3">
                <div class="product-card">
                    <a href="#" onclick="checkOutProductId(` + resp['data'][i]['id'] + `)" class="product-link">
                    
                    `+dataImage+`
                        <span class="overlay"></span>
                        
                        <span class="info">
                        <span class="title">` + resp['data'][i]['name'] + `</span>
                        <span class="price">` + "Rp." + dataPrice + `</span>
                        <div style="display:flex;justify-content: space-between;margin-top:14px">
                        <span class="title" style="color:#8d8d8d !important;"> Kode   ` + resp['data'][i]['code'] + `</span>
                        <span class="title" style="align-self: center;font-size: 4px;color: #e7dede;"> <i class="nav-icon fas fa-circle mt-1"></i></span>
                        <span class="title" style="color:#8d8d8d"> <i class="nav-icon fas fa-archive mt-1" style="color:#fba701;"></i> ` + resp['data'][i]['stock'] + `</span>
                        </div>
                            
                        </span>
                    </a>
    
                </div>
            </div>`
            }

            var tabHtml3 = `
                                </tbody>
                                </table>
                            </div>`

            var tabHtml = tabHtml2;
            $("#isiProduct").html(tabHtml)

            // $('#tableProductCashier').DataTable();

        }
    })
}

function checkOutProductId(id_p, nam) {
    var id = parseInt(id_p);

    $.ajax({
        url: "getRecomendationProduct",
        data: {
            "id_prod": id,
            "name_prod": nam
        },
        dataType: 'json',
        error: err => {
            console.log(err)
            end_loader();
        },
        success: function (resp) {
            console.log(resp)
            var isi_ = ``

            for (i in resp['data']) {
                isi_ += `<div class="col-md-3">
                            <div class="row" style="border-radius: 10px;background-color: chartreuse;margin:5px;padding:5px;">
                                <div class="col-md-8">
                                ` + resp['data'][i][0] + `
                                </div>
                                <div class="col-md-4">
                                ` + resp['data'][i][1] + ` %
                                </div>
                            </div>
                        </div>`
            }

            $("#isiRecomendation").html(isi_)

        }
    })


    var getIndex = prod_save.findIndex(item => item.id == id)
    if (prod_arr[id].stock != 0) {
        if (getIndex == -1) {
            prod_save.push(prod_arr[id]);
            dataOption = '';
            
            if(prod_arr[id].dataSerialNumber.length == 0){
                dataInputCount = ` <div class="input-group" >
                    <input type="button" id="button-minus" value="-" class="button-minus" data-field="quantity[]" data-idProd = "` + prod_arr[id].id + `">
                    <input type="number" id="qty` + prod_arr[id].id + `" step="1" max="" value="1" name="quantity[]" class="quantity-field">
                    <input type="button" value="+" class="button-plus" data-field="quantity[]" data-idProd = "` + prod_arr[id].id + `">
                </div>`;
                
            }else{
                dataInputCount='';
                dataOption += `<select id="select4`+id+`" name="saveSn[`+id+`][]" style="width: 100%;height: 40px;" multiple required>`;
                for (let i = 0; i < prod_arr[id].dataSerialNumber.length; i++) {
                    if (i == 0) {
                        dataOption += `<option value="`+prod_arr[id].dataSerialNumber[i].serial_number+`" selected>`+prod_arr[id].dataSerialNumber[i].serial_number+`</option>`;
                    }else{
                        dataOption += `<option value="`+prod_arr[id].dataSerialNumber[i].serial_number+`">`+prod_arr[id].dataSerialNumber[i].serial_number+`</option>`;

                    }
                }
                dataOption += ` </select>`;
            }
            $('#listView').append(
    
            `<div class="col-md-1 col-sm-6 col-12 parentTable` + id + `" style="margin-top: 10px;" id="parentTable` + id + `">
                <button type="button" onClick="hapus(` + id + `)" class="btn btn-outline-danger btn-block"><i class="fa fa-times"></i></button>
            </div>
            <div class="col-md-4 col-sm-6 col-12 parentTable` + id + `" style="margin-top: 10px;">
                <p style="margin-bottom: 0px;">
                    ` + prod_arr[id].name + `
                </p>
                <p>
                    <input type="input" value="`+parseFloat(prod_arr[id].selling_price).toLocaleString('en-US')+`" class="inputPrice"  data-idProd = "` + prod_arr[id].id + `">
                </p>
                
            </div>
            <div class="col-md-4 col-sm-6 col-12 parentTable` + id + `" style="margin-top: 10px;">
            `+dataInputCount+`
            
            `+dataOption+`
            
            </div>
            <div class="col-md-3 col-sm-6 col-12 parentTable` + id + `" style="margin-top: 10px;text-align: right;">
            <p id="total` + prod_arr[id].id + `">
            ` + "Rp." + parseFloat(prod_arr[id].selling_price).toLocaleString('en-US') + `
            </p>
            </div>
            <div style="border-bottom: 1px solid #B0B0B0; width: 100%;" class="parentTable` + id + `"></div>
            `);
            // prod_save[getIndex].dataSerialNumberzzzzxxx =$('#select4'+id).val()
            var getIndex = prod_save.findIndex(item => item.id == id)
            prod_save[getIndex].qty = 1;
            prod_save[getIndex].total = prod_arr[id].selling_price;
        } else {
            if (prod_save[getIndex].qty >= prod_arr[id].stock) {
                alert('Stock Anda Abis');
                prod_save[getIndex].qty = prod_arr[id].stock;
            }else{
                var getIndex = prod_save.findIndex(item => item.id == id)
                prod_save[getIndex].qty += 1;
                prod_save[getIndex].total = prod_save[getIndex].selling_price * prod_save[getIndex].qty;
                console.log(prod_save);
                $('#total' + id).html("Rp." + parseFloat(prod_save[getIndex].total).toLocaleString('en-US'));
                $('#qty' + id).val(prod_save[getIndex].qty);
            }
        }
    } else {
        alert('Stock Anda Abis');
    }
    $('#select4'+id).select2({
        placeholder: 'Pilih Serial Number'
    })
    $('#select4'+id).change(function(){
        var arr = $(this).val()
        prod_save[getIndex].qty = arr.length;
        prod_save[getIndex].total = prod_save[getIndex].selling_price * prod_save[getIndex].qty;
        $('#total' + id).html("Rp." + parseFloat(prod_save[getIndex].total).toLocaleString('en-US'));
        console.log(arr.length);
        prod_save[getIndex].dataSerialNumberzzzzxxx =arr
        calc();
    });
    if (prod_arr[id].dataSerialNumber.length == 0) {
        prod_save[getIndex].dataSerialNumberzzzzxxx = 0
    } else {
        prod_save[getIndex].dataSerialNumberzzzzxxx =$('#select4'+id).val()
        
    }
    calc();
}


$('#product-id').on('change', function () {
    var id = $('#product-id').val().split(",")[0];
    var nama = $('#product-id').val().split(",")[1];

    checkOutProductId(id, nama)
})

$(document).ready(function (e) {
    $('#allCategory').click();
});

function deleteRow(idClass, name, id){
    
    if (confirm("Are you sure to remove " + name + " product form list?") == true) {
        $("."+idClass).remove();
        for (let i = 0; i < prod_save.length; i++) {
            console.log(prod_save[i])
            if (prod_save[i]['id'] == id){
                prod_save.splice(i, 1)
            }
        }
        calc()
    }
}

// $("#parentTable"+id).on('click', function(){
//     viewlist.remove()

//     calc()
// })


$.fn.dataList = function (options) {
    this.each(function () {
        var $table = $(this);
        if ($table.is('ul')) {
            var $ul = $table;
            $table = $ul.wrap('<table><tbody/></table').closest('table');
            $ul.find('li').wrap('<tr><td/></tr>').contents().unwrap();
            $ul.contents().unwrap()
            $table.prepend('<thead><tr><th>Heading</th></tr></thead>');
        }
        $table.dataTable(options);
    });
}

$(document).ready(function () {
    $('.example').dataList({
        "sPaginationType": "full_numbers"
    });
    $('.select4').select2({
        placeholder: 'Search Karyawan'
    })
});