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

from horizon import tabs
from horizon import workflows

from openstack_dashboard.dashboards.project.endpoint_groups \
    import tabs as epg_tabs
from openstack_dashboard.dashboards.project.endpoint_groups \
    import workflows as epg_workflows

EPGTabs = epg_tabs.EPGTabs

AddEPG = epg_workflows.AddEPG


class IndexView(tabs.TabView):
    tab_group_class = (EPGTabs)
    template_name = 'project/endpoint_groups/details_tabs.html'


class AddEPGView(workflows.WorkflowView):
    workflow_class = AddEPG
    template_name = "project/endpoint_groups/addepg.html"
