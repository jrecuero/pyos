# import json
from conf_data import config_desc
from pydb import Factory, Workflow


def old_factory_01():
    factory = Factory()

    factory.process_config(config_desc)
    # print(f"Class:Uni flags: {factory.get_klass_flags('Uni')}")
    # print(f"Class:Poli flags: {factory.get_klass_flags('Poli')}")
    # print(f"Prop:Poli:tDn flags: {factory.get_prop_flags('Poli', 'tDn')}")

    # print(json.dumps(factory.dump_tree("Poli"), indent=4))
    # print(json.dumps(factory.dump_klass("Poli"), indent=4))
    # print(json.dumps(factory.dump(), indent=4))
    # print(json.dumps(factory.dump_tree("Tenant"), indent=4))

    wf = Workflow("test")
    wf.add_cls(factory.get_klass("Tenant"))

    # uni = factory.new_mo("Uni", dn="uni/1", name="Root node")
    # poli = factory.new_mo("Poli", tDn="uni/poli/1", desc="Config node")
    # print(poli.__dict__)
    tenant = factory.new_mo(
        "Tenant", dn="root/uni", tDn="root/uni/poli", region="us-west"
    )
    # print(tenant.__dict__)

    # wf.add_cls(factory.get_klass("Tenant"))
    # wf.add_mo(tenant)

    tenant.region = "us-east-1"
    tenant.deleted()


def old_factory_02():
    factory = Factory()
    factory.process_config(config_desc)

    wf = Workflow("test")
    wf.add_cls(factory.get_klass("Tenant"))
    region = factory.new_mo(
        "Region", dn="uni/region-[us-west-01]", name="us-west-01", area="us-west"
    )
    wf.add_mo(region)
    tenant_coke = factory.new_mo(
        "Tenant", dn="uni/region-[us-west-01]/coke", name="infra"
    )
    tenant_coke.name = "coke"
    # tenant_coke.region = region
    # tenant_coke.parenting("region", region, "tenants")
    tenant_coke.rel_region(region)

    tenant_pepsi = factory.new_mo(
        "Tenant", dn="uni/region-[us-west-01]/pepsi", name="pepsi"
    )
    tenant_pepsi.rel_region(region)

    print(f"{tenant_coke.region}")
    print(f"{tenant_pepsi.region}")
    print(f"{region.tenants}")


def new_factory():
    tenant_config = [
        {"dn": "uni/region-[us-west-01]/coke", "name": "infra"},
        {"dn": "uni/region-[us-west-01]/pepsi", "name": "infra"},
    ]

    factory = Factory("test")
    factory.process_config(config_desc)

    wf = Workflow("test")
    wf.add_cls(factory.get_klass("Tenant"))
    region = factory.new_mo(
        "Region", dn="uni/region-[us-west-01]", name="us-west-01", area="us-west"
    )
    wf.add_mo(region)

    tenants = []
    for t in tenant_config:
        tenant = factory.new_mo("Tenant", **t)
        tenant.rel_region(region)
        tenants.append(tenant)

    for tenant in tenants:
        print(f"{tenant.region}")
    print(f"{region.tenants}")
    print(f"{wf.kdbase.db}")


if __name__ == "__main__":
    new_factory()
