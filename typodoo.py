# SPDX-FileCopyrightText: 2022-present Stéphane Bidoul <stephane.bidoul@acsone.eu>
#
# SPDX-License-Identifier: MIT

import wrapt


@wrapt.when_imported("odoo.models")
def hook(model):
    print("Giving Odoo MetaModel additional super powers.")

    _orig_new = model.MetaModel.__new__

    def _typodoo_new(meta, name, bases, attrs):
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

        def _extends(bases):
            """ Check if at least one base is a sub class of BaseModel but not
            a direct child of BaseModel
            """
            for base in bases:
                if issubclass(
                    base, model.BaseModel
                ) and base not in [
                    model.TransientModel,
                    model.Model,
                    model.AbstractModel,
                ]:
                    return True
            return False

        # if '_original_module' is into attrs, the metaclass is called
        # from the method BaseModel._build_model when the class hierarchy
        # is build from the graph. We must only take care of the first call
        # to the metaclass when the original module is imported.
        if "_original_module" not in attrs:
            if _extends(bases):
                # TODO support delegation inheritance too ?
                # TODO Merge with existing _inherit field, or error if already set.
                attrs["_inherit"] = list(_inherit(bases))
                bases = tuple(_bases(bases))  # TODO Deduplicate.

        return _orig_new(meta, name, bases, attrs)

    model.MetaModel.__new__ = _typodoo_new

    _orig_init = model.MetaModel.__init__

    def _typodoo_init(self, name, bases, attrs):
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
