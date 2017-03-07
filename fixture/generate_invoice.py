import random

import pytest

from model.invoice import Invoice


summ = random.randint(10, 2000)
invoice = Invoice.create(summ=summ, user=1)
print(invoice.summ)

