$(function() {
    $('#create_new').click(function() {
        uni_modal("Add New Product", "manage_products")
    })
    $('.edit-data').click(function() {
        uni_modal("Edit Product", "manage_products?id=" + $(this).attr('data-id'))
    })
    $('.delete-data').click(function() {
        _conf("Are you sure to delete this Product?", "delete_product", [$(this).attr('data-id')])
    })

    $('#uni_modal').on('shown.bs.modal', function() {
        $('#category_id').select2({
            placeholder: "Please Select Category Here",
            width: '100%',
            dropdownParent: $('#uni_modal')
        }),
        $('#supplier_id').select2({
            placeholder: "Please Select supplier Here",
            width: '100%',
            dropdownParent: $('#uni_modal')
        })
    })
})

function delete_product($id) {
    // start_loader();
    $.ajax({
        url: "delete_product",
        method: "GET",
        data: {
            id: $id
        },
        dataType: "json",
        error: err => {
            console.log(err)
            alert_toast("An error occured.", 'error');
            // end_loader();
        },
        success: function(resp) {
            if (typeof resp == 'object' && resp.status == 'success') {
                location.reload();
            } else {
                alert_toast("An error occured.", 'error');
                // end_loader();
            }
        }
    })
}

$(document).ready( function () {
    $('#tableProduct').DataTable();
} );