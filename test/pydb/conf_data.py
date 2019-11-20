config_desc = [
    {
        "mo": "DN",
        "flags": {"concrete": False, "label": "Identificable base object"},
        "properties": [
            {"name": "dn", "flags": {"editable": False, "default": "default"}},
            {"name": "name", "flags": {"default": ""}},
        ],
    },
    {
        "mo": "Account",
        "flags": {"super": "DN", "label": "Account information"},
        "properties": [{"name": "proxy", "flags": {"default": ""}}],
    },
    {
        "mo": "Region",
        "flags": {"super": "DN", "label": "Region information"},
        "properties": [
            {"name": "area", "flags": {"default": "none"}},
            {
                "name": "tenants",
                "flags": {
                    "href": "child:Tenant:region",
                    "type": "str:href",
                    "default": None,
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
                    "type": "list:href",
                    "default": None,
                },
            }
        ],
    },
]
