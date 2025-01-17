{
    'name': 'Room Booking',
    'sequence': -102,
    'depends': ['base', 'mail', 'account', 'product', 'sale'],
    'author': 'Plus Tech',
    'summary': """ Room Booking """,
    'description': """ Room Booking """,
    'website': "http://www.plustech.com",
    'version': '1.0.0',
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/room_squ.xml',
        'data/booking_squ.xml',
        'data/mail_template_data.xml',
        'views/menu.xml',
        'views/facility_room_view.xml',
        'views/room_view.xml',
        'views/booking_room_view.xml',
        'views/res_config_settings_view.xml',
        'views/booking_inhert_invoice.xml',
        'reports/peaper_format_report.xml',
        'reports/report.xml',
        'reports/booking_card.xml',
        'reports/sale_report_inherit.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3'

}
