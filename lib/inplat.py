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
        # пофиксить и передавать сюда юзера целиком, а не только айди
        payment = Payment.create(user_id=user_id, sum=100)

        result = await self.inplat_client.pay_and_link(client_id=user_id,
                                                       cryptogramma=crypto,
                                                       account=payment.get_id(),
                                                       sum=payment.sum)

        if result['code'] == 0:
            payment.inplat_id = result['id']
            payment.error_code = 0
            payment.status = payment.PAYMENT_STATUS['wait_for_redirect']
            payment.update()
            return {'error_code': 0, 'url': result['url']}

        else:
            payment.status = payment.PAYMENT_STATUS['error']
            payment.error_code = result['code']
            payment.update()
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

