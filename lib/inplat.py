from .external_api.inplat_wrapper import InplatClient

class Inplat():

    '''
    Основные бизнес-процессы:
    1) привязка с оплатой 1 рубля, статус - reserved
    2) checkout
    3) hold
    4) pay
    '''

    def __init__(self):
        self.inplat_client = InplatClient()

    def link_card_by_cryptogramma(self, user_id, crypto):
        result = self.inplat_client.pay_and_link(client_id=user_id, cryptogramma=crypto)

        if result['code'] == 0:
            return {'error_code': 0, 'url': result['url']}

    def _hold(self):
        pass

    def _pay(self):
        pass

    def _checkout(self):
        pass

    def _get_links_by_client_id(self):
        pass
