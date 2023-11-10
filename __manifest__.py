{
    'name': 'Schede carburante',
    'version': '16',
    'author': "Luca Cocozza",
    'application': True,
    'description': "Gestione delle schede carburante.",
    'depends': ['carburante',],
    'data': [
        # # Settaggi per accesso ai contenuti
        'data/ir.model.access.csv',
        # # Caricamento delle view,
        'view/res_partner_view_update.xml',
        'view/fleet_fuel_driver_view.xml',
        # Menu
        'view/menu.xml',
    ],
}
