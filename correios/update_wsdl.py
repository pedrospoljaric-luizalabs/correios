import logging
import os

import requests

logger = logging.getLogger(__name__)


MODULE_PATH = os.path.join(os.path.dirname(__file__), 'wsdls')


WSDL_PATH = os.environ.get('CORREIOS_WSDL_PATH', MODULE_PATH)


SPECS = [
    {
        'get': 'https://apps.correios.com.br/'
        'SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl',
        'filename': 'AtendeCliente-production.wsdl'
    },
    {
        'get': 'https://apphom.correios.com.br/'
        'SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl',
        'filename': 'AtendeCliente-test.wsdl'
    },
    {
        'get': 'https://webservice.correios.com.br/'
        'service/rastro/Rastro.wsdl',
        'filename': 'Rastro.wsdl'
    },
    {
        'get': 'http://ws.correios.com.br/'
        'calculador/CalcPrecoPrazo.asmx?WSDL',
        'filename': 'CalcPrecoPrazo.asmx'
    },
    {
        'get': 'https://webservice.correios.com.br/'
        'service/rastro/Rastro_schema1.xsd',
        'filename': 'Rastro_schema1.xsd'
    },
]


def create_file(filename, body):
    file_path = os.path.join(WSDL_PATH, filename)
    logger.debug(
        'Creating file: {filename}\n'
        'Path: {path}'.format(filename=filename, path=WSDL_PATH)
    )
    with open(file_path, 'w+') as file:
        file.truncate()
        file.write(body)
        logger.debug(
            'Successfully create file: {filename}'.format(filename=filename)
        )


def update_wsdl():
    for file_spec in SPECS:
        logger.debug(
            'Updating File: {filename}'.format(**file_spec)
        )

        response = requests.get(file_spec['get'])

        if response.status_code != 200:
            logger.warning(
                'Fail to access Correios: {get}'.format(**file_spec)
            )
            continue

        create_file(file_spec['filename'], response.text)


if __name__ == '__main__':
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    update_wsdl()
