{
    'name': 'Inouk Tree',
    'category': 'Inouk',
    'description': """
Inouk Tree
==========

Advanced tree selector.
""",
    'version': '0.1',
    'depends': ['web'],
    'data': [
        # This is how we load ou javascript
        'views/jsloader.xml'
    ],
    'qweb': [
        'static/src/xml/*.xml'
    ],
    'installable': True,
    'auto_install': False
}
