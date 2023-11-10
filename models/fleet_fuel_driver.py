from odoo import fields, models, api
import logging, datetime


_logger = logging.getLogger(__name__)
now = datetime.datetime.now()


class FleetFuelDriver(models.Model):
    _name = "fleet.fuel.driver"
    _description = "Tabella storico carte carburanti"
    
    
    driver_code = fields.Char()
    driver_pin = fields.Char()
    start_datetime = fields.Datetime()
    end_datetime = fields.Datetime()
    state = fields.Selection(string='Status', required=True, readonly=True, copy=False, selection=[('valid', 'Valida'),('unvalid', 'Non valida'),], default='valid')
    res_partner_id = fields.Many2one('res.partner')



class FleetFieldsUpdate(models.Model):
    _inherit = "res.partner"
    
    
    driver_code = fields.Char()
    driver_pin = fields.Char()


    def open_fleet_fuel_driver(self):
        return {
            'name': 'Fleet Fuel Drivers',
            'view_mode': 'tree,form',
            'res_model': 'fleet.fuel.driver',
            'type': 'ir.actions.act_window',
            'domain': [('res_partner_id', '=', self.id)],
            'context': {
                'default_res_partner_id': self.id,
            },
            'target': 'current',
        }

    
    @api.onchange('driver_code', 'driver_pin')
    def _update_fleet_fuel_driver(self):
        id_partner = self._origin.id
        driver = {}
        _logger.info('STAMPO SELF.ID ->  %s', id_partner)
        driver_record = self.env['fleet.fuel.driver'].search([('res_partner_id', '=', id_partner), ('end_datetime', '=', False)])
        driver['driver_code'] = driver_record.read(['driver_code'])
        driver['driver_pin'] = driver_record.read(['driver_pin'])
        driver['start_datetime'] = driver_record.read(['start_datetime'])
        driver['end_datetime'] = driver_record.read(['end_datetime'])
        driver['state'] = driver_record.read(['state'])
        driver['res_partner_id'] = driver_record.read(['res_partner_id'])

        if driver['driver_code']:
            _logger.info('STAMPO driver_code ->  %s', driver['driver_code'][0]['driver_code'])
        else:
            _logger.info('Nessun driver_code')
        if driver['driver_code']:
            _logger.info('STAMPO driver_pin ->  %s', driver['driver_pin'][0]['driver_pin'])
        else:
            _logger.info('Nessun driver_pin')

        def _crea_nuovo_record(self):
            self.env['fleet.fuel.driver'].create({
                    'driver_code': self.driver_code,
                    'driver_pin': self.driver_pin,
                    'res_partner_id': self._origin.id,
                    'start_datetime': datetime.datetime.now()
                })

        
        # Controllo se esiste un record vecchio
        if driver_record:
            # Controllo che il dato vecchio sia diverso da quello nuovo
            if driver['driver_pin'][0]['driver_pin'] != self.driver_code and driver['driver_pin'][0]['driver_pin'] != self.driver_pin:
                
                if self.driver_code != False and self.driver_pin != False:
                    # Aggiorno il dato vecchio
                    driver_record.write({
                        'end_datetime': datetime.datetime.now(),
                        'state': 'unvalid'
                    })
                    #creo il dato nuovo
                    _crea_nuovo_record(self)
        # Se non esiste e i campi non sono vuoti procedo con la creazione di uno nuovo
        elif self.driver_code != False and self.driver_pin != False:
                self.env['fleet.fuel.driver'].create({
                    'driver_code': self.driver_code,
                    'driver_pin': self.driver_pin,
                    'res_partner_id': self._origin.id,
                    'start_datetime': datetime.datetime.now()
                })

            
            