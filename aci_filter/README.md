# Overview

Connect to API via Rest Connecor, and create filter entry, check the added filter entry (and delete the filter entry). This will check if the filter entry exists, or not to make sure REST API is properly done.

No python knowledge required. All is done in YAML by using `Blitz`(Quick Trigger).

# Steps

Please check `trigger_datafile.yaml`. The test is written in YAML. So, easy to find corresponding steps in the YAML.

1. Check Filter Entry doesn't exist
2. Check Filter Entry doesn't exist under tenant
3. Create Filter Entry under tenant
4. Check Filter Entry exists
5. Check Filter Entry exists under tenant
6. Delete Filter Entry (Optional)

# Preparation

Install pyATS|Genie and Rest Connector.

```
pip install 'pyats[full]' rest.connector
```

# Running

By pyats run job command
```
pyats run job job.py --testbed-file aci_devnet_sandbox.yaml
```

By pyats run genie command (without `job.py`)
```
pyats run genie --testbed-file aci_devnet_sandbox.yaml --trigger-datafile trigger_datafile.yaml --trigger-groups "And('tenant')" --subsection-datafile subsection_datafile.yaml
```

# Try customization in YAML

### Try #1

Above example keeps the filter entry on APIC. So, let's enable `delete` section.

Please uncomment section `delete_filter_entry` in `trigger_datafile.yaml`.

```
    - delete_filter_entry:
        - api:
            device: uut
            function: apic_rest_post
            arguments:
              dn: "/api/node/mo/uni/tn-%{vars.tenant}/flt-%{vars.filter}/e-%{vars.filter_entry}.json"
              payload: |
                {
                  "vzEntry": {
                    "attributes": {
                      "dn": "uni/tn-%{vars.tenant}/flt-%{vars.filter}/e-%{vars.filter_entry}",
                      "status": "deleted"
                    },
                    "children": []
                  }
                }
            include:
              - contains_key_value("totalCount", '0')
```

The deletion can be checked on APIC.



