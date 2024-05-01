# -*- coding: utf-8 -*-
{
    'name': "Legal Administration",
    'summary': """ Legal Administration""",
    'description': """ Legal Administration """,
    'author': "Plus Tech",
    'sequence': -100,
    'website': "http://www.plustech.com",
    'version': '1.0.0',
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/agencies_seq.xml',
        'views/menu.xml',
        'views/issues_legal_view.xml',
        'views/sessions_legal_view.xml',
        'views/appeal_legal_view.xml',
        'views/implementation_legal_view.xml',
        'views/agencies_legal_view.xml',
        'views/promissory_note_legal_view.xml',
        'views/investigation_legal_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3'
}
