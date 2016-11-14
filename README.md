Tool to get memory allocated from vcd triggering its api

## Description

This tool as it is now can only get the allocated memory from a virtual
cloud director application and its organization. It collects all memory
provisioned in a virtual data center configured in virtual cloud director.

Example json file
```json
{
  "headers": {"Accept": "application/*+xml;version=5.5"},
  "user": "test",
  "password": "test123",
  "base_url": "https://test.vcd.com/api/",
  "url_filter": "filter=(vdcName==test_vdc)"
  "organization": "my_organization"
}
```

This calls the rest api of "https://test.vcd.com/api/" with given user
credentials and gets all memory allocated by virtual machines in
 "my_organization".