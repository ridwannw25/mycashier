$(function() {
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

$(document).ready( function () {
    $('#tableSupplier').DataTable();
} );