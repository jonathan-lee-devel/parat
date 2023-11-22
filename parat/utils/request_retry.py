"""
This module allows a user to attempt to make a request multiple times if the target host is
temporarily down
"""

import logging
import time
import requests
import urllib3

from parat.enums.http_request_methods import HttpRequestMethod
from parat.exceptions.request_retry_exception import RequestRetryException
from parat.utils.http_request_settings import HttpRequestSettings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def request_retry_download_file(
        url: str,
        max_retry: int,
        request_settings: HttpRequestSettings,
        output_file_path: str):
    """
    Function which utilizes local request retry function to download file at specified URL
    :param url: of the file to download
    :param max_retry: Amount of times to retry the request
    :param request_settings: Settings for the request namely body, proxy, and SSL
    :param output_file_path: File path for the response body to be written to
    :return:
    """
    response = request_retry(HttpRequestMethod.GET, url, max_retry, request_settings)
    logging.info(f'Writing response data to {output_file_path}')
    with open(output_file_path, 'w') as output_file:
        output_file.write(response.text)


def request_retry(
        request_method: HttpRequestMethod,
        url: str,
        max_retry: int,
        request_settings: HttpRequestSettings):
    """
    Function to retry requests if the target host is not found. Geometric retry is used here.
    :param request_method: Which REST request is being conducted
    :param url: URL you want to run your request against
    :param max_retry: Amount of times to retry the request
    :param request_settings: Settings for the request namely body, proxy, and SSL
    :return: response
    :rtype: requests.Response
    """
    count = 0
    response = None
    valid_response_codes = [requests.codes.ok, requests.codes.created, requests.codes.no_content]
    logging.debug(f'type_of_request: {request_method.name}')
    logging.debug(f'url: {str(url)}')
    while count < max_retry:
        try:
            response = make_request_based_on_input(request_method, url, request_settings)
            if response and response.status_code in valid_response_codes:
                break
            raise requests.exceptions.RequestException
        except requests.exceptions.RequestException:
            logging.debug(f'Could not make the {request_method.name} request')
            if response is not None:
                logging.debug(f'Response status code: {str(response.status_code)}')
                logging.debug(f'Response reason: {str(response.reason)}')
                logging.debug(f'Response output: {str(response.text)}')

                if response.status_code == requests.codes.bad_request:
                    raise RequestRetryException('Bad request detected') from requests.exceptions.RequestException
        count += 1
        if count == max_retry:
            raise RequestRetryException(f'Failed to execute {request_method.name} request after {max_retry} tries')

        sleep_time = 2 ** count
        logging.warning(f'Failed to make {request_method.name} request. '
                        f'Sleeping and then trying again in {sleep_time} seconds')
        time.sleep(sleep_time)
    return response


def make_request_based_on_input(request_method: HttpRequestMethod, url: str, request_settings: HttpRequestSettings):
    """
    Makes a request based on the request type passed in
    :param request_method: Which REST request is being conducted
    :param url: URL you want to run your request against
    :param request_settings: Settings for the request namely body, proxy, and SSL
    :return: response
    :rtype: requests.Response
    """
    logging.debug(f'Trying to make {request_method.name} request')
    response = None
    try:
        if request_method == HttpRequestMethod.GET:
            logging.debug(f'Doing a {request_method.name} request')
            response = requests.get(url, proxies=request_settings.proxy, timeout=10, verify=request_settings.ssl,
                                    auth=request_settings.auth)
        elif request_method == HttpRequestMethod.PATCH:
            logging.debug(f'Doing a {request_method.name} request')
            response = requests.patch(url, json=request_settings.body, timeout=20, proxies=request_settings.proxy,
                                      verify=request_settings.ssl, auth=request_settings.auth)
        elif request_method == HttpRequestMethod.PUT:
            logging.debug(f'Doing a {request_method.name} request')
            response = requests.put(url, json=request_settings.body, timeout=5, proxies=request_settings.proxy,
                                    verify=request_settings.ssl, auth=request_settings.auth)
        elif request_method == HttpRequestMethod.POST:
            logging.debug(f'Doing a {request_method.name} request')
            response = requests.post(url, json=request_settings.body, timeout=20, proxies=request_settings.proxy,
                                     verify=request_settings.ssl, auth=request_settings.auth)
        elif request_method == HttpRequestMethod.DELETE:
            logging.debug(f'Doing a {request_method.name} request')
            response = requests.delete(url, timeout=10, proxies=request_settings.proxy, verify=request_settings.ssl)
    except (requests.exceptions.ProxyError, AssertionError):
        logging.error(f'Could not make {request_method.name} request due to a Proxy Error')
    return response
