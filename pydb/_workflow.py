from ._loggar import log


class KlassSeedDbase:
    """KlassSeedDbase class stores information for every class that has an
    active instance.
    """

    _repo = None

    def __init__(self):
        if KlassSeedDbase._repo is None:
            KlassSeedDbase._repo = {}

    @property
    def db(self):
        """db property returns the class _repo attribute that contains all
        KlassSeed instances.
        """
        return KlassSeedDbase._repo

    def add(self, kname=None, kseed=None):
        """add adds a new KlassSeed instance to the repository.
        """
        if kname:
            kseed = self.db.get(kname, None)
            if kseed is None:
                kseed = KlassSeed(kname)
                self.db[kname] = kseed
        elif kseed:
            if self.db.get(kseed.name, None) is None:
                self.db[kseed.name] = kseed
        else:
            return None
        return kseed


class KlassSeed:
    """KlassSeed class stores information for every class registered to a
    workflow. It shows if there is at least one instance for that class
    available, so workflow shoul fetcher for it.
    Flag should be cleared only if all instances have been deleted.
    """

    def __init__(self, klass_name):
        self.klass_name = klass_name
        self.active = False
        KlassSeedDbase().add(kseed=self)

    @property
    def name(self):
        return self.klass_name


class DepSeed:
    """DepSeed class stores a particular dependency for a workflow. It could
    be a class with/without properties, or an instance with/without properties.

    Instance registered to the seed means there is at least one instance for
    that class, so the KlassSeed should be activated.
    """

    def __init__(self, klass_seed, instance=None, props=None):
        self.klass_seed = klass_seed
        self.instance = instance
        if self.instance:
            self.klass_seed.active = True
        self.props = props if props else []


class SeedRelation:
    """SeedRelation allows to fetch instance from one class to another.
    """

    def __init__(self, klass_one, klass_two, rel_one_2_two, rel_two_2_one):
        self.klass_one = klass_one
        self.klass_two = klass_two
        self.rel_one_2_two = rel_one_2_two
        self.rel_two_2_one = rel_two_2_one


class Workflow:

    _ID = 0

    def __init__(self, name="default"):
        self.name = name
        Workflow._ID += 1
        self._id = Workflow._ID
        self.mos_props = {}
        self.clss_props = {}
        self.mo_to_mo_map = {}
        self.mos = {}
        self.flags = {}
        self.seeds = {}
        self.relations = []
        self.enabled = False

    @property
    def id(self):
        return self._id

    @property
    def kdbase(self):
        return KlassSeedDbase()

    def start(self):
        """start starts the workflow.
        """
        self.enabled = True
        self.audit()

    def stop(self):
        """stop stops the workflow.
        """
        self.enabled = False

    def audit(self):
        """audit will check every seed in the workflow to check status for
        each one.
        """
        if self.enabled:
            pass

    def add_seed(self, klass_name, instance=None, props=None):
        """add_seed adds a new dependency seed to the workflow.
        """
        klass_seed = KlassSeed(klass_name)
        self.seeds[klass_name] = DepSeed(klass_seed, instance, props)

    def add_relation(self, klass_one, klass_two, rel_one_2_two, rel_two_2_one):
        """add_relation adds a new relation between two seeds.
        """
        rel = SeedRelation(klass_one, klass_two, rel_one_2_two, rel_two_2_one)
        self.relations.append(rel)

    def cls_check_mo_properties(self, mo, prop, value):
        """cls_check_mo_properties checks properties for the given class.
        """
        seed = self.seeds.get(mo.__class__.__name__, None)
        if seed is None:
            return
        if prop is None:
            log.Workflow(self.name).Trace(
                f"CLS:{mo.__class__} @ {mo._mo_status}"
            ).trace()
        else:
            old_value = mo.__dict__.get(prop, None)
            log.Workflow(self.name).Trace(
                f"CLS:{mo.__class__} @ {mo._mo_status} {prop} : {old_value} -> {value}"
            ).trace()

    def mo_check_mo_properties(self, mo, prop, value):
        """mo_check_mo_properties checks properties for the given mo instance.
        """
        seed = self.seeds.get(mo.__class__.__name__, None)
        if seed is None:
            return
        if prop is None:
            log.Workflow(self.name).Trace(
                f"CLS:{mo.__class__} @ {mo._mo_status}"
            ).trace()
        else:
            old_value = mo.__dict__.get(prop, None)
            log.Workflow(self.name).Trace(
                f"MO:{mo.__class__} @ {mo._mo_status} {prop} : {old_value} -> {value}"
            ).trace()

    def add_cls(self, cls, props=None):
        """add_cls adds a new class to the workflow.
        """
        self.add_seed(cls.__name__, instance=None, props=props)
        self.clss_props[cls] = props
        cls.cls_to_workflow(
            self.id, self.cls_check_mo_properties, on_status=props is None
        )

    def add_mo(self, mo, props=None):
        """add_mo adds a new instance to the workflow.
        """
        self.add_seed(mo.__class__.__name__, instance=mo, props=props)
        self.mos_props[mo] = props
        mo.mo_to_workflow(self.id, self.mo_check_mo_properties, on_status=props is None)
