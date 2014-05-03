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


class AddEPGAction(workflows.Action):
    name = forms.CharField(max_length=80,
                           label=_("Name"),
                           required=False)
    description = forms.CharField(max_length=80,
                                  label=_("Description"),
                                  required=False)

    def __init__(self, request, *args, **kwargs):
        super(AddEPGAction, self).__init__(request, *args, **kwargs)

    class Meta:
        name = _("Create EPG")
        help_text = _("Create a new EPG")


class AddEPGStep(workflows.Step):
    action_class = AddEPGAction
    contributes = ("name", "description")

    def contribute(self, data, context):
        context = super(AddEPGStep, self).contribute(data, context)
        return context


class AddEPG(workflows.Workflow):
    slug = "addepg"
    name = _("Create EPG")
    finalize_button_name = _("Create")
    success_message = _('Create EPG "%s".')
    failure_message = _('Unable to create EPG "%s".')
    success_url = "horizon:project:endpoint_groups:index"
    default_steps = (AddEPGStep,)

    def format_status_message(self, message):
        return message % self.context.get('name')

    def handle(self, request, context):
        try:
            api.group_policy.epg_create(request, **context)
            return True
        except Exception as e:
            msg = self.format_status_message(self.failure_message) + str(e)
            exceptions.handle(request, msg)
            return False
