from rest_framework.versioning import URLPathVersioning

class DefaultVersion(URLPathVersioning):
    version_param = ["v1"]