default_app_config = 'project.apps.authorization.apps.AuthorizationConfig'


def path_to_image_profile(instance, filename: str) -> str:
    return f'users/profile-{instance.email}/profile_image{filename[filename.rfind("."):]}'
