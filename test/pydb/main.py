# import json
from conf_data import config_desc
from pydb import Factory, Workflow


if __name__ == "__main__":
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
