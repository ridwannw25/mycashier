baseUrl="http://127.0.0.1:8000";
urlPrint = baseUrl+'/totalStock?dataPrint?false?false?false';
dataStatus = 'Belum';
dataProduct = 'false';
dataToko = 'false';
datakategori = 'false';
var group_id = document.getElementById('group_id').textContent;
$(function() {
    $('.edit-data').click(function() {
        uni_modal("Edit Product", "?id=" + $(this).attr('data-id'))
    })
    $('#create_new').click(function() {
        uni_modal("Add New Category", "manage_supplier")
    })
    $('.edit-data').click(function() {
        uni_modal("Edit Category", "manage_supplier?id=" + $(this).attr('data-id'))
    })
    $('.delete-data').click(function() {
        _conf("Are you sure to delete this Supplier?", "delete_supplier", [$(this).attr('data-id')])
    })
})
function editSn(id) {
    uni_modal("Edit Serial Number", "manage_change_sn?id=" +id)
}
function delete_supplier($id) {
    // start_loader();
    $.ajax({
        url: "delete_supplier",
        method: "GET",
        data: {
            id: $id
        },
        dataType: "json",
        error: err => {
            console.log(err)
            alert("An error occured.");
            // end_loader();
            $("#confirm_modal").modal("toggle");
        },
        success: function(resp) {
            if (typeof resp == 'object' && resp.status == 'success') {
                location.reload();
            } else {
                alert("An error occured.");
                // end_loader();
            }
            $("#confirm_modal").modal("toggle");
        }
    })
}
function getListData(status,namaProduct,idtoko,idkategori) {
    // start_loader();
    $.ajax({
        url: "totalStockData",
        method: "POST",
        data:{
            'status':status,
            'nameProduct':namaProduct,
            'idtoko':idtoko,
            'idkategori':idkategori,
        },
        dataType: "json",
        error: err => {
            console.log(err)
            alert("An error occured.");
            // end_loader();
            $("#confirm_modal").modal("toggle");
        },
        success: function(resp) {
            $('.removeData').remove()
            resp.data.forEach(value => {
                dataSN = '';
                if (value.dataSerialNumber.length == 0) {
                    dataSN=`<td class="px-2 py-1 text-center"></td>
                    <td class="px-2 py-1 text-center"></td>
                    <td class="px-2 py-1 text-center"></td>`;
                    // dataSN=``;
                } else {
                    dataSN=`<td class="px-2 py-1 text-center">`+value.dataSerialNumber[0].serial_number+`</td>
                    <td class="px-2 py-1 text-center">`+value.dataSerialNumber[0].outlet+`</td>
                    <td class="px-2 py-1 text-center">`+value.dataSerialNumber[0].statusPayment+`</td>`;
                    
                }
                if(group_id == 2){
                    dataEdit=`<td><button class="mdc-button mdc-button--raised p-1 icon-button filled-button--light mdc-ripple-upgraded edit-data" onclick=editSn("`+value.dataSerialNumber[0].idItem+`") type="button" data-id="`+value.dataSerialNumber[0].idItem+`" title="Edit">
                    <i class="material-icons mdc-button__icon">edit</i>
                </button></td>`;
                }else{
                    dataEdit=``;
                }
                $('.listData').append(`<tr class="removeData">
                <td class="px-2 py-1 text-center">`+value.category_id+`</td>
                <td class="px-2 py-1 text-center">`+value.name+`</td>
                <td class="px-2 py-1 text-center">`+value.stock+`</td>
                <td class="px-2 py-1 text-center">`+"Rp." + parseFloat(value.modal).toLocaleString('en-US')+`</td>
                
                `+dataSN+`
               `+dataEdit+`
                </tr >`);
                for (let i = 1; i < value.dataSerialNumber.length; i++) {
                    if(group_id == 2){
                        dataEdit=`<td><button class="mdc-button mdc-button--raised p-1 icon-button filled-button--light mdc-ripple-upgraded edit-data" onclick=editSn("`+value.dataSerialNumber[i].idItem+`") type="button" data-id="`+value.dataSerialNumber[i].idItem+`" title="Edit">
                        <i class="material-icons mdc-button__icon">edit</i>
                    </button></td>`;
                    }else{
                        dataEdit=``;
                    }
                    $('.listData').append(`<tr class="removeData">
                    <td class="px-2 py-1 text-center"> </td>
                    <td class="px-2 py-1 text-center"> </td>
                    <td class="px-2 py-1 text-center"></td>
                    <td class="px-2 py-1 text-center"></td>
                    <td class="px-2 py-1 text-center">`+value.dataSerialNumber[i].serial_number+`</td>
                    <td class="px-2 py-1 text-center">`+value.dataSerialNumber[i].outlet+`</td>
                    <td class="px-2 py-1 text-center">`+value.dataSerialNumber[i].statusPayment+`</td>
                    `+dataEdit+`
                    </tr >`);
                    
                }
            });
        }
    })
}

$(document).ready( function () {
    $('.selectCategory').select2({
        placeholder: 'Search Kategori'
    })
    $('.select3').select2({
        placeholder: 'Search Karyawan',
        containerCssClass : "show-hide"
    })
    $('.select212').select2({
        placeholder: 'Search product'
    })
    $('.select212c').select2({
        placeholder: 'Search Grup'
    })
    
    $('#statusData').on('change',function () {
        statusData = $('#statusData').val();
        dataStatus= statusData;
        if (statusData == 'Sudah') {
            urlPrint = baseUrl+'/totalStock?dataPrint?Sudah?'+dataProduct+'?'+dataToko+'?'+datakategori
            getListData(dataStatus,dataProduct,dataToko,datakategori)
        } else {
            urlPrint = baseUrl+'/totalStock?dataPrint?'+dataProduct+'?'+dataToko+'?'+datakategori
            getListData(dataStatus,dataProduct,dataToko,datakategori)
        }

    })
    $('#toko').on('change',function () {
        toko = $('#toko').val();
        dataToko= toko;
        if (statusData == 'Sudah') {
            urlPrint = baseUrl+'/totalStock?dataPrint?Sudah?'+dataProduct+'?'+dataToko+'?'+datakategori
            getListData(dataStatus,dataProduct,dataToko,datakategori)
        } else {
            urlPrint = baseUrl+'/totalStock?dataPrint?'+dataProduct+'?'+dataToko+'?'+datakategori
            getListData(dataStatus,dataProduct,dataToko,datakategori)
        }

    })
    $('#kategori').on('change',function () {
        kategori = $('#kategori').val();
        datakategori= kategori;
        if (statusData == 'Sudah') {
            urlPrint = baseUrl+'/totalStock?dataPrint?Sudah?'+dataProduct+'?'+dataToko+'?'+datakategori
            getListData(dataStatus,dataProduct,dataToko,datakategori)
        } else {
            urlPrint = baseUrl+'/totalStock?dataPrint?'+dataProduct+'?'+dataToko+'?'+datakategori
            getListData(dataStatus,dataProduct,dataToko,datakategori)
        }

    })
    $("#namaprod").keyup(function() {
        namaprod = $('#namaprod').val();
        dataProduct= namaprod;
        if (statusData == 'Sudah') {
            urlPrint = baseUrl+'/totalStock?dataPrint?Sudah?'+dataProduct+'?'+dataToko+'?'+datakategori
            getListData(dataStatus,dataProduct,dataToko,datakategori)
        } else {
            if (namaprod.length > 2) {
                if (namaprod == '') {
                    urlPrint = baseUrl+'/totalStock?dataPrint?'+dataProduct+'?'+dataToko+'?'+datakategori
                    getListData(dataStatus,dataProduct,dataToko,datakategori)
                } else {
                    urlPrint = baseUrl+'/totalStock?dataPrint?'+dataProduct+'?'+dataToko+'?'+datakategori
                    getListData(dataStatus,dataProduct,dataToko,datakategori)
                }                
            }

        }
      })
    // $('#namaprod').on('change',function () {
    //     namaprod = $('#namaprod').val();
    //     dataProduct= namaprod;
    //     if (statusData == 'Sudah') {
    //         urlPrint = 'http://127.0.0.1:8000/totalStock?dataPrint?Sudah?'+dataProduct+'?'+dataToko
    //         getListData(dataStatus,dataProduct,dataToko)
    //     } else {
    //         urlPrint = 'http://127.0.0.1:8000/totalStock?dataPrint?'+dataProduct+'?'+dataToko
    //         getListData(dataStatus,dataProduct,dataToko)
    //     }

    // })
    // $('.tableSupplier').DataTable({
        let url = window.location.href.split("?");
        // let params = (new URL(url)).searchParams;
        // alert(url[2]);
        
        if (url[1] == 'dataPrint' && url[2] == "Sudah") {
            $('#receipt_print').remove();
            $('.select3').remove();
            getListData('Sudah')
        }else{
            if (url[1] == 'dataPrint') {
                $('#receipt_print').remove();
                $('.deleteSelect').remove();
                $('select').hide();
                // alert('asdad');
                $(".show-hide").parent().parent().hide();
                // var elem = document.getElementById('statusData');
                // elem.style.display = 'none';
                // alert(url[2]);
                getListData('Belum',url[2],url[3],url[4])
            } else {
                getListData('Belum',dataProduct,dataToko,datakategori)
            }
        }
        
        // alert(url[1]);
        // params.get('dataPrint') // "n1"
       
        $('#receipt_print').click(function () {
           var nw= window.open(urlPrint, '_blank', "width=800,height=800,left=300, top = 200")
           nw.document.close()
           //    $('#receipt_print').hide()
           setTimeout(() => {
            //    nw.document.write()
               nw.print()
               setTimeout(() => {
                nw.close()
                end_loader()
            }, 6500)
           }, 7000); 
           
        })
    
} );