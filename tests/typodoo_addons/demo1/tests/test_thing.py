from typing_extensions import reveal_type
from odoo.tests.common import TransactionCase

from odoo.addons.demo1.models.res_partner import ResPartner
from odoo.addons.demo1.models.thing import Thing


class TestThing(TransactionCase):
    def test_thing(self):
        thing = Thing(self.env).create({"name": "Test Thing", "weight": 42})
        assert thing.name == "Test Thing"
        assert thing.weight == 42

    def test_res_partner(self):
        partner = ResPartner(self.env).create({"name": "Test Partner"})
        # TODO this should reveal demo1.models.ResPartner
        reveal_type(partner)
        partner = ResPartner(self.env).search([("name", "=", "Test Partner")])
        reveal_type(partner)
        p2 = ResPartner(self.env).browse(partner.id)
        assert p2.name == "Test Partner"
        partner.thing_ids = [
            (0, 0, {"name": "Universe", "weight": 42}),
            (0, 0, {"name": "Towel", "weight": 1}),
        ]
        assert p2.thing_count == 2
        assert p2.thing_weight == 43
