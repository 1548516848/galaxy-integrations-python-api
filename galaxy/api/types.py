from dataclasses import dataclass
from typing import List, Dict, Optional

from galaxy.api.consts import LicenseType, LocalGameState, PresenceState

@dataclass
class Authentication():
    user_id: str
    user_name: str

@dataclass
class Cookie():
    name: str
    value: str
    domain: Optional[str] = None
    path: Optional[str] = None

@dataclass
class NextStep():
    next_step: str
    auth_params: Dict[str, str]
    cookies: Optional[List[Cookie]] = None

@dataclass
class LicenseInfo():
    license_type: LicenseType
    owner: Optional[str] = None

@dataclass
class Dlc():
    dlc_id: str
    dlc_title: str
    license_info: LicenseInfo

@dataclass
class Game():
    game_id: str
    game_title: str
    dlcs: List[Dlc]
    license_info: LicenseInfo

@dataclass
class Achievement():
    unlock_time: int
    achievement_id: Optional[str] = None
    achievement_name: Optional[str] = None

    def __post_init__(self):
        assert self.achievement_id or self.achievement_name, \
            "One of achievement_id or achievement_name is required"

@dataclass
class LocalGame():
    game_id: str
    local_game_state: LocalGameState

@dataclass
class Presence():
    presence_state: PresenceState
    game_id: Optional[str] = None
    presence_status: Optional[str] = None

@dataclass
class UserInfo():
    user_id: str
    is_friend: bool
    user_name: str
    avatar_url: str
    presence: Presence

@dataclass
class Room():
    room_id: str
    unread_message_count: int
    last_message_id: str

@dataclass
class Message():
    message_id: str
    sender_id: str
    sent_time: int
    message_text: str

@dataclass
class GameTime():
    game_id: str
    time_played: int
    last_played_time: int
