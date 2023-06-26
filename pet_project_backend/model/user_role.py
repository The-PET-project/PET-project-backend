from enum import Enum


class UserRole(Enum):
    ADMIN = (True, True, True, True, True, True)
    USER = (True, True, True, True, False, False)
    GUEST = (True, False, False, False, False, False)

    def __init__(
        self,
        browse_private_sites: bool,
        add_content: bool,
        edit_content: bool,
        send_message: bool,
        edit_accounts: bool,
        delete_accounts: bool,
    ):
        self.can_browse_private_sites: bool = browse_private_sites
        self.can_add_content: bool = add_content
        self.can_edit_content: bool = edit_content
        self.can_send_message: bool = send_message
        self.can_edit_accounts: bool = edit_accounts
        self.can_delete_accounts: bool = delete_accounts

    @staticmethod
    def resolve(user_type: str):
        try:
            return UserRole[user_type]
        except KeyError:
            return UserRole.GUEST
