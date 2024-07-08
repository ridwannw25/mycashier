$(function() {
    $('.view-data').click(function() {
        uni_modal("Transaction's invoice", "receipt_bast?id=" + $(this).attr('data-id'))
    })
    $('.create_invoiceBybast').click(function() {
        uni_modal("Membuat Invoice", "createInvoiceByBast?id=" + $(this).attr('data-id'))
    })
    $('.delete-data').click(function() {
        _conf("Are you sure to delete <b>" + $(this).attr('data-code') + "</b> Transaction record?", "delete_sale", [$(this).attr('data-id')])
    })
    $('.delete-retur').click(function() {
        _conf("Are you sure to retur <b>" + $(this).attr('data-code') + "</b> Transaction record?", "delete_retur", [$(this).attr('data-id')])
    })

})

function delete_sale($id) {
    start_loader();
    $.ajax({
        url: "delete_sale",
        method: "GET",
        data: {
            id: $id
        },
        dataType: "json",
        error: err => {
            console.log(err)
            alert("An error occured.", 'error');
            end_loader();
        },
        success: function(resp) {
            if (typeof resp == 'object' && resp.status == 'success') {
                location.reload();
            } else {
                alert("An error occured.", 'error');
                end_loader();
            }
        }
    })
}
function delete_retur($id) {
    start_loader();
    $.ajax({
        url: "delete_retur",
        method: "GET",
        data: {
            id: $id
        },
        dataType: "json",
        error: err => {
            console.log(err)
            alert("An error occured.", 'error');
            end_loader();
        },
        success: function(resp) {
            if (typeof resp == 'object' && resp.status == 'success') {
                location.reload();
            } else {
                alert("An error occured.", 'error');
                end_loader();
            }
        }
    })
}

$(document).ready( function () {
    $('#tableSales').DataTable();
});