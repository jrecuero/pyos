from ._loggar import log
from ._mo import MO, MoStatus


class Factory:
    def __init__(self, name="default"):
        self.name = name
        self._repo = {}

    def set_klass_flags(self, flags):
        """set_klass_flags sets default values for class flags if not present.
        """
        flags.setdefault("super", None)
        flags.setdefault("config", True)
        flags.setdefault("concrete", True)
        flags.setdefault("access", "all")
        flags.setdefault("owner", "system")
        flags.setdefault("deletable", True)
        flags.setdefault("editable", True)
        flags.setdefault("visible", True)
        flags.setdefault("label", "")
        return flags

    def set_prop_flags(self, flags):
        """set_prop_flags sets default values for property flags if not present.
        """
        flags.setdefault("config", True)
        flags.setdefault("deletable", True)
        flags.setdefault("editable", True)
        flags.setdefault("visible", True)
        flags.setdefault("type", "str:base")
        flags.setdefault("auto", False)
        flags.setdefault("default", None)
        flags.setdefault("validate", None)
        flags.setdefault("href", None)
        flags.setdefault("label", None)
        return flags

    def new_klass(self, desc):
        """new_klass creates and add to the internal repository a new class
        with the given configuration.
        """
        assert desc["mo"] and desc["flags"], "Incomplete descriptor"
        klass_name = desc["mo"]
        klass = self._repo.get(klass_name, None)
        if klass is None:
            super_name = desc["flags"].get("super", None)
            super_klass = MO if super_name is None else self.get_klass(super_name)
            if super_klass is None:
                log.Factory(self.name).Class(klass_name).Super(super_name).Exception(
                    "not found"
                ).error()
                raise Exception(f"Super class {super_name} not found for {klass_name}")
            klass = self.new_derived_klass(super_klass, desc)
        return klass

    def parenting(self, parent_prop, child_prop):
        """parenting sets the parent MO for a give instance, parent and child
        property have to be passed too.
        """

        def _parenting(mo, parent):
            mo.parenting(parent_prop, parent, child_prop)
            # if parent and hasattr(mo, parent_prop) and hasattr(parent, child_prop):
            #     setattr(mo, parent_prop, parent)
            #     setattr(parent, child_prop, mo)

        return _parenting

    def unparenting(self, parent_prop, child_prop):
        """unparenting unsets the parent MO for a given instance, parent and cihld
        property have to be passed too.
        """

        def _unparenting(mo, parent=None):
            parent = parent or getattr(mo, parent_prop)
            mo.unparenting(parent_prop, parent, child_prop)

        return _unparenting

    def childrening(self, child_prop, parent_prop):
        """childrening sets the child MO for a give instance, child and parent
        property have to be passed too.
        """

        def _childrening(mo, child):
            mo.childrening(child_prop, child, parent_prop)
            # if child and hasattr(mo, child_prop) and hasattr(child, parent_prop):
            #     setattr(mo, child_prop, child)
            #     setattr(child, parent_prop, mo)

        return _childrening

    def unchildrening(self, child_prop, parent_prop):
        """unchildrening unsets the childMO for a given insntance, child and parent
        property have to be passed too.
        """

        def _unchildrening(mo, child=None):
            child = child or getattr(mo, child_prop)
            mo.unchildrening(child_prop, child, parent_prop)

        return _unchildrening

    def add_to_list(self, prop):
        """add_to_list adds a value to a list property.
        """

        def _add_to_list(mo, value):
            lista = getattr(mo, prop)
            lista.append(value)
            klass_name = mo.__class__.__name__
            log.Class(klass_name).Update(prop).To(value).Status(mo._mo_status).trace()
            mo.updated(prop, value)

        return _add_to_list

    def del_from_list(self, prop):
        """del_from_list deletes a value from a list property.
        """

        def _del_from_list(mo, value):
            getattr(mo, prop).remove(value)
            klass_name = mo.__class__.__name__
            log.Class(klass_name).Update(prop).To(value).Status(mo._mo_status).trace()
            mo.updated(prop, value)

        return _del_from_list

    def new_derived_klass(self, super_klass, desc):
        """new_derived_klass creates a class using the given super class using
        the given configuration description.
        """
        assert (
            desc["mo"] and desc["flags"] and desc["properties"]
        ), "Incomplete descriptor"
        klass_name = desc["mo"]
        klass_flags = self.set_klass_flags(desc["flags"])
        klass_props = desc["properties"]
        properties_dict = {
            p["name"]: self.set_prop_flags(p["flags"]) for p in klass_props
        }
        attribute_dict = {k: v["default"] for k, v in properties_dict.items()}
        if super_klass.__name__ not in ["MO"]:
            properties_dict.update(super_klass._properties)

        # Create parent/child relation properties
        for k, v in properties_dict.items():
            if v["href"]:
                href, href_klass, href_prop = v["href"].split(":")
                if href == "parent":
                    attribute_dict[f"href_{k}"] = self.parenting(k, href_prop)
                    attribute_dict[f"unhref_{k}"] = self.unparenting(k, href_prop)
                elif href == "child":
                    attribute_dict[f"href_{k}"] = self.childrening(k, href_prop)
                    attribute_dict[f"unhref_{k}"] = self.unchildrening(k, href_prop)
                if v["type"] in ["list:href"]:
                    attribute_dict[f"add_{k}"] = self.add_to_list(k)
                    attribute_dict[f"del_{k}"] = self.del_from_list(k)

        attribute_dict.update(
            {
                "_flags": klass_flags,
                "_properties": properties_dict,
                "_cls_workflows": {},
                "_mo_status": MoStatus.NONE,
                "_mo_workflows": {},
            }
        )
        klass = type(klass_name, (super_klass,), attribute_dict)
        self._repo[klass_name] = klass
        log.Factory(self.name).Create(klass_name).trace()
        return klass

    def process_config(self, config_desc):
        """process_config generates and stores in the repository classes for
        the given configuration data.
        """
        for cd in config_desc:
            self.new_klass(cd)
        return self._repo

    def get_klass(self, klass_name):
        """get_klass returns a class from the internal repository for the
        given name.
        """
        return self._repo.get(klass_name, None)

    def new_mo(self, klass_name, **kwargs):
        """new_mo return a new instance for the given class and with the given
        attributes.
        """
        klass = self.get_klass(klass_name)
        if klass:
            return klass(**kwargs)
        return None

    def get_klass_flags(self, klass_name):
        """get_klass_flags returns all flag options for the given class name.
        """
        klass = self.get_klass(klass_name)
        if klass:
            return klass._flags
        return None

    def get_prop_flags(self, klass_name, prop_name):
        """get_prop_name returns all flag options for the given property for
        the given class.
        """
        klass = self.get_klass(klass_name)
        if klass:
            return [v for k, v in klass._properties.items() if k == prop_name]
        return None

    def dump_klass(self, klass_name):
        """dump_klass dumps all class information for the given class name.
        """
        klass = self.get_klass(klass_name)
        if klass:
            return {
                "mo": klass_name,
                "flags": klass._flags,
                "properties": [
                    {"name": k, "flags": v} for k, v in klass._properties.items()
                ],
            }
        return None

    def dump_tree(self, klass_name):
        """dump_tree dumps all class and all super classes  information for
        the given class.
        """
        result = list()
        klass = self.get_klass(klass_name)
        super_name = klass._flags["super"]
        if super_name is not None:
            result.extend(self.dump_tree(super_name))
        result.append(self.dump_klass(klass_name))
        return result

    def dump(self):
        """dump dumps all classes in the internal respository.
        """
        return [self.dump_klass(k) for k in self._repo.keys()]
