from libs.object_view import ObjectView
import yaml
import yaml.scanner

# the C version is faster, but it doesn't always exist
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader  # type: ignore  # noqa: F401


def load_yaml_text(contents):
    result = None
    try:
        result = yaml.load(contents, Loader=SafeLoader)
    except (yaml.scanner.ScannerError, yaml.YAMLError) as e:
        raise str(e)

    return ObjectView(result)

def save_yaml_file(file_path, json):
    result = None
    try:
        yaml.add_representer(str, quoted_presenter)
        with open(file_path, 'w') as file:
            result = yaml.dump(
                data=json,
                stream=file,
                indent=2,
                default_flow_style=False
            )
    except (yaml.scanner.ScannerError, yaml.YAMLError) as e:
        raise str(e)
    return result
    

def quoted_presenter(dumper, data):
    """
    Dump style
    """
    # if "env_var" in data:
    #     return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='')