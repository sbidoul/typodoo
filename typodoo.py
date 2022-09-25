# SPDX-FileCopyrightText: 2022-present Stéphane Bidoul <stephane.bidoul@acsone.eu>
#
# SPDX-License-Identifier: MIT

import wrapt


@wrapt.when_imported("odoo.models")
def hook(model):
    print("Giving Odoo MetaModel additional super powers.")

    from odoo import fields

    def _enhance_fields(class_name, attrs):
        annotations = attrs.get("__annotations__")
        if not annotations:
            return
        for name, field in attrs.items():
            if not isinstance(field, fields.Field):
                # Not an Odoo field.
                continue
            annotation = annotations.get(name)
            if annotation is None:
                # No type annotation on field, nothing to add.
                continue
            if isinstance(field, fields._Relational):
                assert issubclass(annotation, model.BaseModel), (
                    f"Relational field {name!r} of {class_name!r} must be "
                    f"type annotated with a model class, not {annotation!r}."
                )
                field_comodel_name = (
                    field.args.get("comodel_name") or field.comodel_name
                )
                if not field_comodel_name:
                    field.args["comodel_name"] = annotation._name
                else:
                    assert field_comodel_name == annotation._name, (
                        f"Relational field {name!r} of {class_name!r} "
                        f"has a comodel_name {field_comodel_name!r} that "
                        f"does not match its type annotation {annotation!r}."
                    )
            # TODO support more field types
            # TODO more type annotation vs field type checks
            # TODO derive Odoo specific field type from type annotation
            # TODO Optional / required (what to do with null = False in Odoo?)

    _orig_new = model.MetaModel.__new__

    def _typodoo_new(meta, name, bases, attrs, extends=False):
        def _bases(bases):
            for base in bases:
                if issubclass(base, model.TransientModel):
                    yield model.TransientModel
                elif issubclass(base, model.Model):
                    yield model.Model
                elif issubclass(base, model.AbstractModel):
                    yield model.AbstractModel
                else:
                    yield base

        def _inherit(bases):
            for base in bases:
                if issubclass(base, model.TransientModel):
                    assert base._name, f"TransientModel {base} has no _name"
                    yield base._name
                elif issubclass(base, model.Model):
                    assert base._name, f"Model {base} has no _name"
                    yield base._name
                elif issubclass(base, model.AbstractModel):
                    yield base._name or "base"

        # TODO support delegation inheritance too ?
        if extends is True:
            # TODO Merge with existing _inherit field, or error if already set.
            attrs["_inherit"] = list(_inherit(bases))
            bases = tuple(_bases(bases))  # TODO Deduplicate.

        _enhance_fields(name, attrs)

        return _orig_new(meta, name, bases, attrs)

    model.MetaModel.__new__ = _typodoo_new

    _orig_init = model.MetaModel.__init__

    def _typodoo_init(self, name, bases, attrs, extends=False):
        return _orig_init(self, name, bases, attrs)

    model.MetaModel.__init__ = _typodoo_init

    _orig_call = model.MetaModel.__call__

    def _typodoo_call(cls, env, *args):
        registry_cls = env.registry[cls._name]
        if cls is registry_cls:
            # cls is in registry, we likely come from api.Environment.__get_item__
            # and we want to call the regular constructor.
            return _orig_call(cls, env, *args)
        else:
            # We are instanciating a class that is not in the registry so
            # the user is likely calling ModelClass(env), so we do the same
            # as api.Environment.__get_item__.
            assert not args
            return registry_cls(env, (), ())
    
    model.MetaModel.__call__ = _typodoo_call
