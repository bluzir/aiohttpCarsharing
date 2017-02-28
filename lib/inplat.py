from .external_api.inplat_wrapper import InplatClient
from model.payment import Payment

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

    async def link_card_by_cryptogramma(self, user_id, crypto):
        payment = Payment.create()

        result = await self.inplat_client.pay_and_link(client_id=user_id, cryptogramma=crypto, account=payment.get_id())

        if result['code'] == 0:
            return {'error_code': 0, 'url': result['url']}

        else:
            return {'error_code': result['code'], 'message': result['message']}

    def _hold(self):
        pass

    def _pay(self):
        pass

    def _checkout(self):
        pass

    async def get_links_by_client_id(self, user_id):
        result = await self.inplat_client.links(user_id)
        if result['code'] == 46:
            # не делаем ничего: привязок нет
            pass
        else:
            # бизнес логика
            pass

