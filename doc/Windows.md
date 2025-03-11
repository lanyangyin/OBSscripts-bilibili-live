# Windows10 或 Windows11
## 环境配置
- 下载安装Python3.10+
- 安装OBS
## 配置插件
- 打开OBS
- 在菜单栏的【工具】中，选择`脚本`
- 在脚本窗口中的`python设置`中配置python安装路径
- 使用以下代码获得python安装路径
```bash
python PYTHONPATH
```
- 例如
```
C:/Users/lanan/AppData/Local/Programs/Python/Python310
```
- Python310目录结构大致如下
```
├─DLLs
├─Doc
├─include
│  ├─cpython
│  └─internal
├─Lib
│  ├─asyncio
│  │  └─__pycache__
│  ├─collections
│  │  └─__pycache__
│  ├─concurrent
│  │  ├─futures
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─ctypes
│  │  ├─macholib
│  │  │  └─__pycache__
│  │  ├─test
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─curses
│  │  └─__pycache__
│  ├─dbm
│  │  └─__pycache__
│  ├─distutils
│  │  ├─command
│  │  │  └─__pycache__
│  │  ├─tests
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─email
│  │  ├─mime
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─encodings
│  │  └─__pycache__
│  ├─ensurepip
│  │  ├─_bundled
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─html
│  │  └─__pycache__
│  ├─http
│  │  └─__pycache__
│  ├─idlelib
│  │  ├─Icons
│  │  ├─idle_test
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─importlib
│  │  ├─metadata
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─json
│  │  └─__pycache__
│  ├─lib2to3
│  │  ├─fixes
│  │  │  └─__pycache__
│  │  ├─pgen2
│  │  │  └─__pycache__
│  │  ├─tests
│  │  │  ├─data
│  │  │  │  ├─fixers
│  │  │  │  │  ├─myfixes
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─logging
│  │  └─__pycache__
│  ├─msilib
│  │  └─__pycache__
│  ├─multiprocessing
│  │  ├─dummy
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─pydoc_data
│  │  └─__pycache__
│  ├─site-packages
│  │  ├─adodbapi
│  │  │  ├─examples
│  │  │  │  └─__pycache__
│  │  │  ├─test
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─argcomplete
│  │  │  ├─bash_completion.d
│  │  │  ├─packages
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─argcomplete-3.3.0.dist-info
│  │  ├─asttokens
│  │  │  └─__pycache__
│  │  ├─asttokens-2.4.1.dist-info
│  │  ├─attr
│  │  │  └─__pycache__
│  │  ├─attrs
│  │  │  └─__pycache__
│  │  ├─attrs-23.2.0.dist-info
│  │  │  └─licenses
│  │  ├─backcall
│  │  │  └─__pycache__
│  │  ├─backcall-0.2.0.dist-info
│  │  ├─beautifulsoup4-4.12.3.dist-info
│  │  │  └─licenses
│  │  ├─bleach
│  │  │  ├─_vendor
│  │  │  │  ├─html5lib
│  │  │  │  │  ├─filters
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─treeadapters
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─treebuilders
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─treewalkers
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─_trie
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─html5lib-1.1.dist-info
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─bleach-6.1.0.dist-info
│  │  ├─bs4
│  │  │  ├─builder
│  │  │  │  └─__pycache__
│  │  │  ├─tests
│  │  │  │  ├─fuzz
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─certifi
│  │  │  └─__pycache__
│  │  ├─certifi-2024.2.2.dist-info
│  │  ├─chardet
│  │  │  ├─cli
│  │  │  │  └─__pycache__
│  │  │  ├─metadata
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─chardet-4.0.0.dist-info
│  │  ├─charset_normalizer
│  │  │  ├─cli
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─charset_normalizer-3.3.2.dist-info
│  │  ├─click
│  │  │  └─__pycache__
│  │  ├─click-8.1.7.dist-info
│  │  ├─colorama
│  │  │  ├─tests
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─colorama-0.4.6.dist-info
│  │  │  └─licenses
│  │  ├─dateutil
│  │  │  ├─parser
│  │  │  │  └─__pycache__
│  │  │  ├─tz
│  │  │  │  └─__pycache__
│  │  │  ├─zoneinfo
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─decorator-5.1.1.dist-info
│  │  ├─defusedxml
│  │  │  └─__pycache__
│  │  ├─defusedxml-0.7.1.dist-info
│  │  ├─docopt-0.6.2.dist-info
│  │  ├─executing
│  │  │  └─__pycache__
│  │  ├─executing-2.0.1.dist-info
│  │  ├─fastjsonschema
│  │  │  └─__pycache__
│  │  ├─fastjsonschema-2.20.0.dist-info
│  │  ├─ffmpy-0.3.2.dist-info
│  │  ├─idna
│  │  │  └─__pycache__
│  │  ├─idna-2.10.dist-info
│  │  ├─IPython
│  │  │  ├─core
│  │  │  │  ├─magics
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─profile
│  │  │  │  ├─tests
│  │  │  │  │  ├─daft_extension
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─extensions
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─external
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─lib
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─sphinxext
│  │  │  │  └─__pycache__
│  │  │  ├─terminal
│  │  │  │  ├─pt_inputhooks
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─shortcuts
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─testing
│  │  │  │  ├─plugin
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─utils
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─ipython-8.12.3.dist-info
│  │  ├─isapi
│  │  │  ├─doc
│  │  │  ├─samples
│  │  │  │  └─__pycache__
│  │  │  ├─test
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─jedi
│  │  │  ├─api
│  │  │  │  ├─refactoring
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─inference
│  │  │  │  ├─compiled
│  │  │  │  │  ├─subprocess
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─gradual
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─value
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─plugins
│  │  │  │  └─__pycache__
│  │  │  ├─third_party
│  │  │  │  ├─django-stubs
│  │  │  │  │  └─django-stubs
│  │  │  │  │      ├─apps
│  │  │  │  │      ├─conf
│  │  │  │  │      │  ├─locale
│  │  │  │  │      │  └─urls
│  │  │  │  │      ├─contrib
│  │  │  │  │      │  ├─admin
│  │  │  │  │      │  │  ├─templatetags
│  │  │  │  │      │  │  └─views
│  │  │  │  │      │  ├─admindocs
│  │  │  │  │      │  ├─auth
│  │  │  │  │      │  │  ├─handlers
│  │  │  │  │      │  │  └─management
│  │  │  │  │      │  │      └─commands
│  │  │  │  │      │  ├─contenttypes
│  │  │  │  │      │  │  └─management
│  │  │  │  │      │  │      └─commands
│  │  │  │  │      │  ├─flatpages
│  │  │  │  │      │  │  └─templatetags
│  │  │  │  │      │  ├─gis
│  │  │  │  │      │  │  └─db
│  │  │  │  │      │  │      └─models
│  │  │  │  │      │  ├─humanize
│  │  │  │  │      │  │  └─templatetags
│  │  │  │  │      │  ├─messages
│  │  │  │  │      │  │  └─storage
│  │  │  │  │      │  ├─postgres
│  │  │  │  │      │  │  ├─aggregates
│  │  │  │  │      │  │  └─fields
│  │  │  │  │      │  ├─redirects
│  │  │  │  │      │  ├─sessions
│  │  │  │  │      │  │  ├─backends
│  │  │  │  │      │  │  └─management
│  │  │  │  │      │  │      └─commands
│  │  │  │  │      │  ├─sitemaps
│  │  │  │  │      │  │  └─management
│  │  │  │  │      │  │      └─commands
│  │  │  │  │      │  ├─sites
│  │  │  │  │      │  ├─staticfiles
│  │  │  │  │      │  │  ├─management
│  │  │  │  │      │  │  │  └─commands
│  │  │  │  │      │  │  └─templatetags
│  │  │  │  │      │  └─syndication
│  │  │  │  │      ├─core
│  │  │  │  │      │  ├─cache
│  │  │  │  │      │  │  └─backends
│  │  │  │  │      │  ├─checks
│  │  │  │  │      │  │  └─security
│  │  │  │  │      │  ├─files
│  │  │  │  │      │  ├─handlers
│  │  │  │  │      │  ├─mail
│  │  │  │  │      │  │  └─backends
│  │  │  │  │      │  ├─management
│  │  │  │  │      │  │  └─commands
│  │  │  │  │      │  ├─serializers
│  │  │  │  │      │  └─servers
│  │  │  │  │      ├─db
│  │  │  │  │      │  ├─backends
│  │  │  │  │      │  │  ├─base
│  │  │  │  │      │  │  ├─dummy
│  │  │  │  │      │  │  ├─mysql
│  │  │  │  │      │  │  ├─postgresql
│  │  │  │  │      │  │  └─sqlite3
│  │  │  │  │      │  ├─migrations
│  │  │  │  │      │  │  └─operations
│  │  │  │  │      │  └─models
│  │  │  │  │      │      ├─fields
│  │  │  │  │      │      ├─functions
│  │  │  │  │      │      └─sql
│  │  │  │  │      ├─dispatch
│  │  │  │  │      ├─forms
│  │  │  │  │      ├─http
│  │  │  │  │      ├─middleware
│  │  │  │  │      ├─template
│  │  │  │  │      │  ├─backends
│  │  │  │  │      │  └─loaders
│  │  │  │  │      ├─templatetags
│  │  │  │  │      ├─test
│  │  │  │  │      ├─urls
│  │  │  │  │      ├─utils
│  │  │  │  │      │  └─translation
│  │  │  │  │      └─views
│  │  │  │  │          ├─decorators
│  │  │  │  │          └─generic
│  │  │  │  └─typeshed
│  │  │  │      ├─stdlib
│  │  │  │      │  ├─2
│  │  │  │      │  │  ├─distutils
│  │  │  │      │  │  │  └─command
│  │  │  │      │  │  ├─email
│  │  │  │      │  │  │  └─mime
│  │  │  │      │  │  ├─encodings
│  │  │  │      │  │  ├─multiprocessing
│  │  │  │      │  │  │  └─dummy
│  │  │  │      │  │  └─os
│  │  │  │      │  ├─2and3
│  │  │  │      │  │  ├─ctypes
│  │  │  │      │  │  ├─curses
│  │  │  │      │  │  ├─ensurepip
│  │  │  │      │  │  ├─lib2to3
│  │  │  │      │  │  │  └─pgen2
│  │  │  │      │  │  ├─logging
│  │  │  │      │  │  ├─msilib
│  │  │  │      │  │  ├─pydoc_data
│  │  │  │      │  │  ├─pyexpat
│  │  │  │      │  │  ├─sqlite3
│  │  │  │      │  │  ├─wsgiref
│  │  │  │      │  │  ├─xml
│  │  │  │      │  │  │  ├─dom
│  │  │  │      │  │  │  ├─etree
│  │  │  │      │  │  │  ├─parsers
│  │  │  │      │  │  │  │  └─expat
│  │  │  │      │  │  │  └─sax
│  │  │  │      │  │  └─_typeshed
│  │  │  │      │  ├─3
│  │  │  │      │  │  ├─asyncio
│  │  │  │      │  │  ├─collections
│  │  │  │      │  │  ├─concurrent
│  │  │  │      │  │  │  └─futures
│  │  │  │      │  │  ├─dbm
│  │  │  │      │  │  ├─distutils
│  │  │  │      │  │  │  └─command
│  │  │  │      │  │  ├─email
│  │  │  │      │  │  │  └─mime
│  │  │  │      │  │  ├─encodings
│  │  │  │      │  │  ├─html
│  │  │  │      │  │  ├─http
│  │  │  │      │  │  ├─importlib
│  │  │  │      │  │  ├─json
│  │  │  │      │  │  ├─multiprocessing
│  │  │  │      │  │  │  └─dummy
│  │  │  │      │  │  ├─os
│  │  │  │      │  │  ├─tkinter
│  │  │  │      │  │  ├─unittest
│  │  │  │      │  │  ├─urllib
│  │  │  │      │  │  ├─venv
│  │  │  │      │  │  └─xmlrpc
│  │  │  │      │  ├─3.7
│  │  │  │      │  └─3.9
│  │  │  │      │      └─zoneinfo
│  │  │  │      └─third_party
│  │  │  │          ├─2
│  │  │  │          │  ├─concurrent
│  │  │  │          │  │  └─futures
│  │  │  │          │  ├─fb303
│  │  │  │          │  ├─kazoo
│  │  │  │          │  │  └─recipe
│  │  │  │          │  ├─OpenSSL
│  │  │  │          │  ├─routes
│  │  │  │          │  ├─scribe
│  │  │  │          │  ├─six
│  │  │  │          │  │  └─moves
│  │  │  │          │  │      └─urllib
│  │  │  │          │  └─tornado
│  │  │  │          ├─2and3
│  │  │  │          │  ├─atomicwrites
│  │  │  │          │  ├─attr
│  │  │  │          │  ├─backports
│  │  │  │          │  ├─bleach
│  │  │  │          │  ├─boto
│  │  │  │          │  │  ├─ec2
│  │  │  │          │  │  ├─elb
│  │  │  │          │  │  ├─kms
│  │  │  │          │  │  └─s3
│  │  │  │          │  ├─cachetools
│  │  │  │          │  ├─characteristic
│  │  │  │          │  ├─chardet
│  │  │  │          │  ├─click
│  │  │  │          │  ├─cryptography
│  │  │  │          │  │  ├─hazmat
│  │  │  │          │  │  │  ├─backends
│  │  │  │          │  │  │  ├─bindings
│  │  │  │          │  │  │  │  └─openssl
│  │  │  │          │  │  │  └─primitives
│  │  │  │          │  │  │      ├─asymmetric
│  │  │  │          │  │  │      ├─ciphers
│  │  │  │          │  │  │      ├─kdf
│  │  │  │          │  │  │      ├─serialization
│  │  │  │          │  │  │      └─twofactor
│  │  │  │          │  │  └─x509
│  │  │  │          │  ├─datetimerange
│  │  │  │          │  ├─dateutil
│  │  │  │          │  │  └─tz
│  │  │  │          │  ├─deprecated
│  │  │  │          │  ├─emoji
│  │  │  │          │  ├─flask
│  │  │  │          │  │  └─json
│  │  │  │          │  ├─geoip2
│  │  │  │          │  ├─google
│  │  │  │          │  │  └─protobuf
│  │  │  │          │  │      ├─compiler
│  │  │  │          │  │      ├─internal
│  │  │  │          │  │      └─util
│  │  │  │          │  ├─jinja2
│  │  │  │          │  ├─markdown
│  │  │  │          │  │  └─extensions
│  │  │  │          │  ├─markupsafe
│  │  │  │          │  ├─maxminddb
│  │  │  │          │  ├─nmap
│  │  │  │          │  ├─paramiko
│  │  │  │          │  ├─pymysql
│  │  │  │          │  │  └─constants
│  │  │  │          │  ├─pynamodb
│  │  │  │          │  │  └─connection
│  │  │  │          │  ├─pytz
│  │  │  │          │  ├─pyVmomi
│  │  │  │          │  │  ├─vim
│  │  │  │          │  │  └─vmodl
│  │  │  │          │  ├─redis
│  │  │  │          │  ├─requests
│  │  │  │          │  │  └─packages
│  │  │  │          │  │      └─urllib3
│  │  │  │          │  │          ├─contrib
│  │  │  │          │  │          ├─packages
│  │  │  │          │  │          │  └─ssl_match_hostname
│  │  │  │          │  │          └─util
│  │  │  │          │  ├─retry
│  │  │  │          │  ├─simplejson
│  │  │  │          │  ├─slugify
│  │  │  │          │  ├─tzlocal
│  │  │  │          │  ├─werkzeug
│  │  │  │          │  │  ├─contrib
│  │  │  │          │  │  ├─debug
│  │  │  │          │  │  └─middleware
│  │  │  │          │  └─yaml
│  │  │  │          └─3
│  │  │  │              ├─aiofiles
│  │  │  │              │  └─threadpool
│  │  │  │              ├─docutils
│  │  │  │              │  └─parsers
│  │  │  │              │      └─rst
│  │  │  │              ├─filelock
│  │  │  │              ├─freezegun
│  │  │  │              ├─jwt
│  │  │  │              │  └─contrib
│  │  │  │              │      └─algorithms
│  │  │  │              ├─pkg_resources
│  │  │  │              ├─pyrfc3339
│  │  │  │              ├─six
│  │  │  │              │  └─moves
│  │  │  │              │      └─urllib
│  │  │  │              ├─typed_ast
│  │  │  │              └─waitress
│  │  │  └─__pycache__
│  │  ├─jedi-0.19.1.dist-info
│  │  ├─jinja2
│  │  │  └─__pycache__
│  │  ├─jinja2-3.1.4.dist-info
│  │  ├─jsonschema
│  │  │  ├─benchmarks
│  │  │  │  ├─issue232
│  │  │  │  └─__pycache__
│  │  │  ├─tests
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─jsonschema-4.22.0.dist-info
│  │  │  └─licenses
│  │  ├─jsonschema_specifications
│  │  │  ├─schemas
│  │  │  │  ├─draft201909
│  │  │  │  │  └─vocabularies
│  │  │  │  ├─draft202012
│  │  │  │  │  └─vocabularies
│  │  │  │  ├─draft3
│  │  │  │  ├─draft4
│  │  │  │  ├─draft6
│  │  │  │  └─draft7
│  │  │  ├─tests
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─jsonschema_specifications-2023.12.1.dist-info
│  │  │  └─licenses
│  │  ├─jupyterlab_pygments
│  │  │  └─__pycache__
│  │  ├─jupyterlab_pygments-0.3.0.dist-info
│  │  │  └─licenses
│  │  ├─jupyter_client
│  │  │  ├─asynchronous
│  │  │  │  └─__pycache__
│  │  │  ├─blocking
│  │  │  │  └─__pycache__
│  │  │  ├─ioloop
│  │  │  │  └─__pycache__
│  │  │  ├─provisioning
│  │  │  │  └─__pycache__
│  │  │  ├─ssh
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─jupyter_client-8.6.2.dist-info
│  │  │  └─licenses
│  │  ├─jupyter_core
│  │  │  ├─utils
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─jupyter_core-5.7.2.dist-info
│  │  │  └─licenses
│  │  ├─markupsafe
│  │  │  └─__pycache__
│  │  ├─MarkupSafe-2.1.5.dist-info
│  │  ├─matplotlib_inline
│  │  │  └─__pycache__
│  │  ├─matplotlib_inline-0.1.7.dist-info
│  │  ├─mistune
│  │  │  ├─directives
│  │  │  │  └─__pycache__
│  │  │  ├─plugins
│  │  │  │  └─__pycache__
│  │  │  ├─renderers
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─mistune-3.0.2.dist-info
│  │  ├─nbclient
│  │  │  └─__pycache__
│  │  ├─nbclient-0.10.0.dist-info
│  │  │  └─licenses
│  │  ├─nbconvert
│  │  │  ├─exporters
│  │  │  │  └─__pycache__
│  │  │  ├─filters
│  │  │  │  └─__pycache__
│  │  │  ├─postprocessors
│  │  │  │  └─__pycache__
│  │  │  ├─preprocessors
│  │  │  │  └─__pycache__
│  │  │  ├─resources
│  │  │  │  └─__pycache__
│  │  │  ├─templates
│  │  │  │  └─skeleton
│  │  │  ├─utils
│  │  │  │  └─__pycache__
│  │  │  ├─writers
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─nbconvert-7.16.4.dist-info
│  │  │  └─licenses
│  │  ├─nbformat
│  │  │  ├─corpus
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─v1
│  │  │  │  └─__pycache__
│  │  │  ├─v2
│  │  │  │  └─__pycache__
│  │  │  ├─v3
│  │  │  │  └─__pycache__
│  │  │  ├─v4
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─nbformat-5.10.4.dist-info
│  │  │  └─licenses
│  │  ├─numpy
│  │  │  ├─char
│  │  │  │  └─__pycache__
│  │  │  ├─compat
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─core
│  │  │  │  └─__pycache__
│  │  │  ├─distutils
│  │  │  │  ├─checks
│  │  │  │  ├─command
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─fcompiler
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─mingw
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─doc
│  │  │  │  └─__pycache__
│  │  │  ├─f2py
│  │  │  │  ├─src
│  │  │  │  ├─tests
│  │  │  │  │  ├─src
│  │  │  │  │  │  ├─abstract_interface
│  │  │  │  │  │  ├─array_from_pyobj
│  │  │  │  │  │  ├─assumed_shape
│  │  │  │  │  │  ├─block_docstring
│  │  │  │  │  │  ├─callback
│  │  │  │  │  │  ├─cli
│  │  │  │  │  │  ├─common
│  │  │  │  │  │  ├─crackfortran
│  │  │  │  │  │  ├─f2cmap
│  │  │  │  │  │  ├─isocintrin
│  │  │  │  │  │  ├─kind
│  │  │  │  │  │  ├─mixed
│  │  │  │  │  │  ├─modules
│  │  │  │  │  │  │  └─gh25337
│  │  │  │  │  │  ├─negative_bounds
│  │  │  │  │  │  ├─parameter
│  │  │  │  │  │  ├─quoted_character
│  │  │  │  │  │  ├─regression
│  │  │  │  │  │  ├─return_character
│  │  │  │  │  │  ├─return_complex
│  │  │  │  │  │  ├─return_integer
│  │  │  │  │  │  ├─return_logical
│  │  │  │  │  │  ├─return_real
│  │  │  │  │  │  ├─size
│  │  │  │  │  │  ├─string
│  │  │  │  │  │  └─value_attrspec
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─_backends
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─fft
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─lib
│  │  │  │  ├─tests
│  │  │  │  │  ├─data
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─linalg
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─ma
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─matrixlib
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─polynomial
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─random
│  │  │  │  ├─lib
│  │  │  │  ├─tests
│  │  │  │  │  ├─data
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─_examples
│  │  │  │  │  ├─cffi
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─cython
│  │  │  │  │  └─numba
│  │  │  │  │      └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─rec
│  │  │  │  └─__pycache__
│  │  │  ├─strings
│  │  │  │  └─__pycache__
│  │  │  ├─testing
│  │  │  │  ├─tests
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─_private
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─tests
│  │  │  │  └─__pycache__
│  │  │  ├─typing
│  │  │  │  ├─tests
│  │  │  │  │  ├─data
│  │  │  │  │  │  ├─fail
│  │  │  │  │  │  ├─misc
│  │  │  │  │  │  ├─pass
│  │  │  │  │  │  │  └─__pycache__
│  │  │  │  │  │  └─reveal
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─_core
│  │  │  │  ├─include
│  │  │  │  │  └─numpy
│  │  │  │  │      └─random
│  │  │  │  ├─lib
│  │  │  │  │  ├─npy-pkg-config
│  │  │  │  │  └─pkgconfig
│  │  │  │  ├─tests
│  │  │  │  │  ├─data
│  │  │  │  │  ├─examples
│  │  │  │  │  │  ├─cython
│  │  │  │  │  │  │  └─__pycache__
│  │  │  │  │  │  └─limited_api
│  │  │  │  │  │      └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─_pyinstaller
│  │  │  │  └─__pycache__
│  │  │  ├─_typing
│  │  │  │  └─__pycache__
│  │  │  ├─_utils
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─numpy-2.0.0.dist-info
│  │  ├─numpy.libs
│  │  ├─packaging
│  │  │  └─__pycache__
│  │  ├─packaging-24.0.dist-info
│  │  ├─pandas
│  │  │  ├─api
│  │  │  │  ├─extensions
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─indexers
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─interchange
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─types
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─typing
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─arrays
│  │  │  │  └─__pycache__
│  │  │  ├─compat
│  │  │  │  ├─numpy
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─core
│  │  │  │  ├─arrays
│  │  │  │  │  ├─arrow
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─sparse
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─array_algos
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─computation
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─dtypes
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─groupby
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─indexers
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─indexes
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─interchange
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─internals
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─methods
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─ops
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─reshape
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─sparse
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─strings
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─tools
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─util
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─window
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─_numba
│  │  │  │  │  ├─kernels
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─errors
│  │  │  │  └─__pycache__
│  │  │  ├─io
│  │  │  │  ├─clipboard
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─excel
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─formats
│  │  │  │  │  ├─templates
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─json
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─parsers
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─sas
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─plotting
│  │  │  │  ├─_matplotlib
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─tests
│  │  │  │  ├─api
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─apply
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─arithmetic
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─arrays
│  │  │  │  │  ├─boolean
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─categorical
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─datetimes
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─floating
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─integer
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─interval
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─masked
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─numpy_
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─period
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─sparse
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─string_
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─timedeltas
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─base
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─computation
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─config
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─construction
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─copy_view
│  │  │  │  │  ├─index
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─dtypes
│  │  │  │  │  ├─cast
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─extension
│  │  │  │  │  ├─array_with_attr
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─base
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─date
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─decimal
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─json
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─list
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─frame
│  │  │  │  │  ├─constructors
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─indexing
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─methods
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─generic
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─groupby
│  │  │  │  │  ├─aggregate
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─methods
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─transform
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─indexes
│  │  │  │  │  ├─base_class
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─categorical
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─datetimelike_
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─datetimes
│  │  │  │  │  │  ├─methods
│  │  │  │  │  │  │  └─__pycache__
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─interval
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─multi
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─numeric
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─object
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─period
│  │  │  │  │  │  ├─methods
│  │  │  │  │  │  │  └─__pycache__
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─ranges
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─timedeltas
│  │  │  │  │  │  ├─methods
│  │  │  │  │  │  │  └─__pycache__
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─indexing
│  │  │  │  │  ├─interval
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─multiindex
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─interchange
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─internals
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─io
│  │  │  │  │  ├─excel
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─formats
│  │  │  │  │  │  ├─style
│  │  │  │  │  │  │  └─__pycache__
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─json
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─parser
│  │  │  │  │  │  ├─common
│  │  │  │  │  │  │  └─__pycache__
│  │  │  │  │  │  ├─dtypes
│  │  │  │  │  │  │  └─__pycache__
│  │  │  │  │  │  ├─usecols
│  │  │  │  │  │  │  └─__pycache__
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─pytables
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─sas
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─xml
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─libs
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─plotting
│  │  │  │  │  ├─frame
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─reductions
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─resample
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─reshape
│  │  │  │  │  ├─concat
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─merge
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─scalar
│  │  │  │  │  ├─interval
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─period
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─timedelta
│  │  │  │  │  │  ├─methods
│  │  │  │  │  │  │  └─__pycache__
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─timestamp
│  │  │  │  │  │  ├─methods
│  │  │  │  │  │  │  └─__pycache__
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─series
│  │  │  │  │  ├─accessors
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─indexing
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─methods
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─strings
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─tools
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─tseries
│  │  │  │  │  ├─frequencies
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─holiday
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─offsets
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─tslibs
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─util
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─window
│  │  │  │  │  ├─moments
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─tseries
│  │  │  │  └─__pycache__
│  │  │  ├─util
│  │  │  │  ├─version
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─_config
│  │  │  │  └─__pycache__
│  │  │  ├─_libs
│  │  │  │  ├─tslibs
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─window
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─_testing
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─pandas-2.2.2.dist-info
│  │  ├─pandas.libs
│  │  ├─pandocfilters-1.5.1.dist-info
│  │  ├─parso
│  │  │  ├─pgen2
│  │  │  │  └─__pycache__
│  │  │  ├─python
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─parso-0.8.4.dist-info
│  │  ├─pickleshare-0.7.5.dist-info
│  │  ├─PIL
│  │  │  └─__pycache__
│  │  ├─pillow-10.3.0.dist-info
│  │  ├─pip
│  │  │  ├─_internal
│  │  │  │  ├─cli
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─commands
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─distributions
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─index
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─locations
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─metadata
│  │  │  │  │  ├─importlib
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─models
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─network
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─operations
│  │  │  │  │  ├─build
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─install
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─req
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─resolution
│  │  │  │  │  ├─legacy
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─resolvelib
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─utils
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─vcs
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─_vendor
│  │  │  │  ├─cachecontrol
│  │  │  │  │  ├─caches
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─certifi
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─distlib
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─distro
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─idna
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─msgpack
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─packaging
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─pkg_resources
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─platformdirs
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─pygments
│  │  │  │  │  ├─filters
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─formatters
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─lexers
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─styles
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─pyproject_hooks
│  │  │  │  │  ├─_in_process
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─requests
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─resolvelib
│  │  │  │  │  ├─compat
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─rich
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─tenacity
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─tomli
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─truststore
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─urllib3
│  │  │  │  │  ├─contrib
│  │  │  │  │  │  ├─_securetransport
│  │  │  │  │  │  │  └─__pycache__
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─packages
│  │  │  │  │  │  ├─backports
│  │  │  │  │  │  │  └─__pycache__
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─util
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─pip-24.1.1.dist-info
│  │  ├─pipreqs
│  │  │  └─__pycache__
│  │  ├─pipreqs-0.5.0.dist-info
│  │  ├─pipx
│  │  │  ├─commands
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─pipx-1.5.0.dist-info
│  │  │  └─licenses
│  │  ├─pkg_resources
│  │  │  ├─extern
│  │  │  │  └─__pycache__
│  │  │  ├─_vendor
│  │  │  │  ├─importlib_resources
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─jaraco
│  │  │  │  │  ├─text
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─more_itertools
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─packaging
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─pyparsing
│  │  │  │  │  ├─diagram
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─platformdirs
│  │  │  └─__pycache__
│  │  ├─platformdirs-4.2.0.dist-info
│  │  │  └─licenses
│  │  ├─prompt_toolkit
│  │  │  ├─application
│  │  │  │  └─__pycache__
│  │  │  ├─clipboard
│  │  │  │  └─__pycache__
│  │  │  ├─completion
│  │  │  │  └─__pycache__
│  │  │  ├─contrib
│  │  │  │  ├─completers
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─regular_languages
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─ssh
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─telnet
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─eventloop
│  │  │  │  └─__pycache__
│  │  │  ├─filters
│  │  │  │  └─__pycache__
│  │  │  ├─formatted_text
│  │  │  │  └─__pycache__
│  │  │  ├─input
│  │  │  │  └─__pycache__
│  │  │  ├─key_binding
│  │  │  │  ├─bindings
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─layout
│  │  │  │  └─__pycache__
│  │  │  ├─lexers
│  │  │  │  └─__pycache__
│  │  │  ├─output
│  │  │  │  └─__pycache__
│  │  │  ├─shortcuts
│  │  │  │  ├─progress_bar
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─styles
│  │  │  │  └─__pycache__
│  │  │  ├─widgets
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─prompt_toolkit-3.0.47.dist-info
│  │  ├─pure_eval
│  │  │  └─__pycache__
│  │  ├─pure_eval-0.2.2.dist-info
│  │  ├─pygments
│  │  │  ├─filters
│  │  │  │  └─__pycache__
│  │  │  ├─formatters
│  │  │  │  └─__pycache__
│  │  │  ├─lexers
│  │  │  │  └─__pycache__
│  │  │  ├─styles
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─pygments-2.18.0.dist-info
│  │  │  └─licenses
│  │  ├─pyperclip
│  │  │  └─__pycache__
│  │  ├─pyperclip-1.9.0.dist-info
│  │  ├─pypinyin
│  │  │  ├─contrib
│  │  │  │  └─__pycache__
│  │  │  ├─seg
│  │  │  │  └─__pycache__
│  │  │  ├─style
│  │  │  │  └─__pycache__
│  │  │  ├─tools
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─pypinyin-0.51.0.dist-info
│  │  ├─pypng-0.20220715.0.dist-info
│  │  ├─pythonwin
│  │  │  └─pywin
│  │  │      ├─debugger
│  │  │      │  └─__pycache__
│  │  │      ├─Demos
│  │  │      │  ├─app
│  │  │      │  │  └─__pycache__
│  │  │      │  ├─ocx
│  │  │      │  │  └─__pycache__
│  │  │      │  └─__pycache__
│  │  │      ├─dialogs
│  │  │      │  └─__pycache__
│  │  │      ├─docking
│  │  │      │  └─__pycache__
│  │  │      ├─framework
│  │  │      │  ├─editor
│  │  │      │  │  ├─color
│  │  │      │  │  │  └─__pycache__
│  │  │      │  │  └─__pycache__
│  │  │      │  └─__pycache__
│  │  │      ├─idle
│  │  │      │  └─__pycache__
│  │  │      ├─mfc
│  │  │      │  └─__pycache__
│  │  │      ├─scintilla
│  │  │      │  └─__pycache__
│  │  │      ├─tools
│  │  │      │  └─__pycache__
│  │  │      └─__pycache__
│  │  ├─python_dateutil-2.9.0.post0.dist-info
│  │  ├─pytz
│  │  │  ├─zoneinfo
│  │  │  │  ├─Africa
│  │  │  │  ├─America
│  │  │  │  │  ├─Argentina
│  │  │  │  │  ├─Indiana
│  │  │  │  │  ├─Kentucky
│  │  │  │  │  └─North_Dakota
│  │  │  │  ├─Antarctica
│  │  │  │  ├─Arctic
│  │  │  │  ├─Asia
│  │  │  │  ├─Atlantic
│  │  │  │  ├─Australia
│  │  │  │  ├─Brazil
│  │  │  │  ├─Canada
│  │  │  │  ├─Chile
│  │  │  │  ├─Etc
│  │  │  │  ├─Europe
│  │  │  │  ├─Indian
│  │  │  │  ├─Mexico
│  │  │  │  ├─Pacific
│  │  │  │  └─US
│  │  │  └─__pycache__
│  │  ├─pytz-2024.1.dist-info
│  │  ├─pywin32-306.dist-info
│  │  ├─pywin32_system32
│  │  ├─pyzbar
│  │  │  ├─scripts
│  │  │  │  └─__pycache__
│  │  │  ├─tests
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─pyzbar-0.1.9.dist-info
│  │  ├─pyzmq-26.0.3.dist-info
│  │  │  └─licenses
│  │  │      └─licenses
│  │  ├─pyzmq.libs
│  │  ├─qrcode
│  │  │  ├─compat
│  │  │  │  └─__pycache__
│  │  │  ├─image
│  │  │  │  ├─styles
│  │  │  │  │  ├─moduledrawers
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─tests
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─qrcode-7.4.2.dist-info
│  │  ├─referencing
│  │  │  ├─tests
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─referencing-0.35.1.dist-info
│  │  │  └─licenses
│  │  ├─requests
│  │  │  └─__pycache__
│  │  ├─requests-2.32.3.dist-info
│  │  ├─rpds
│  │  │  └─__pycache__
│  │  ├─rpds_py-0.18.1.dist-info
│  │  │  └─license_files
│  │  ├─setuptools
│  │  │  ├─command
│  │  │  │  └─__pycache__
│  │  │  ├─config
│  │  │  │  ├─_validate_pyproject
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─extern
│  │  │  │  └─__pycache__
│  │  │  ├─_distutils
│  │  │  │  ├─command
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─_vendor
│  │  │  │  ├─importlib_metadata
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─importlib_resources
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─jaraco
│  │  │  │  │  ├─text
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─more_itertools
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─packaging
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─pyparsing
│  │  │  │  │  ├─diagram
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─tomli
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─setuptools-65.5.0.dist-info
│  │  ├─six-1.16.0.dist-info
│  │  ├─soupsieve
│  │  │  └─__pycache__
│  │  ├─soupsieve-2.5.dist-info
│  │  │  └─licenses
│  │  ├─stack_data
│  │  │  └─__pycache__
│  │  ├─stack_data-0.6.3.dist-info
│  │  ├─tests
│  │  │  └─__pycache__
│  │  ├─tinycss2
│  │  │  └─__pycache__
│  │  ├─tinycss2-1.3.0.dist-info
│  │  ├─tomli
│  │  │  └─__pycache__
│  │  ├─tomli-2.0.1.dist-info
│  │  ├─tornado
│  │  │  ├─platform
│  │  │  │  └─__pycache__
│  │  │  ├─test
│  │  │  │  ├─csv_translations
│  │  │  │  ├─gettext_translations
│  │  │  │  │  └─fr_FR
│  │  │  │  │      └─LC_MESSAGES
│  │  │  │  ├─static
│  │  │  │  │  └─dir
│  │  │  │  ├─templates
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─tornado-6.4.1.dist-info
│  │  ├─traitlets
│  │  │  ├─config
│  │  │  │  └─__pycache__
│  │  │  ├─tests
│  │  │  │  └─__pycache__
│  │  │  ├─utils
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─traitlets-5.14.3.dist-info
│  │  │  └─licenses
│  │  ├─typing_extensions-4.11.0.dist-info
│  │  ├─tzdata
│  │  │  ├─zoneinfo
│  │  │  │  ├─Africa
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─America
│  │  │  │  │  ├─Argentina
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─Indiana
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─Kentucky
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  ├─North_Dakota
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Antarctica
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Arctic
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Asia
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Atlantic
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Australia
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Brazil
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Canada
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Chile
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Etc
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Europe
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Indian
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Mexico
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Pacific
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─US
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─tzdata-2024.1.dist-info
│  │  ├─urllib3
│  │  │  ├─contrib
│  │  │  │  ├─_securetransport
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─packages
│  │  │  │  ├─backports
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─util
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─urllib3-1.26.18.dist-info
│  │  ├─userpath
│  │  │  └─__pycache__
│  │  ├─userpath-1.9.2.dist-info
│  │  │  └─licenses
│  │  ├─wcwidth
│  │  │  └─__pycache__
│  │  ├─wcwidth-0.2.13.dist-info
│  │  ├─webencodings
│  │  │  └─__pycache__
│  │  ├─webencodings-0.5.1.dist-info
│  │  ├─websocket
│  │  │  ├─tests
│  │  │  │  ├─data
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─websockets
│  │  │  ├─extensions
│  │  │  │  └─__pycache__
│  │  │  ├─legacy
│  │  │  │  └─__pycache__
│  │  │  ├─sync
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─websockets-12.0.dist-info
│  │  ├─websocket_client-1.8.0.dist-info
│  │  ├─win32
│  │  │  ├─Demos
│  │  │  │  ├─c_extension
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─dde
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─images
│  │  │  │  ├─pipes
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─security
│  │  │  │  │  ├─sspi
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─service
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─win32wnet
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─include
│  │  │  ├─lib
│  │  │  │  └─__pycache__
│  │  │  ├─libs
│  │  │  ├─scripts
│  │  │  │  ├─ce
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─VersionStamp
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  └─test
│  │  │      ├─win32rcparser
│  │  │      └─__pycache__
│  │  ├─win32com
│  │  │  ├─client
│  │  │  │  └─__pycache__
│  │  │  ├─demos
│  │  │  │  └─__pycache__
│  │  │  ├─HTML
│  │  │  │  └─image
│  │  │  ├─include
│  │  │  ├─libs
│  │  │  ├─makegw
│  │  │  │  └─__pycache__
│  │  │  ├─server
│  │  │  │  └─__pycache__
│  │  │  ├─servers
│  │  │  │  └─__pycache__
│  │  │  ├─test
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─win32comext
│  │  │  ├─adsi
│  │  │  │  ├─demos
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─authorization
│  │  │  │  ├─demos
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─axcontrol
│  │  │  │  └─__pycache__
│  │  │  ├─axdebug
│  │  │  │  └─__pycache__
│  │  │  ├─axscript
│  │  │  │  ├─client
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─Demos
│  │  │  │  │  └─client
│  │  │  │  │      ├─asp
│  │  │  │  │      │  └─interrupt
│  │  │  │  │      ├─ie
│  │  │  │  │      └─wsh
│  │  │  │  ├─server
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─test
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─bits
│  │  │  │  ├─test
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─directsound
│  │  │  │  ├─test
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─ifilter
│  │  │  │  ├─demo
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─internet
│  │  │  │  └─__pycache__
│  │  │  ├─mapi
│  │  │  │  ├─demos
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─propsys
│  │  │  │  ├─test
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─shell
│  │  │  │  ├─demos
│  │  │  │  │  ├─servers
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─test
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  └─taskscheduler
│  │  │      ├─test
│  │  │      │  └─__pycache__
│  │  │      └─__pycache__
│  │  ├─yarg
│  │  │  └─__pycache__
│  │  ├─yarg-0.1.9.dist-info
│  │  ├─zmq
│  │  │  ├─auth
│  │  │  │  └─__pycache__
│  │  │  ├─backend
│  │  │  │  ├─cffi
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─cython
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─devices
│  │  │  │  └─__pycache__
│  │  │  ├─eventloop
│  │  │  │  └─__pycache__
│  │  │  ├─green
│  │  │  │  ├─eventloop
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─log
│  │  │  │  └─__pycache__
│  │  │  ├─ssh
│  │  │  │  └─__pycache__
│  │  │  ├─sugar
│  │  │  │  └─__pycache__
│  │  │  ├─tests
│  │  │  │  └─__pycache__
│  │  │  ├─utils
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─_distutils_hack
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─sqlite3
│  │  ├─test
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─test
│  │  ├─audiodata
│  │  ├─capath
│  │  ├─cjkencodings
│  │  ├─crashers
│  │  │  └─__pycache__
│  │  ├─data
│  │  ├─decimaltestdata
│  │  ├─dtracedata
│  │  │  └─__pycache__
│  │  ├─encoded_modules
│  │  │  └─__pycache__
│  │  ├─imghdrdata
│  │  ├─leakers
│  │  │  └─__pycache__
│  │  ├─libregrtest
│  │  │  └─__pycache__
│  │  ├─sndhdrdata
│  │  ├─subprocessdata
│  │  │  └─__pycache__
│  │  ├─support
│  │  │  └─__pycache__
│  │  ├─test_asyncio
│  │  │  └─__pycache__
│  │  ├─test_capi
│  │  │  └─__pycache__
│  │  ├─test_email
│  │  │  ├─data
│  │  │  └─__pycache__
│  │  ├─test_import
│  │  │  ├─data
│  │  │  │  ├─circular_imports
│  │  │  │  │  ├─subpkg
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─package
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─package2
│  │  │  │  │  └─__pycache__
│  │  │  │  └─unwritable
│  │  │  │      └─__pycache__
│  │  │  └─__pycache__
│  │  ├─test_importlib
│  │  │  ├─builtin
│  │  │  │  └─__pycache__
│  │  │  ├─data
│  │  │  │  └─__pycache__
│  │  │  ├─data01
│  │  │  │  ├─subdirectory
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─data02
│  │  │  │  ├─one
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─two
│  │  │  │  │  └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─data03
│  │  │  │  ├─namespace
│  │  │  │  │  ├─portion1
│  │  │  │  │  │  └─__pycache__
│  │  │  │  │  └─portion2
│  │  │  │  │      └─__pycache__
│  │  │  │  └─__pycache__
│  │  │  ├─extension
│  │  │  │  └─__pycache__
│  │  │  ├─frozen
│  │  │  │  └─__pycache__
│  │  │  ├─import_
│  │  │  │  └─__pycache__
│  │  │  ├─namespacedata01
│  │  │  ├─namespace_pkgs
│  │  │  │  ├─both_portions
│  │  │  │  │  └─foo
│  │  │  │  │      └─__pycache__
│  │  │  │  ├─module_and_namespace_package
│  │  │  │  │  ├─a_test
│  │  │  │  │  └─__pycache__
│  │  │  │  ├─not_a_namespace_pkg
│  │  │  │  │  └─foo
│  │  │  │  │      └─__pycache__
│  │  │  │  ├─portion1
│  │  │  │  │  └─foo
│  │  │  │  │      └─__pycache__
│  │  │  │  ├─portion2
│  │  │  │  │  └─foo
│  │  │  │  │      └─__pycache__
│  │  │  │  ├─project1
│  │  │  │  │  └─parent
│  │  │  │  │      └─child
│  │  │  │  │          └─__pycache__
│  │  │  │  ├─project2
│  │  │  │  │  └─parent
│  │  │  │  │      └─child
│  │  │  │  │          └─__pycache__
│  │  │  │  └─project3
│  │  │  │      └─parent
│  │  │  │          └─child
│  │  │  │              └─__pycache__
│  │  │  ├─partial
│  │  │  │  └─__pycache__
│  │  │  ├─source
│  │  │  │  └─__pycache__
│  │  │  ├─zipdata01
│  │  │  │  └─__pycache__
│  │  │  ├─zipdata02
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─test_json
│  │  │  └─__pycache__
│  │  ├─test_peg_generator
│  │  │  └─__pycache__
│  │  ├─test_tools
│  │  │  └─__pycache__
│  │  ├─test_warnings
│  │  │  ├─data
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─test_zoneinfo
│  │  │  ├─data
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  ├─tracedmodules
│  │  │  └─__pycache__
│  │  ├─typinganndata
│  │  │  └─__pycache__
│  │  ├─xmltestdata
│  │  │  └─c14n-20
│  │  ├─ziptestdata
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─tkinter
│  │  ├─test
│  │  │  ├─test_tkinter
│  │  │  │  └─__pycache__
│  │  │  ├─test_ttk
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─turtledemo
│  │  └─__pycache__
│  ├─unittest
│  │  ├─test
│  │  │  ├─testmock
│  │  │  │  └─__pycache__
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─urllib
│  │  └─__pycache__
│  ├─venv
│  │  ├─scripts
│  │  │  ├─common
│  │  │  ├─nt
│  │  │  └─posix
│  │  └─__pycache__
│  ├─wsgiref
│  │  └─__pycache__
│  ├─xml
│  │  ├─dom
│  │  │  └─__pycache__
│  │  ├─etree
│  │  │  └─__pycache__
│  │  ├─parsers
│  │  │  └─__pycache__
│  │  ├─sax
│  │  │  └─__pycache__
│  │  └─__pycache__
│  ├─xmlrpc
│  │  └─__pycache__
│  ├─zoneinfo
│  │  └─__pycache__
│  └─__pycache__
├─libs
├─Scripts
│  └─__pycache__
├─share
│  ├─jupyter
│  │  ├─labextensions
│  │  │  └─jupyterlab_pygments
│  │  │      └─static
│  │  └─nbconvert
│  │      └─templates
│  │          ├─asciidoc
│  │          ├─base
│  │          ├─basic
│  │          ├─classic
│  │          │  └─static
│  │          ├─compatibility
│  │          ├─lab
│  │          │  └─static
│  │          ├─latex
│  │          ├─markdown
│  │          ├─python
│  │          ├─reveal
│  │          │  └─static
│  │          ├─rst
│  │          ├─script
│  │          └─webpdf
│  └─man
│      └─man1
├─tcl
│  ├─dde1.4
│  ├─nmake
│  ├─reg1.3
│  ├─tcl8
│  │  ├─8.4
│  │  │  └─platform
│  │  ├─8.5
│  │  └─8.6
│  ├─tcl8.6
│  │  ├─encoding
│  │  ├─http1.0
│  │  ├─msgs
│  │  ├─opt0.4
│  │  └─tzdata
│  │      ├─Africa
│  │      ├─America
│  │      │  ├─Argentina
│  │      │  ├─Indiana
│  │      │  ├─Kentucky
│  │      │  └─North_Dakota
│  │      ├─Antarctica
│  │      ├─Arctic
│  │      ├─Asia
│  │      ├─Atlantic
│  │      ├─Australia
│  │      ├─Brazil
│  │      ├─Canada
│  │      ├─Chile
│  │      ├─Etc
│  │      ├─Europe
│  │      ├─Indian
│  │      ├─Mexico
│  │      ├─Pacific
│  │      ├─SystemV
│  │      └─US
│  ├─tix8.4.3
│  │  ├─bitmaps
│  │  ├─demos
│  │  │  ├─bitmaps
│  │  │  └─samples
│  │  └─pref
│  │      └─__pycache__
│  └─tk8.6
│      ├─demos
│      │  └─images
│      ├─images
│      ├─msgs
│      └─ttk
└─Tools
    ├─demo
    │  └─__pycache__
    ├─i18n
    │  └─__pycache__
    ├─pynche
    │  ├─X
    │  └─__pycache__
    └─scripts
        └─__pycache__
```
![img_2.png](img_2.png)
- 在脚本窗口中的`脚本`中添加脚本`bilibili-live.py`
![img.png](img.png)
![img_1.png](img_1.png)
