#!/usr/bin/env python

import requests
import xml.etree.ElementTree as ET
import sys
import math

_author_ = 'Dominik Schuster'


# Get memory allocated right now in VDCNAME
class MemoryAllocation:
    def __init__(self, verbose, base_url, user, password, environment, headers, url_filter):
        self.verbose = verbose
        self.user = user
        self.password = password
        self.organization = organization
        self.session = None
        self.url_filter = url_filter
        self.headers = headers
        self.base_url = base_url
        self.memory_allocated = 0
        self.page = 1

        # Call return_allocated_memory as long as http status code is 200
        while self.get_raw_xml(in_fields='name,memoryAllocationMB', page=self.page) is not None:
            self.return_allocated_memory(self.get_raw_xml(in_fields='name,memoryAllocationMB,isDeployed', page=self.page))
            self.page += 1
        # Print memory sum
        self.print_allocated_memory_in_gb(self.memory_allocated)
        self.logout()

    def login(self):
        if self.session:
            self.logout()
        self.session = requests.Session()
        auth = ('%s@%s' % (self.user, self.organization), self.password)
        r = self.session.post(self.base_url + 'sessions',
                              headers=self.headers, verify=True, auth=auth)
        if 'x-vcloud-authorization' in r.headers:
            self.session.headers.update({'x-vcloud-authorization': r.headers['x-vcloud-authorization']})
        else:
            print("Couldn't login")
            print(r)
            sys.exit(-1)

    # Logs you out after script is finished
    def logout(self):
        if self.session:
            url = self.base_url + 'session'
            self.session.delete(url)
            self.session = None

    # Gets raw xml with query specified in url_filter
    def get_raw_xml(self, in_type='vApp', in_fields=None, out_format='idrecords',
                    limit=None, page=1):
        if not self.session:
            self.login()
        url = self.base_url + 'query?' + self.url_filter
        # VCD api has a page_size limit which is annoying
        # because you have to call the api 5 times if you have 600 vApps
        page_size = 128
        if limit and limit < page_size:
            page_size = limit

        # Do a get api call to get all vApps in filter set
        params = {'pageSize': page_size, 'type': in_type, 'format': out_format,
                  'fields': in_fields, 'filter': self.url_filter, 'filterEncoded': True, 'page': page}

        r = self.session.get(url, headers=self.headers, verify=True, params=params)

        if r.status_code != 200:
            return None

        # Returns in fact not pretty xml
        return r.text

    # Does a addition for every memory found in xml that we get from
    # __query function
    def return_allocated_memory(self, query_data):
        # Convert xml into dictionary
        root = ET.fromstring(query_data)
        # Iterate over dictionary
        for child in root:
            if child.tag == "{http://www.vmware.com/vcloud/v1.5}VAppRecord":
                is_deployed = child.attrib.get('isDeployed')
                if is_deployed == 'true':
                    try:
                        self.memory_allocated += int(child.attrib.get('memoryAllocationMB'))
                    except TypeError:
                        self.memory_allocated += 0

        return self.memory_allocated

    # Prints the memory sum in gigabyte
    def print_allocated_memory_in_gb(self, memory_allocated):
        sum_in_gb = int(math.ceil(memory_allocated / 1024))
        print("Memory allocated in BaseCommitment: " + str(sum_in_gb) + " GB")
