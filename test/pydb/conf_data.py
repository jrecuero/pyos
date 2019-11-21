config_desc = [
    {
        "mo": "DN",
        "flags": {"concrete": False, "label": "Identificable base object"},
        "properties": [
            {
                "name": "dn",
                "flags": {
                    "editable": False,
                    "default": "default",
                    "label": "Unique identification",
                },
            },
            {
                "name": "name",
                "flags": {"default": "", "label": "User defined instance name"},
            },
            {
                "name": "oper-state",
                "flags": {"default": None, "label": "Instance operational state"},
            },
        ],
    },
    {
        "mo": "Account",
        "flags": {"super": "DN", "label": "Account information"},
        "properties": [
            {"name": "proxy", "flags": {"default": "", "label": "Account proxy"}},
            {"name": "vendor", "flags": {"default": "", "label": "Account vendor"}},
        ],
    },
    {
        "mo": "Region",
        "flags": {"super": "DN", "label": "Region information"},
        "properties": [
            {
                "name": "area",
                "flags": {"default": "none", "label": "Region location area"},
            },
            {
                "name": "tenants",
                "flags": {
                    "href": "child:Tenant:region",
                    "type": "list:href",
                    "default": None,
                    "label": "Region tenants",
                },
            },
        ],
    },
    {
        "mo": "Tenant",
        "flags": {"super": "DN", "label": "Tenant information"},
        "properties": [
            {
                "name": "region",
                "flags": {
                    "href": "parent:Region:tenants",
                    "type": "str:href",
                    "default": None,
                    "label": "Tenant region",
                },
            }
        ],
    },
    {
        "mo": "HubCtx",
        "flags": {"super": "DN", "label": "Transit gateway information"},
        "properties": [
            {
                "name": "asn",
                "flags": {
                    "default": 0,
                    "type": "int:base",
                    "label": "Transit gateway asn identifier",
                },
            },
            {
                "name": "vrf",
                "flags": {"default": "default", "label": "VRF group identifier"},
            },
        ],
    },
]
