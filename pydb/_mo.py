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
        - super : super class.
        - config: configuration or no class.
        - concrete: concrete or abstract class.
        - access: who can access to the class.
        - owner: class owner.
        - deletable: instance can be the deleted.
        - editable: instance can be edited.
        - visible: instance is visible.
        - label: user defined class description.

    For every class property there are a set of options too.

    Property options:
        - config: configuration or not property.
        - deletable: property can be deleted.
        - editable: property can be edited.
        - visible: property is visible.
        - type: property type.
        - auto: auto generated property.
        - default: property default value.
        - validate: method that validate property value.
    """

    def __init__(self, **kwargs):
        self._mo_status = MoStatus.INIT
        self._mo_workflows = {}
        # set default values for all properties provisioned for the given class.
        for k in [k for k in dir(self) if not k.startswith("_")]:
            setattr(self, k, getattr(self, k, None))
        # update values for properties given when instance is created.
        # for k, v in [(k, v) for k, v in kwargs.items() if hasattr(self, k)]:
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._mo_status = MoStatus.CREATED

    # def __process_get_attr(self, attr):
    #    print(f"attribute {attr} was read")
    #    return False

    def __process_set_attr(self, attr, value):
        """__process_set_attr process any instance attribute that is going to
        be set/updated.
        """
        if not hasattr(self, attr):
            klass_name = self.__class__.__name__
            log.Class(klass_name).Exception(
                f"Can not create new property: {attr}"
            ).error()
            raise Exception(f"{klass_name} can not create new property: {attr}")
        # prop = (
        #     self._properties.get(attr, None)
        #     if getattr(self, "_properties", None)
        #     else None
        # )
        # print(f"attribute {attr} set to {value} [{prop}]")

    # def __getattr__(self, attr):
    #    try:
    #        return self.__getattribute__(attr)
    #    except Exception:
    #        return self.__process_get_attr(attr)

    def __setattr__(self, attr, value):
        """__setattr__ overwrites default method in orde to provide special
        processing when any attribute is being set/updated.
        """
        self.__process_set_attr(attr, value)
        klass_name = self.__class__.__name__
        log.Class(klass_name).Update(attr).To(value).Status(self._mo_status).trace()
        return super(MO, self).__setattr__(attr, value)

    @classmethod
    def cls_to_workflow(cls, wf_id, wf_cb):
        """cls_to_workflow appends a worflow callback for the class.
        """
        cls._cls_workflows.setdefault(wf_id, []).append(wf_cb)

    def mo_to_workflow(self, wf_id, wf_cb):
        """mo_to_workflow appends a workflow callback for the instance.
        """
        self._mo_workflows.setdefault(wf_id, []).append(wf_cb)

    def __str__(self):
        """___str___ overwrites default method to return a string
        representation for the instance.
        """
        return f"{self.__dict__}"
