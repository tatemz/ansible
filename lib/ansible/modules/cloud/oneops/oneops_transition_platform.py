#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oneops_transition_platform

short_description: A module for provisioning a OneOps platform inside of an assembly

version_added: "2.9"

description:
    - "OneOps documentation: http://oneops.com/overview/documentation.html"

options:
    oneops_host:
        description:
            - The hostname of the OneOps instance
        required: true
        type: str
    api_key:
        description:
            - A user's API key for communicating with the OneOps API
        required: true
        type: str
    email:
        description:
            - A user's email for communicating with the OneOps API
        required: true
        type: str
    organization:
        description:
            - The name of the organization to create the platform in
        required: true
        type: str
    assembly:
        description:
            - A hash/dictionary of assembly configuration used to add the platform
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the assembly the platform will be under
                required: true
                type: str
    platform:
        description:
            - A hash/dictionary of platform configuration used to create the platform
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the platform
                required: true
                type: str
            comments:
                description:
                    - Comments for your platform. Visible in the OneOps UI
                required: false
                type: str
                default: "This platform created by the OneOps Ansible module"
            description:
                description:
                    - A useful description for your platform
                required: false
                type: str
                default: "This platform created by the OneOps Ansible module"
            pack:
                description:
                    - A hash/dictionary of platform OneOps pack configuration used to create the platform
                required: false
                type: dict
                suboptions:
                    source:
                        description:
                            - The source of the OneOps pack
                        required: false
                        type: str
                        default: "oneops"
                    name:
                        description:
                            - The name of the OneOps pack
                        required: false
                        type: str
                        default: "custom"
                    major_version:
                        description:
                            - The major version number of the OneOps pack
                        required: false
                        type: str
                        default: "1"
                    version:
                        description:
                            - The minor version number of the OneOps pack
                        required: false
                        type: str
                        default: "1"

author:
    - Tate Barber (@tatemz)
    - Samuel Hymen (@s0hyman)
'''

EXAMPLES = '''
# Create a new platform
- name: Create my-platform in my-org in OneOps
  oneops:
    oneops_host: oneops.example.com
    api_key: 12345abcde
    email: sam.walton@walmart.com
    organization: my-organization
    platform:
        name: my-platform
        comments: A comment attached to my platform that can be read in OneOps UI
        description: A description of my platform
        pack: 
            source: my-source
            name: my-pack
            major_version: '1'
            version: '1'
'''

RETURN = '''
platform:
    description: The platform object from the OneOps API
    returned: when success
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneops import module_argument_spec
from ansible.module_utils.oneops import oneops_api


def enable_platform(module, state):
    if oneops_api.OneOpsTransitionPlatform.exists(module):
        state.update(changed=True)  # TODO: Determine if platform is already enabled
        oneops_api.OneOpsTransitionPlatform.enable(module)

    module.exit_json(**state)


def disable_platform(module, state):
    if oneops_api.OneOpsTransitionPlatform.exists(module):
        state.update(changed=True)  # TODO: Determine if platform is already disabled
        oneops_api.OneOpsTransitionPlatform.disable(module)

    module.exit_json(**state)


def get_oneops_transition_platform_module():
    return AnsibleModule(
        argument_spec=module_argument_spec.get_oneops_transition_platform_module_argument_spec(),
        supports_check_mode=True,
    )


def run_module():
    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    state = dict(
        changed=False,
        platform=dict(),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = get_oneops_transition_platform_module()

    if module.params['platform']['state'] == 'enabled':
        return enable_platform(module, state)

    if module.params['platform']['state'] == 'disabled':
        return disable_platform(module, state)

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**state)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**state)


def main():
    run_module()


if __name__ == '__main__':
    main()
