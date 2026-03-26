import pytest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))

from app.services.oracle_client import OracleClient, OracleConnectionConfig


def test_oracle_connection_config():
    config = OracleConnectionConfig(
        host="localhost",
        port=1521,
        username="system",
        password="password",
        service_name="ORCL"
    )
    
    assert config.host == "localhost"
    assert config.port == 1521
    assert config.username == "system"
    assert config.service_name == "ORCL"


def test_oracle_connection_config_with_sid():
    config = OracleConnectionConfig(
        host="localhost",
        port=1521,
        username="system",
        password="password",
        sid="ORCL",
        connection_type="sid"
    )
    
    assert config.sid == "ORCL"
    assert config.connection_type == "sid"


@patch('oracledb.connect')
def test_oracle_client_connect(mock_connect):
    config = OracleConnectionConfig(
        host="localhost",
        port=1521,
        username="system",
        password="password",
        service_name="ORCL"
    )
    
    client = OracleClient(config)
    
    with client.get_connection() as conn:
        mock_connect.assert_called_once()
    
    conn.close()


@patch('oracledb.connect')
def test_test_connection_success(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ("Oracle Database 19c",)
    mock_conn.cursor.return_value = mock_cursor
    mock_connect = MagicMock(return_value=mock_conn)
    
    config = OracleConnectionConfig(
        host="localhost",
        port=1521,
        username="system",
        password="password",
        service_name="ORCL"
    )
    
    client = OracleClient(config)
    
    with patch('app.services.oracle_client.oracledb.connect', mock_connect):
        success, message, version = client.test_connection()
    
    assert success is True
    assert version == "Oracle Database 19c"


@patch('oracledb.connect')
def test_test_connection_failure(mock_connect):
    mock_connect.side_effect = Exception("Connection failed")
    
    config = OracleConnectionConfig(
        host="localhost",
        port=1521,
        username="system",
        password="wrong",
        service_name="ORCL"
    )
    
    client = OracleClient(config)
    
    with patch('app.services.oracle_client.oracledb.connect', mock_connect):
        success, message, version = client.test_connection()
    
    assert success is False
    assert "Connection failed" in message
