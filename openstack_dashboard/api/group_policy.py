#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Ronak Shah


from __future__ import absolute_import

from openstack_dashboard.api import neutron

neutronclient = neutron.neutronclient


class EPG(neutron.NeutronAPIDictWrapper):
    """Wrapper for neutron endpoint group."""

    def get_dict(self):
        epg_dict = self._apidict
        epg_dict['epg_id'] = epg_dict['id']
        return epg_dict


class Contract(neutron.NeutronAPIDictWrapper):
    """Wrapper for neutron contract."""

    def get_dict(self):
        contract_dict = self._apidict
        contract_dict['contract_id'] = contract_dict['id']
        return contract_dict


def epg_create(request, **kwargs):
    body = {'endpoint_group': kwargs}
    epg = neutronclient(request).create_endpoint_group(
        body).get('endpoint_group')
    return EPG(epg)

def epg_list(request, **kwargs):
    epgs = neutronclient(request).list_endpoint_groups(
        **kwargs).get('endpoint_groups')
    return [EPG(epg) for epg in epgs]

def epg_get(request, epg_id):
    return {}


def epg_delete(request, epg_id):
    pass


def epg_update(request, epg_id, **kwargs):
    return {}


def contract_create(request, **kwargs):
    pass


def contract_list(request, **kwargs):
    return []


def contract_get(request, contract_id):
    return {}


def contract_delete(request, contract_id):
    pass


def contract_update(request, contract_id, **kwargs):
    return {}


def policyrule_create(request, **kwargs):
    pass


def policyrule_list(request, **kwargs):
    return []


def policyrule_get(request, pr_id):
    return {}


def policyrule_delete(request, pr_id):
    pass


def policyrule_update(request, pr_id, **kwargs):
    return {}


def policyclassifier_create(request, **kwargs):
    pass


def policyclassifier_list(request, **kwargs):
    return []


def policyclassifier_get(request, pc_id):
    return {}


def policyclassifier_delete(request, pc_id):
    pass


def policyclassifier_update(request, pc_id, **kwargs):
    return {}

