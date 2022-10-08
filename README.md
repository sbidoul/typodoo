# typodoo

[![PyPI - Version](https://img.shields.io/pypi/v/typodoo.svg)](https://pypi.org/project/typodoo)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/typodoo.svg)](https://pypi.org/project/typodoo)

-----

Towards idiomatic Python with types for Odoo models.

This package supports the Odoo Experience 2022 talk ([sildes](https://docs.google.com/presentation/d/1A8UzGnw3TisUjajnPySiHk6E75tEpi7D3zxsHdtjIW4/edit?usp=sharing), [video](https://youtu.be/pAVGpEVORbY)).

It works best when [a few type
annotations](https://github.com/odoo/odoo/compare/16.0...acsone:odoo:16.0-type-annotations?expand=1)
are added to the Odoo core.

/!\ This is pre-alpha stuff /!\

## What?

`pip install typodoo` to monkey patch the Odoo metaclass on Odoo startup.

Then, you can still write this, as usual:

```python
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    friend = fields.Boolean()
    industry2_id = fields.Many2one(
        'res.partner.industry',
        string='Secondary Industry',
        required=True,
    )
```

But you can also write this:

```python
from odoo import fields

from odoo.addons.base.models.res_partner import (
    Partner, ResPartnerIndustry
)

class ResPartner(Partner):
    friend = fields.Boolean()
    industry2_id = fields.Many2one[ResPartnerIndustry](
        string='Secondary Industry',
    )
```

And also this:

```python
from odoo.addons.my_addon.models.res_partner import ResPartner


partners = ResPartner(self.env).search([])
```

## Why?

Idiomatic python.

Native auto completion in IDEs.

Static type checking.

## Development

`pip install -e .`

Then, copy `typodoo_activate.pth` to `$VIRTUAL_ENV/lib/python3.10/site-packages`.
Automating this setup is a TODO.

## License

`typodoo` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
