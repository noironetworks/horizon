
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


class SelectPolicyRuleAction(workflows.Action):
    rule = forms.MultipleChoiceField(
        label=_("Policy Rules"),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        help_text=_("Create a contract with selected rules."))

    class Meta:
        name = _("Rules")
        help_text = _("Select policy-rules for your contract.")

    def populate_rule_choices(self, request, context):
        try:
            tenant_id = self.request.user.tenant_id
            rules = api.group_policy.policyrule_list(request,
                                                     tenant_id=tenant_id)
            for r in rules:
                r.set_id_as_name_if_empty()
            rules = sorted(rules,
                           key=lambda rule: rule.name)
            rule_list = [(rule.id, rule.name) for rule in rules]
        except Exception as e:
            rule_list = []
            exceptions.handle(request,
                              _('Unable to retrieve rules (%(error)s).') % {
                                  'error': str(e)})
        # TODO - Remove this
        rule_list = [('rule-uuid1', 'rule-1'), ('rule-uuid2', 'rule-2')]
        return rule_list


class SelectPolicyRuleStep(workflows.Step):
    action_class = SelectPolicyRuleAction
    contributes = ("policy_rules",)

    def contribute(self, data, context):
        if data:
            rules = self.workflow.request.POST.getlist("policy_rule")
            if rules:
                rules = [r for r in rules if r != '']
                context['policy_rules'] = rules
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
                     SelectPolicyRuleStep)
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


class SelectPolicyClassifierAction(workflows.Action):
    classifier = forms.MultipleChoiceField(
        label=_("Policy Classifier"),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        help_text=_("Create a policy with selected classifier."))

    class Meta:
        name = _("Classifiers")
        help_text = _("Select classifiers for your policy-rule.")

    def populate_classifier_choices(self, request, context):
        try:
            tenant_id = self.request.user.tenant_id
            classifiers = api.group_policy.policyclassifier_list(request,
                tenant_id=tenant_id)
            for c in classifiers:
                c.set_id_as_name_if_empty()
            classifiers = sorted(classifiers,
                           key=lambda rule: rule.name)
            classifier_list = [(c.id, c.name) for c in classifiers]
        except Exception as e:
            classifier_list = []
            exceptions.handle(request,
                              _('Unable to retrieve classifiers (%(error)s).')
                              % {'error': str(e)})
        # TODO - Remove this
        classifier_list = [('classifier-uuid1', 'classifier-1'), 
                           ('classifier-uuid2', 'classifier-2')]
        return classifier_list


class SelectPolicyActionAction(workflows.Action):
    action = forms.MultipleChoiceField(
        label=_("Policy Action"),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        help_text=_("Create a policy-rule with selected action."))

    class Meta:
        name = _("actions")
        help_text = _("Select actions for your policy-rule.")

    def populate_action_choices(self, request, context):
        try:
            tenant_id = self.request.user.tenant_id
            actions = api.group_policy.policyaction_list(request,
                tenant_id=tenant_id)
            for a in actions:
                a.set_id_as_name_if_empty()
            actions = sorted(actions,
                           key=lambda rule: rule.name)
            action_list = [(a.id, a.name) for a in actions]
        except Exception as e:
            action_list = []
            exceptions.handle(request,
                              _('Unable to retrieve actions (%(error)s).')
                              % {'error': str(e)})
        # TODO - Remove this
        action_list = [('action-uuid1', 'action-1'), 
                           ('action-uuid2', 'action-2')]
        return action_list


class SelectPolicyActionStep(workflows.Step):
    action_class = SelectPolicyActionAction
    contributes = ("policy_actions",)

    def contribute(self, data, context):
        if data:
            actions = self.workflow.request.POST.getlist(
                "policy_action")
            if actions:
                actions = [a for a in actions if a != '']
                context['policy_actions'] = actions
            return context


class SelectPolicyClassifierStep(workflows.Step):
    action_class = SelectPolicyClassifierAction
    contributes = ("policy_classifiers",)

    def contribute(self, data, context):
        if data:
            classifiers = self.workflow.request.POST.getlist(
                "policy_classifier")
            if classifiers:
                classifiers = [c for c in classifiers if c != '']
                context['policy_classifiers'] = classifiers
            return context


class AddPolicyRuleAction(workflows.Action):
    name = forms.CharField(max_length=80,
                           label=_("Name"),
                           required=False)
    description = forms.CharField(max_length=80,
                                  label=_("Description"),
                                  required=False)

    def __init__(self, request, *args, **kwargs):
        super(AddPolicyRuleAction, self).__init__(request, *args, **kwargs)

    class Meta:
        name = _("Create Policy-Rule")
        help_text = _("Create a new Policy-Rule")


class AddPolicyRuleStep(workflows.Step):
    action_class = AddPolicyRuleAction
    contributes = ("name", "description")

    def contribute(self, data, context):
        context = super(AddPolicyRuleStep, self).contribute(data, context)
        return context


class AddPolicyRule(workflows.Workflow):
    slug = "addpolicyrule"
    name = _("Create Policy-Rule")
    finalize_button_name = _("Create")
    success_message = _('Create Policy-Rule "%s".')
    failure_message = _('Unable to create Policy-Rule "%s".')
    success_url = "horizon:project:contracts:index"
    default_steps = (AddPolicyRuleStep,
                     SelectPolicyClassifierStep,)
#                     SelectPolicyActionStep)
    wizard = True

    def format_status_message(self, message):
        return message % self.context.get('name')

    def _create_policyrule(self, request, context):
        try:
            api.group_policy.policyrule_create(request, **context)
            return True
        except Exception as e:
            msg = self.format_status_message(self.failure_message) + str(e)
            exceptions.handle(request, msg)
            return False

    def handle(self, request, context):
        policy_rule = self._create_policyrule(request, context)
        if not policy_rule:
            return False
        if (not context['with_classifier'] and
            not context['with_action']):
            return True


class AddClassifierAction(workflows.Action):
    name = forms.CharField(max_length=80,
                           label=_("Name"),
                           required=False)
    protocol = forms.ChoiceField(
        label=_("Protocol"),
        choices=[('tcp', _('TCP')),
                 ('udp', _('UDP')),
                 ('icmp', _('ICMP')),
                 ('any', _('ANY'))],)
    min_port = forms.CharField(
        max_length=80,
        label=_("Port Range(Min)"),
        required=False)
    max_port = forms.CharField(
        max_length=80,
        label=_("Port Range(Max)"),
        required=False)
    direction = forms.ChoiceField(
        label=_("Direction"),
        choices=[('in', _('IN')),
                 ('out', _('OUT')),
                 ('bi', _('BI')),])
    action = forms.ChoiceField(
        label=_("Action"),
        choices=[('allow', _('ALLOW')),
                 ('redirect', _('REDIRECT'))],)

    def __init__(self, request, *args, **kwargs):
        super(AddClassifierAction, self).__init__(request, *args, **kwargs)

    class Meta:
        name = _("Create Contract")
        help_text = _("Create a new Contract")


class AddClassifierStep(workflows.Step):
    action_class = AddClassifierAction
    contributes = ("name", "protocol", "min_port", "max_port", "direction", "action")

    def contribute(self, data, context):
        context = super(AddClassifierStep, self).contribute(data, context)
        return context


class AddPolicyClassifier(workflows.Workflow):
    slug = "addpolicyclassifier"
    name = _("Create Classifier")
    finalize_button_name = _("Create")
    success_message = _('Create Classifier "%s".')
    failure_message = _('Unable to create Classifier "%s".')
    success_url = "horizon:project:contracts:index"
    default_steps = (AddClassifierStep,)

    def format_status_message(self, message):
        return message % self.context.get('name')

    def _create_classifer(self, request, context):
        try:
            api.group_policy.policyclassifier_create(request, **context)
            return True
        except Exception as e:
            msg = self.format_status_message(self.failure_message) + str(e)
            exceptions.handle(request, msg)
            return False

    def handle(self, request, context):
        classifier = self._create_classifer(request, context)
        if not classifier:
            return False
        return True
