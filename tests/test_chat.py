import asyncio
import json

import pytest

from galaxy.api.types import Room, Message
from galaxy.api.errors import (
    UnknownError, AuthenticationRequired, BackendNotAvailable, BackendTimeout, BackendError,
    TooManyMessagesSent, IncoherentLastMessage, MessageNotFound
)

def test_send_message_success(plugin, read, write):
    request = {
        "jsonrpc": "2.0",
        "id": "3",
        "method": "send_message",
        "params": {
            "room_id": "14",
            "message": "Hello!"
        }
    }

    read.side_effect = [json.dumps(request).encode() + b"\n", b""]
    plugin.send_message.coro.return_value = None
    asyncio.run(plugin.run())
    plugin.send_message.assert_called_with(room_id="14", message="Hello!")
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "id": "3",
        "result": None
    }

@pytest.mark.parametrize("error,code,message", [
    pytest.param(UnknownError, 0, "Unknown error", id="unknown_error"),
    pytest.param(AuthenticationRequired, 1, "Authentication required", id="not_authenticated"),
    pytest.param(BackendNotAvailable, 2, "Backend not available", id="backend_not_available"),
    pytest.param(BackendTimeout, 3, "Backend timed out", id="backend_timeout"),
    pytest.param(BackendError, 4, "Backend error", id="backend_error"),
    pytest.param(TooManyMessagesSent, 300, "Too many messages sent", id="too_many_messages")
])
def test_send_message_failure(plugin, read, write, error, code, message):
    request = {
        "jsonrpc": "2.0",
        "id": "6",
        "method": "send_message",
        "params": {
            "room_id": "15",
            "message": "Bye"
        }
    }

    read.side_effect = [json.dumps(request).encode() + b"\n", b""]
    plugin.send_message.coro.side_effect = error()
    asyncio.run(plugin.run())
    plugin.send_message.assert_called_with(room_id="15", message="Bye")
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "id": "6",
        "error": {
            "code": code,
            "message": message
        }
    }

def test_mark_as_read_success(plugin, read, write):
    request = {
        "jsonrpc": "2.0",
        "id": "7",
        "method": "mark_as_read",
        "params": {
            "room_id": "14",
            "last_message_id": "67"
        }
    }

    read.side_effect = [json.dumps(request).encode() + b"\n", b""]
    plugin.mark_as_read.coro.return_value = None
    asyncio.run(plugin.run())
    plugin.mark_as_read.assert_called_with(room_id="14", last_message_id="67")
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "id": "7",
        "result": None
    }

@pytest.mark.parametrize("error,code,message", [
    pytest.param(UnknownError, 0, "Unknown error", id="unknown_error"),
    pytest.param(AuthenticationRequired, 1, "Authentication required", id="not_authenticated"),
    pytest.param(BackendNotAvailable, 2, "Backend not available", id="backend_not_available"),
    pytest.param(BackendTimeout, 3, "Backend timed out", id="backend_timeout"),
    pytest.param(BackendError, 4, "Backend error", id="backend_error"),
    pytest.param(
        IncoherentLastMessage,
        400,
        "Different last message id on backend",
        id="incoherent_last_message"
    )
])
def test_mark_as_read_failure(plugin, read, write, error, code, message):
    request = {
        "jsonrpc": "2.0",
        "id": "4",
        "method": "mark_as_read",
        "params": {
            "room_id": "18",
            "last_message_id": "7"
        }
    }

    read.side_effect = [json.dumps(request).encode() + b"\n", b""]
    plugin.mark_as_read.coro.side_effect = error()
    asyncio.run(plugin.run())
    plugin.mark_as_read.assert_called_with(room_id="18", last_message_id="7")
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "id": "4",
        "error": {
            "code": code,
            "message": message
        }
    }

def test_get_rooms_success(plugin, read, write):
    request = {
        "jsonrpc": "2.0",
        "id": "2",
        "method": "import_rooms"
    }

    read.side_effect = [json.dumps(request).encode() + b"\n", b""]
    plugin.get_rooms.coro.return_value = [
        Room("13", 0, None),
        Room("15", 34, "8")
    ]
    asyncio.run(plugin.run())
    plugin.get_rooms.assert_called_with()
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "id": "2",
        "result": {
            "rooms": [
                {
                    "room_id": "13",
                    "unread_message_count": 0,
                },
                {
                    "room_id": "15",
                    "unread_message_count": 34,
                    "last_message_id": "8"
                }
            ]
        }
    }

def test_get_rooms_failure(plugin, read, write):
    request = {
        "jsonrpc": "2.0",
        "id": "9",
        "method": "import_rooms"
    }

    read.side_effect = [json.dumps(request).encode() + b"\n", b""]
    plugin.get_rooms.coro.side_effect = UnknownError()
    asyncio.run(plugin.run())
    plugin.get_rooms.assert_called_with()
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "id": "9",
        "error": {
            "code": 0,
            "message": "Unknown error"
        }
    }

def test_get_room_history_from_message_success(plugin, read, write):
    request = {
        "jsonrpc": "2.0",
        "id": "2",
        "method": "import_room_history_from_message",
        "params": {
            "room_id": "34",
            "message_id": "66"
        }
    }

    read.side_effect = [json.dumps(request).encode() + b"\n", b""]
    plugin.get_room_history_from_message.coro.return_value = [
        Message("13", "149", 1549454837, "Hello"),
        Message("14", "812", 1549454899, "Hi")
    ]
    asyncio.run(plugin.run())
    plugin.get_room_history_from_message.assert_called_with(room_id="34", message_id="66")
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "id": "2",
        "result": {
            "messages": [
                {
                    "message_id": "13",
                    "sender_id": "149",
                    "sent_time": 1549454837,
                    "message_text": "Hello"
                },
                {
                    "message_id": "14",
                    "sender_id": "812",
                    "sent_time": 1549454899,
                    "message_text": "Hi"
                }
            ]
        }
    }

@pytest.mark.parametrize("error,code,message", [
    pytest.param(UnknownError, 0, "Unknown error", id="unknown_error"),
    pytest.param(AuthenticationRequired, 1, "Authentication required", id="not_authenticated"),
    pytest.param(BackendNotAvailable, 2, "Backend not available", id="backend_not_available"),
    pytest.param(BackendTimeout, 3, "Backend timed out", id="backend_timeout"),
    pytest.param(BackendError, 4, "Backend error", id="backend_error"),
    pytest.param(MessageNotFound, 500, "Message not found", id="message_not_found")
])
def test_get_room_history_from_message_failure(plugin, read, write, error, code, message):
    request = {
        "jsonrpc": "2.0",
        "id": "7",
        "method": "import_room_history_from_message",
        "params": {
            "room_id": "33",
            "message_id": "88"
        }
    }

    read.side_effect = [json.dumps(request).encode() + b"\n", b""]
    plugin.get_room_history_from_message.coro.side_effect = error()
    asyncio.run(plugin.run())
    plugin.get_room_history_from_message.assert_called_with(room_id="33", message_id="88")
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "id": "7",
        "error": {
            "code": code,
            "message": message
        }
    }

def test_get_room_history_from_timestamp_success(plugin, read, write):
    request = {
        "jsonrpc": "2.0",
        "id": "7",
        "method": "import_room_history_from_timestamp",
        "params": {
            "room_id": "12",
            "from_timestamp": 1549454835
        }
    }

    read.side_effect = [json.dumps(request).encode() + b"\n", b""]
    plugin.get_room_history_from_timestamp.coro.return_value = [
        Message("12", "155", 1549454836, "Bye")
    ]
    asyncio.run(plugin.run())
    plugin.get_room_history_from_timestamp.assert_called_with(
        room_id="12",
        from_timestamp=1549454835
    )
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "id": "7",
        "result": {
            "messages": [
                {
                    "message_id": "12",
                    "sender_id": "155",
                    "sent_time": 1549454836,
                    "message_text": "Bye"
                }
            ]
        }
    }

def test_get_room_history_from_timestamp_failure(plugin, read, write):
    request = {
        "jsonrpc": "2.0",
        "id": "3",
        "method": "import_room_history_from_timestamp",
        "params": {
            "room_id": "10",
            "from_timestamp": 1549454800
        }
    }

    read.side_effect = [json.dumps(request).encode() + b"\n", b""]
    plugin.get_room_history_from_timestamp.coro.side_effect = UnknownError()
    asyncio.run(plugin.run())
    plugin.get_room_history_from_timestamp.assert_called_with(
        room_id="10",
        from_timestamp=1549454800
    )
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "id": "3",
        "error": {
            "code": 0,
            "message": "Unknown error"
        }
    }

def test_update_room(plugin, write):
    messages = [
        Message("10", "898", 1549454832, "Hi")
    ]

    async def couritine():
        plugin.update_room("14", 15, messages)

    asyncio.run(couritine())
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "method": "chat_room_updated",
        "params": {
            "room_id": "14",
            "unread_message_count": 15,
            "messages": [
                {
                    "message_id": "10",
                    "sender_id": "898",
                    "sent_time": 1549454832,
                    "message_text": "Hi"
                }
            ]
        }
    }
