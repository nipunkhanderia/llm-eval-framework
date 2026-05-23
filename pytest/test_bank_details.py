import pytest
from bank_details import create_account
from bank_details import search_account
from bank_details import account_list

def test_create_account():
    accntlist = create_account("Nipun", 100)
    new_accnt = accntlist[-1]
    assert new_accnt["name"] == "Nipun" 


def test_search():
    create_account ("Stark", 100)
    result = search_account("Stark")
    assert result == "Stark", "name not found"



@pytest.fixture
def set_up_acount():
    create_account("Nipun", 100)
    create_account("Rhythm", 200)
    return account_list

def test_search_function(set_up_acount):
    result = search_account("Nipun")
    assert result == "Nipun"

def Test_create_Acount(set_up_acount):
        acc = account_list[0]
        assert acc["name"] == "Nipun", "Name not found people"
