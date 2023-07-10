from datetime import datetime
import json

from utils import funcs
def test_get_data():
    data = funcs.get_data()
    assert isinstance(data, list)

def test_executed_operations():
    result = funcs.executed_operations()
    assert isinstance(result, list)
    assert all(operation.get('state', '').lower() == 'executed' for operation in result)

def test_sort_data():
    result = funcs.sort_data()
    assert isinstance(result, list)
    assert all(isinstance(operation['date'], str) for operation in result)
    sorted_result = sorted(result, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)
    assert result == sorted_result

def test_last_operations():
    result = funcs.last_operations()
    assert isinstance(result, list)
    assert len(result) <= 5
    assert all(operation in funcs.sort_data()[:5] for operation in result)

def test_hiding_card():
    data = [
        {'description': 'Test 1', 'from': '1234567890123456', 'to': '1234567890123456'},
        {'description': 'Test 2', 'from': '12345678901234567890', 'to': '12345678901234567890'},
    ]
    result = funcs.hiding_card(data)
    assert isinstance(result, list)
    assert all('123456**********' in operation['from'] for operation in result)
    assert all('123456**********' in operation['to'] for operation in result)

def test_date_new():
    data = [{'date': '2022-01-01T00:00:00.000000', 'description': 'Test'}]
    result = funcs.date_new(data)
    assert isinstance(result, list)
    assert all(operation['date'] == '01.01.2022' for operation in result)

def test_result_output(capsys):
    data = [
        {'date': '2022-01-01T00:00:00.000000', 'description': 'Test', 'from': '1234567890123456', 'to': '1234567890123456'},
        {'date': '2022-01-02T00:00:00.000000', 'description': 'Test', 'from': '1234567890123456', 'to': '1234567890123456'},
    ]
    funcs.result_output(data)
    captured = capsys.readouterr()
    expected_output = "01.01.2022\n02.01.2022\n"
    assert captured.out == expected_output
'''''схожий пример
    import pytest
    import json
    import datetime
    from utils import funcs
    @pytest.fixture
    def operations_list():
        """Provide some operations from operations.json for each test."""
        return [{'state': 'executed', 'date': '2022-07-12T14:30:10.123', 'description': 'перевод', 'from': 'test_from', 'to': 'test_to', 'operationAmount': {'amount': 10, 'currency': {'name': 'USD'}}}]
    
    @pytest.fixture
    def operations_dict():
        """Provides single operations dictionary"""
        return {'state': 'executed', 'date': '2022-07-12T14:30:10.123', 'description': 'перевод', 'from': 'test_from', 'to': 'test_to', 'operationAmount': {'amount': 10, 'currency': {'name': 'USD'}}}
    
    
    def test_executed_operations(operations_list):
        with open('operations.json', 'w', encoding='utf-8') as file:
            json.dump(operations_list, file)
        assert funcs.executed_operations() == operations_list
    
    def test_sort_data(operations_list):
        with open('operations.json', 'w', encoding='utf-8') as file:
            json.dump(operations_list, file)
        assert funcs.sort_data() == operations_list
    
    def test_hiding_card(operations_dict):
        operations_list = [operations_dict]
        assert funcs.hiding_card(operations_list) == [{'state': 'executed', 'date': '2022-07-12T14:30:10.123', 'description': 'перевод', 'from': '****om', 'to': 'te**o', 'operationAmount': {'amount': 10, 'currency': {'name': 'USD'}}}]
    
    def test_date_new(operations_dict):
        operations_list = [operations_dict]
        funcs.hiding_card(operations_list)
        assert funcs.date_new(operations_list) == [{'state': 'executed', 'date': '12.07.2022', 'description': 'перевод', 'from': '****om', 'to': 'te**o', 'operationAmount': {'amount': 10, 'currency': {'name': 'USD'}}}]
'''''
