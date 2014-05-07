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

from horizon import exceptions
from horizon import forms
from horizon import workflows

from openstack_dashboard import api


class AddPolicyRuleAction(workflows.Action):
    with_policy = forms.BooleanField(label=_("Create policy"),
                                     initial=True, required=False)
    name = forms.CharField(max_length=80,
                           label=_("Name"),
                           required=False)
    description = forms.CharField(max_length=80,
                                  label=_("Description"),
                                  required=False)

    def __init__(self, request, *args, **kwargs):
        super(AddPolicyRuleAction, self).__init__(request, *args, **kwargs)

    class Meta:
        name = _("Create Policy Rule")
        help_text = _("Create a new policy rule")


class AddPolicyRuleStep(workflows.Step):
    action_class = AddPolicyRuleAction
    contributes = ("with_policy", "name", "description")

    def contribute(self, data, context):
        context = super(AddPolicyRuleStep, self).contribute(data, context)
        return context


class AddContractAction(workflows.Action):
    name = forms.CharField(max_length=80,
                           label=_("Name"),
                           required=False)
    description = forms.CharField(max_length=80,
                                  label=_("Description"),
                                  required=False)

    def __init__(self, request, *args, **kwargs):
        super(AddContractAction, self).__init__(request, *args, **kwargs)

    class Meta:
        name = _("Create Contract")
        help_text = _("Create a new Contract")


class AddContractStep(workflows.Step):
    action_class = AddContractAction
    contributes = ("name", "description")

    def contribute(self, data, context):
        context = super(AddContractStep, self).contribute(data, context)
        return context


class AddContract(workflows.Workflow):
    slug = "addcontract"
    name = _("Create Contract")
    finalize_button_name = _("Create")
    success_message = _('Create Contract "%s".')
    failure_message = _('Unable to create Contract "%s".')
    success_url = "horizon:project:contracts:index"
    default_steps = (AddContractStep,
                     AddPolicyRuleStep)
    wizard = True

    def format_status_message(self, message):
        return message % self.context.get('name')

    def _create_contract(self, request, context):
        try:
            api.group_policy.contract_create(request, **context)
            return True
        except Exception as e:
            msg = self.format_status_message(self.failure_message) + str(e)
            exceptions.handle(request, msg)
            return False

    def handle(self, request, context):
        contract = self._create_contract(request, context)
        if not contract:
            return False
        if not context['with_policy']:
            return True