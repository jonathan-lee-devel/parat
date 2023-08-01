import click


def verbose_option(func):
    """A decorator for the verbose command line argument"""
    return click.option('-v', '--verbose', type=click.BOOL, is_flag=True, required=False,
                        help='Increase output verbosity')(func)


def input_file_option(func):
    """A decorator for the input file command line argument"""
    return click.option('-if', '--input-file', type=click.STRING, is_flag=False, required=True,
                        help='Input file path')(func)


def release_specifier_option(func):
    """A decorator for the release specifier command line argument"""
    return click.option('-rs', '--release-specifier', type=click.STRING, is_flag=False, required=True,
                        help='Release specifier')(func)


def job_name_option(func):
    """A decorator for the job name command line argument"""
    return click.option('-jn', '--job-name', type=click.STRING, is_flag=False, required=True,
                        help='Job name')(func)


def build_number_option(func):
    """A decorator for the build number command line argument"""
    return click.option('-bn', '--build-number', type=click.INT, is_flag=False, required=True,
                        help='Build number')(func)


def url_end_option(func):
    """A decorator for the URL end command line argument"""
    return click.option('-ue', '--url-end', type=click.STRING, is_flag=False, required=True,
                        help='URL end')(func)


def trim_url_end_option_util(url_end_param: str) -> str:
    url_end_param = url_end_param.removeprefix('/')
    url_end_param = url_end_param.removesuffix('/')
    return url_end_param


def build_jobs_yaml_file_option(func):
    """A decorator for the build jobs YAML file"""
    return click.option('-bjy', '--build-jobs-yaml', type=click.STRING, is_flag=False, required=True,
                        help='Build jobs YAML file path')(func)
