import pytest
from bank_details import create_account
from bank_details import search_account

def test_create_account():
    accntlist = create_account("Nipun", 100)
    new_accnt = accntlist[-1]
    assert new_accnt["name"] == "Nipun" 


def test_search():
    create_account ("Stark", 100)
    result = search_account("Stark")
    assert result == "Stark", "name not found"

