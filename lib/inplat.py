from .external_api.inplat_wrapper import InplatClient
from model.payment import Payment
from model.payment import PaymentStatus


class Inplat():

    def __init__(self):
        self.inplat_client = InplatClient()


    async def link_card_by_cryptogramma(self, user_id, crypto):
        # пофиксить и передавать сюда юзера целиком, а не только айди
        payment = Payment.create(user_id=user_id, sum=100, case=0)

        result = await self.inplat_client.pay_and_link(client_id=user_id,
                                                       cryptogramma=crypto,
                                                       account=payment.get_id(),
                                                       summ=payment.sum)

        print(result)

        if result['code'] == 0:
            payment.inplat_id = result['id']
            payment.error_code = 0
            payment.status = int(PaymentStatus.WAIT_FOR_REDIRECT)
            payment.save()
            return {'error_code': 0, 'url': result['url']}

        else:
            payment.status = int(PaymentStatus.ERROR)
            payment.error_code = result['code']
            payment.save()
            return {'error_code': result['code'], 'message': result['message']}

    def _hold(self):
        pass

    async def pay_by_linked_card(self, User, summ):

        user_id = User.get_id()
        link_id = User.links[0]['link_id']

        payment = Payment.create(user_id=user_id, sum=summ, case=1)

        result = await self.inplat_client.pay_by_link(
            client_id=user_id,
            link_id=link_id,
            account=payment.get_id(),
            summ=payment.sum
        )

        print(result)

        if result['code'] == 0:
            payment.inplat_id = result['id']
            payment.error_code = 0
            payment.status = PaymentStatus.PAID
            payment.paid_at = result['pstamp']
            payment.save()
            return 0

        else:
            payment.status = PaymentStatus.ERROR
            payment.error_code = result['code']
            payment.save()
            return -1


    def _checkout(self):
        pass

    async def refresh_links_by_client_id(self, User):
        result = await self.inplat_client.links(User.id)
        if result['code'] == 0:
            links = result['links']
            print(links, User.links)
            diff = set(links) - set(User.links)
            User.links = User.links.extend(diff)
            User.save()
        elif result['code'] == 46:
            User.links = []
            User.save()
        else:
            raise Exception('wtf?!')

