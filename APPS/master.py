from .models import masterApps


class Master:
    
    def getApps():
        content = {
            'logo': "assets/images/logo.svg",
            'namaAplikasi': "MyKasir",
            'js_inc': [
                "plugins/jquery/jquery.min.js",
                "plugins/jquery-ui/jquery-ui.min.js",
                "plugins/bootstrap/js/bootstrap.bundle.min.js",
                "plugins/overlayScrollbars/js/jquery.overlayScrollbars.min.js",
                "dist/js/adminlte.js",
                "plugins/moment/moment.min.js",
                "plugins/daterangepicker/daterangepicker.js",
                # "assets/select2/dist/js/select2.min.js",
                "dist/js/notif/sweet_alert.min.js",
                "dist/js/jquery.dataTables.min.js",
                "mycashier/js/global.js",
                "plugins/select2/js/select2.full.min.js",
                "plugins/datatables-bs4/js/dataTables.bootstrap4.min.js",
                "plugins/datatables-responsive/js/dataTables.responsive.min.js",
                "plugins/datatables-responsive/js/responsive.bootstrap4.min.js",
                "plugins/datatables-buttons/js/dataTables.buttons.min.js",
                "plugins/datatables-buttons/js/buttons.bootstrap4.min.js",
                "plugins/jszip/jszip.min.js",
                "plugins/pdfmake/pdfmake.min.js",
                "plugins/pdfmake/vfs_fonts.js",
                "plugins/datatables-buttons/js/buttons.html5.min.js",
                "plugins/datatables-buttons/js/buttons.print.min.js",
                # "plugins/datatables-buttons/js/dataTables.buttons.min.js",
                "plugins/datatables-buttons/js/buttons.colVis.min.js",
                # "mycashier/js/action_cashier.js",
            ],
            'css_inc': [
                "plugins/fontawesome-free/css/all.min.css",
                # "plugins/select2-bootstrap4-theme/select2-bootstrap4.min.css",
                "plugins/datatables-bs4/css/dataTables.bootstrap4.min.css",
                "plugins/datatables-responsive/css/responsive.bootstrap4.min.css",
                "plugins/datatables-buttons/css/buttons.bootstrap4.min.css",
                "dist/css/adminlte.min.css",
                "plugins/overlayScrollbars/css/OverlayScrollbars.min.css",
                # "dist/css/jquery.dataTables.min.css",
                "plugins/select2/css/select2.min.css",
                
            ]
            }
    
        return content