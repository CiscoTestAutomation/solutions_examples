# Overview

Connect to API via Rest Connecor, and create tenant, check the tenant and delete the tenant. This will check if the tenant exists, or not to make sure REST API is properly done.

No python knowledge required. All is done in YAML by using `Blitz`(Quick Trigger).

# Steps

Please check `trigger_datafile.yaml`. The test is written in YAML. So, easy to find corresponding steps in the YAML.

1. Check Tenant doesn't exist
2. Create Tenant
3. Check Tenant exist
4. Delete Tenant
5. Check Tenant was deleted 

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
As quick customize, change `tenant` name under `vars` at top of `trigger_datafile.yaml`.

```
vars:
  tenant: new_tenant_by_pyATS
(snip)
```
### Try #2

Comment whole step4(`delete_tenant`).

```
(snip)
              - contains('.*%{vars.tenant}.*', regex=True)
    # - delete_tenant:
    #     - api:
    #         device: uut
    #         function: apic_rest_post
    #         arguments:
    #           dn: "/api/node/mo/uni/tn-%{vars.tenant}.json"
    #           payload: |
    #             {
    #               "fvTenant": {
    #                   "attributes": {
    #                     "dn": "uni/tn-%{vars.tenant}",
    #                     "status": "deleted"
    #                   },
    #                   "children": []
    #               }
    #             }
    #         include:
    #           - contains_key_value("totalCount", '0')
    - check_tenant_was_deleted:
(snip)
```

`check_tenant_was_deleted` step will be failed. but it's fine since we didn't delete. So, it's expected.

Go to https://sandboxapicdc.cisco.com (Check username/password from `aci_devnet_sandbox.yaml`). 

After login to APIC, click `Tenants` tab. And then the created tenant should be there.





