from unittest import mock

import pytest
import requests

from correios.update_wsdl import WSDL_PATH, update_wsdl


class TestUpdateWsdl:

    file_body = 'Whatever'

    @pytest.fixture
    def mock_logger(self):
        with mock.patch('correios.update_wsdl.logger') as mock_logger:
            yield mock_logger

    @pytest.fixture
    def mock_open(self):
        with mock.patch(
            'correios.update_wsdl.open',
            mock.mock_open(),
            create=True
        ) as mock_open:
            yield mock_open

    @pytest.fixture
    def mock_requests_get(self):
        with mock.patch('requests.Response') as mock_response:
            mock_response.text = self.file_body
            mock_response.status_code = 200

            with mock.patch.object(requests, 'get') as mock_get:
                mock_get.return_value = mock_response
                yield mock_get

    @pytest.fixture
    def mock_fail_requests_get(self):
        with mock.patch('requests.Response') as mock_response:
            mock_response.status_code = 500

            with mock.patch.object(requests, 'get') as mock_get:
                mock_get.return_value = mock_response
                yield mock_get

    def test_update_wsdl_success(
        self,
        mock_requests_get,
        mock_open,
        mock_logger
    ):
        update_wsdl()

        open_calls = [
            mock.call(
                '/'.join((WSDL_PATH, 'AtendeCliente-production.wsdl')), 'w+'
            ),
            mock.call('/'.join((WSDL_PATH, 'AtendeCliente-test.wsdl')), 'w+'),
            mock.call('/'.join((WSDL_PATH, 'Rastro.wsdl')), 'w+'),
            mock.call('/'.join((WSDL_PATH, 'CalcPrecoPrazo.asmx')), 'w+'),
            mock.call('/'.join((WSDL_PATH, 'Rastro_schema1.xsd')), 'w+'),
        ]

        mock_open.assert_has_calls(open_calls, any_order=True)

        mock_file = mock_open()

        mock_file.write.assert_called_with(self.file_body)
        assert mock_file.write.call_count == 5

    def test_update_wsdl_should_log_correctly(
        self,
        mock_requests_get,
        mock_open,
        mock_logger
    ):
        update_wsdl()

        debug_calls = [
            mock.call('Updating File: AtendeCliente-production.wsdl'),
            mock.call(
                'Creating file: AtendeCliente-production.wsdl\n'
                'Path: {path}'.format(path=WSDL_PATH)
            ),
            mock.call(
                'Successfully create file: AtendeCliente-production.wsdl'
            ),
            mock.call('Updating File: AtendeCliente-test.wsdl'),
            mock.call(
                'Creating file: AtendeCliente-test.wsdl\n'
                'Path: {path}'.format(path=WSDL_PATH)
            ),
            mock.call('Successfully create file: AtendeCliente-test.wsdl'),
            mock.call('Updating File: Rastro.wsdl'),
            mock.call('Creating file: Rastro.wsdl\nPath: {path}'.format(
                path=WSDL_PATH
            )),
            mock.call('Successfully create file: Rastro.wsdl'),
            mock.call('Updating File: CalcPrecoPrazo.asmx'),
            mock.call(
                'Creating file: CalcPrecoPrazo.asmx\n'
                'Path: {path}'.format(path=WSDL_PATH)
            ),
            mock.call('Successfully create file: CalcPrecoPrazo.asmx'),
            mock.call('Updating File: Rastro_schema1.xsd'),
            mock.call('Creating file: Rastro_schema1.xsd\nPath: {path}'.format(
                path=WSDL_PATH
            )),
            mock.call('Successfully create file: Rastro_schema1.xsd'),
        ]

        mock_logger.debug.assert_has_calls(debug_calls)

    def test_update_wsdl_fail(
        self,
        mock_fail_requests_get,
        mock_open,
        mock_logger
    ):
        update_wsdl()

        debug_calls = [
            mock.call(
                'Fail to access Correios: https://apps.correios.com.br/'
                'SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl'
            ),
            mock.call(
                'Fail to access Correios: https://apphom.correios.com.br/'
                'SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl'
            ),
            mock.call(
                'Fail to access Correios: https://webservice.correios.com.br/'
                'service/rastro/Rastro.wsdl'
            ),
            mock.call(
                'Fail to access Correios: http://ws.correios.com.br/'
                'calculador/CalcPrecoPrazo.asmx?WSDL'
            ),
            mock.call(
                'Fail to access Correios: https://webservice.correios.com.br/'
                'service/rastro/Rastro_schema1.xsd'
            )
        ]

        mock_logger.warning.assert_has_calls(debug_calls)
        mock_open.assert_not_called()
