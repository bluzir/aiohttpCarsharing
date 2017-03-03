from .external_api.inplat_wrapper import InplatClient
from model.payment import Payment
from model.card_link import CardLink

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
        payment = Payment.create(user_id=user_id, sum=100, case=0)

        result = await self.inplat_client.pay_and_link(client_id=user_id,
                                                       cryptogramma=crypto,
                                                       account=payment.get_id(),
                                                       summ=payment.sum)

        print (result)

        if result['code'] == 0:
            payment.inplat_id = result['id']
            payment.error_code = 0
            payment.status = payment.PAYMENT_STATUS['wait_for_redirect']
            payment.save()
            return {'error_code': 0, 'url': result['url']}

        else:
            payment.status = payment.PAYMENT_STATUS['error']
            payment.error_code = result['code']
            payment.save()
            return {'error_code': result['code'], 'message': result['message']}

    def _hold(self):
        pass

    def _pay(self):
        pass

    def _checkout(self):
        pass

    async def refresh_links_by_client_id(self, User):
        result = await self.inplat_client.links(User.id)
        if result['code'] == 0:
            links = result['links']
            diff = set(links) - set(User.links)
            User.links = User.links.extend(diff)
            User.save()
        elif result['code'] == 46:
            User.links = []
            User.save()
        else:
            raise Exception('wtf?!')

