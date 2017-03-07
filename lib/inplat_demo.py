from lib.external_api.inplat_wrapper import InplatClient

inplat_client = InplatClient()

async def _init():
    account = generate_uuid()
    result = await inplat_client.init(
        params={
            'account': account,
            'sum': 123
        },
        pay_params={'cryptogramma':'0dUZK7Iy0I4S9xggWJXH9Y+QUGUn/6cARcnH4B8jZUhDD/A9dyKq9PlBKhyjDHVDWdWYtNSZuDNa4YTLFzt+5O7xzh5dyGP9eZitzws8/ag='})
    print (result)




