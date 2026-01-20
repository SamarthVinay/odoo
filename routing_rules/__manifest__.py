{
    'name': 'Routing Rules Engine',
    'version': '1.0',
    'summary': 'Manage Routing Logic and Conditions',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/demo_data.xml',
        'data/address_data.xml',
        'views/routing_condition_views.xml',
        'views/routing_test_wizard_views.xml',  
        'views/routing_account_views.xml',      
        'views/routing_rule_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
}