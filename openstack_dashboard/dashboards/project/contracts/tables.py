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

from django.utils.translation import ugettext_lazy as _

from horizon import tables


class AddContractLink(tables.LinkAction):
    name = "addcontract"
    verbose_name = _("Create Contract")
    url = "horizon:project:contracts:addcontract"
    classes = ("ajax-modal", "btn-addcontract",)


class AddPolicyRulesLink(tables.LinkAction):
    name = "addpolicyrules"
    verbose_name = _("Create Policy-Rule")
    url = "horizon:project:contracts:addpolicyrule"
    classes = ("ajax-modal", "btn-addpolicyrule",)


class AddPolicyClassifiersLink(tables.LinkAction):
    name = "addpolicyclassifiers"
    verbose_name = _("Create Policy-Classifier")
    url = "horizon:project:contracts:addpolicyclassifier"
    classes = ("ajax-modal", "btn-addpoliclassifier",)


class ContractsTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_("Name"))

    class Meta:
        name = "contractstable"
        verbose_name = _("Contracts")
        table_actions = (AddContractLink,)
        #row_actions = (UpdateFirewallLink, DeleteFirewallLink)


class PolicyRulesTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_("Name"))

    class Meta:
        name = "policyrulestable"
        verbose_name = _("PolicyRules")
        table_actions = (AddPolicyRulesLink,)
        #row_actions = (UpdateFirewallLink, DeleteFirewallLink)


class PolicyClassifiersTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_("Name"))

    class Meta:
        name = "policyclassifierstable"
        verbose_name = _("PolicyClassifiers")
        table_actions = (AddPolicyClassifiersLink,)
        #row_actions = (UpdateFirewallLink, DeleteFirewallLink)
