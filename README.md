# tagtamerv2

Refer to Tag Tamer solution document for Install and Usage documentation.

<<pdf link goes here>>


***

## File Structure

```
.
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── deployment
│   ├── build-s3-dist.sh
│   ├── run-unit-tests.sh
│   ├── tagtamer_private.yaml
│   └── tagtamer_public.yaml
├── LICENSE-SUMMARY
├── LICENSE.txt
├── NOTICE.txt
├── README.md
└── source
    ├── code
    │   ├── config.py
    │   ├── get_tag_groups.py
    │   ├── iam.py
    │   ├── resources_tags.py
    │   ├── role-based-tagger.py
    │   ├── service_catalog.py
    │   ├── set_tag_groups.py
    │   ├── ssm_parameter_store.py
    │   ├── tag_tamer_parameters.json
    │   ├── tag_tamer.py
    │   ├── tag-tamer-run.py
    │   └── templates
    │       ├── actions.html
    │       ├── display-tag-groups.html
    │       ├── edit-tag-group.html
    │       ├── find-config-rules.html
    │       ├── find-tags.html
    │       ├── found-tags.html
    │       ├── index.html
    │       ├── logout.html
    │       ├── redirect.html
    │       ├── select-resource-type.html
    │       ├── tag-resources.html
    │       ├── tag-roles.html
    │       ├── type-to-tag-group.html
    │       ├── updated-config-rules.html
    │       ├── updated-service-catalog.html
    │       ├── updated-tags.html
    │       └── update-service-catalog.html
    ├── config
    │   ├── proxy_params
    │   ├── ssl-redirect.conf
    │   ├── tag-tamer.conf
    │   └── tagtamer.service
    ├── Flask-AWSCognito
    │   ├── docs
    │   │   ├── img
    │   │   │   ├── clientid.png
    │   │   │   ├── cognito_domain.png
    │   │   │   ├── flask-cognito.png
    │   │   │   └── poolid.png
    │   │   ├── make.bat
    │   │   ├── Makefile
    │   │   └── source
    │   │       ├── auth_code.rst
    │   │       ├── configure_aws.rst
    │   │       ├── configure_flask.rst
    │   │       ├── conf.py
    │   │       ├── index.rst
    │   │       └── installation.rst
    │   ├── flask_awscognito
    │   │   ├── constants.py
    │   │   ├── exceptions.py
    │   │   ├── __init__.py
    │   │   ├── plugin.py
    │   │   ├── services
    │   │   │   ├── cognito_service.py
    │   │   │   ├── __init__.py
    │   │   │   └── token_service.py
    │   │   └── utils.py
    │   ├── LICENSE
    │   ├── MANIFEST.in
    │   ├── README.md
    │   ├── requirements.txt
    │   ├── setup.py
    │   └── tests
    │       ├── conftest.py
    │       ├── __init__.py
    │       ├── test_cognito_service.py
    │       ├── test_plugin.py
    │       └── test_token_service.py
    └── tagtamer-install.sh

```

***
