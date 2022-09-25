# typodoo

[![PyPI - Version](https://img.shields.io/pypi/v/typodoo.svg)](https://pypi.org/project/typodoo)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/typodoo.svg)](https://pypi.org/project/typodoo)

-----

Towards idiomatic Python with types for Odoo models.

/!\ This is pre-alpha stuff /!\

## Usage

`pip install typodoo`

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

class ResPartner(Partner, extends=True):
    friend: bool = fields.Boolean()
    industry2_id: ResPartnerIndustry = fields.Many2one(
        string='Secondary Industry',
        required=True,
    )
```

But also this:

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
Make this done automatically by the build backend is a TODO.

## License

`typodoo` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
