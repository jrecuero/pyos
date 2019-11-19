from ._loggar import log


class Workflow:

    _ID = 0

    def __init__(self, name):
        self.name = name
        Workflow._ID += 1
        self._id = Workflow._ID
        self.mos = {}
        self.clss = {}

    @property
    def id(self):
        return self._id

    def cls_check_mo_properties(self, mo, prop, value):
        """cls_check_mo_properties checks properties for the given class.
        """
        if prop is None:
            log.Workflow(self.name).Trace(
                f"CLS:{mo.__class__} Instance update to {mo._mo_status}"
            ).trace()
        else:
            old_value = mo.__dict__.get(prop, None)
            log.Workflow(self.name).Trace(
                f"CLS:{mo.__class__} {prop} : {old_value} -> {value}"
            ).trace()

    def mo_check_mo_properties(self, mo, prop, value):
        """mo_check_mo_properties checks properties for the given mo instance.
        """
        if prop is None:
            log.Workflow(self.name).Trace(
                f"CLS:{mo.__class__} Instance update to {mo._mo_status}"
            ).trace()
        else:
            old_value = mo.__dict__.get(prop, None)
            log.Workflow(self.name).Trace(
                f"MO:{mo.__class__} {prop} : {old_value} -> {value}"
            ).trace()

    def add_cls(self, cls, props=None):
        """add_cls adds a new class to the workflow.
        """
        self.clss[cls] = props
        cls.cls_to_workflow(
            self.id, self.cls_check_mo_properties, on_status=props is None
        )

    def add_mo(self, mo, props=None):
        """add_mo adds a new instance to the workflow.
        """
        self.mos[mo] = props
        mo.mo_to_workflow(self.id, self.mo_check_mo_properties, on_status=props is None)
