# todoo

[![PyPI - Version](https://img.shields.io/pypi/v/todoo.svg)](https://pypi.org/project/todoo)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/todoo.svg)](https://pypi.org/project/todoo)

-----

Towards idiomatic Python with types for Odoo models.

/!\ This is pre-alpha stuff /!\

## Usage

Instead of this:

```python
from odoo import models, fields

class ResParter(models.Model):
    _inherit = "res.partner"

    friend = fields.Boolean()
    industry2_id = fields.Many2one('res.partner.industry', 'Additional Industry')
```

write this:

```python
from odoo import fields

from odoo.addons.base.models.res_partner import Partner

class ResParter(Partner, extends=True):
    friend: bool = fields.Boolean()
    industry2_id: ResPartnerIndustry = fields.Many2one()
```

## Why?

Idiomatic python.

Native auto completion in IDEs.

Static type checking.

## License

`todoo` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
