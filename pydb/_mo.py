from ._loggar import log


class MoStatus:

    NONE = "none"
    INIT = "init"
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"


class MO:
    """MO is the base class any created class will implement.

    Class is created using a configuration data with these options.

    Class options:
        - super : super class. default: None
        - config: configuration or no class. default: True
        - concrete: concrete or abstract class. default: True
        - access: who can access to the class. default: all
        - owner: class owner. default: system
        - deletable: instance can be the deleted. default: True
        - editable: instance can be edited. default: True
        - visible: instance is visible. default: True
        - label: user defined class description. default: ''

    For every class property there are a set of options too.

    Property options:
        - config: configuration or not property. default: True
        - deletable: property can be deleted. default: True
        - editable: property can be edited. default: True
        - visible: property is visible. default: True
        - type: property type. default: str:base
        - auto: auto generated property. default: False
        - default: property default value. default: None
        - validate: method that validate property value. default: None
        - href: property relation with other instance. default: None
        - label: user defined property description. default: ''
    """

    def __init__(self, **kwargs):
        self._mo_status = MoStatus.INIT
        self._mo_workflows = {}
        # set default values for all properties provisioned for the given class.
        for k in [k for k in dir(self) if not k.startswith("_")]:
            prop = self._properties.get(k, None)
            if prop and prop["href"]:
                setattr(self, k, list())
            else:
                setattr(self, k, getattr(self, k, None))
        # update values for properties given when instance is created.
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.created()

    # def __process_get_attr(self, attr):
    #    print(f"attribute {attr} was read")
    #    return False

    def __call_workflows(self, attr=None, value=None):
        """__call_workflows calls to all Class and Instance workflows.
        """
        # Call class workflows callbacks.
        workflows = self.__class__._cls_workflows.values()
        for wf_cb, mo_st in [(cb, st) for wf in workflows for (cb, st) in wf]:
            # if not mo_st or (mo_st and attr is None):
            wf_cb(self, attr, value)
        # Call instance workflows callbacks.
        workflows = self._mo_workflows.values()
        for wf_cb, mo_st in [(cb, st) for wf in workflows for (cb, st) in wf]:
            # if not mo_st or (mo_st and attr is None):
            wf_cb(self, attr, value)

    def __process_set_attr(self, attr, value):
        """__process_set_attr process any instance attribute that is going to
        be set/updated.
        """
        if self._properties.get(attr, None) is None:
            return
        klass_name = self.__class__.__name__
        if not hasattr(self, attr):
            log.Class(klass_name).Exception(
                f"can not create new property: {attr}"
            ).error()
            raise Exception(f"{klass_name} can not create new property: {attr}")
        attr_prop = self._properties.get(attr, None)
        # if attr_prop is None:
        #     log.Class(klass_name).Property(attr).Exception(f"Unknowm property").error()
        #     raise Exception(f"{klass_name}.{attr} Unknown property")
        if (
            attr_prop
            and not attr_prop.get("editable")
            and self._mo_status not in [MoStatus.INIT]
        ):
            log.Class(klass_name).Propertu(attr).Exception(
                f"Only read property"
            ).error()
            raise Exception(f"{klass_name}.{attr} Only read property")
        self.updated(attr, value)

    # def __getattr__(self, attr):
    #    try:
    #        return self.__getattribute__(attr)
    #    except Exception:
    #        return self.__process_get_attr(attr)

    def __setattr__(self, attr=None, value=None):
        """__setattr__ overwrites default method in orde to provide special
        processing when any attribute is being set/updated.
        """
        self.__process_set_attr(attr, value)
        klass_name = self.__class__.__name__
        log.Class(klass_name).Update(attr).To(value).Status(self._mo_status).trace()
        return super(MO, self).__setattr__(attr, value)

    @classmethod
    def cls_to_workflow(cls, wf_id, wf_cb, on_status=False):
        """cls_to_workflow appends a worflow callback for the class.
        """
        cls._cls_workflows.setdefault(wf_id, []).append((wf_cb, on_status))

    def mo_to_workflow(self, wf_id, wf_cb, on_status=False):
        """mo_to_workflow appends a workflow callback for the instance.
        """
        self._mo_workflows.setdefault(wf_id, []).append((wf_cb, on_status))

    def created(self):
        """created sets the mo in CREATED state.
        """
        self._mo_status = MoStatus.CREATED
        self.__call_workflows()

    def updated(self, attr, value):
        """updated sets the mo in UPDATED state.
        """
        # Workflows are not called in INIT status in order to avoid flood of
        # notifications when MOs are being created.
        if self._mo_status not in [MoStatus.INIT]:
            self._mo_status = MoStatus.UPDATED
            self.__call_workflows(attr, value)

    def deleted(self):
        """deleted sets the mo in DELETED state.
        """
        self._mo_status = MoStatus.DELETED
        self.__call_workflows()

    def parenting(self, parent_prop, parent, child_prop):
        """parenting sets the parent MO for a give instance, parent and child
        property have to be passed too.
        """
        if parent and hasattr(self, parent_prop) and hasattr(parent, child_prop):
            parent_prop_flags = self._properties[parent_prop]
            if parent_prop_flags["type"] in ["list:href"]:
                getattr(self, f"add_{parent_prop}")(parent)
            else:
                setattr(self, parent_prop, parent)
            child_prop_flags = parent._properties[child_prop]
            if child_prop_flags["type"] in ["list:href"]:
                getattr(parent, f"add_{child_prop}")(self)
            else:
                getattr(parent, child_prop).append(self)

    def childrening(self, child_prop, child, parent_prop):
        """childrening sets the child MO for a give instance, child and parent
        property have to be passed too.
        """
        if child and hasattr(self, child_prop) and hasattr(child, parent_prop):
            child_prop_flags = self._properties[child_prop]
            if child_prop_flags["type"] in ["list:href"]:
                getattr(self, f"add_{child_prop}")(child)
            else:
                getattr(self, child_prop).append(child)
            parent_prop_flags = child._properties[parent_prop]
            if parent_prop_flags["type"] in ["list:href"]:
                getattr(child, f"add_{parent_prop}")(self)
            else:
                setattr(child, parent_prop, self)

    # def __str__(self):
    #     """___str___ overwrites default method to return a string
    #     representation for the instance.
    #     """
    #     props = "\n  ".join(
    #         [f"{k} : {self.__dict__.get(k)}" for k in self._properties.keys()]
    #     )
    #     return f"{self.__class__.__name__}:\n  {props}"
