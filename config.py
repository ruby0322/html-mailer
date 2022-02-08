class Config:
    
    def __init__(self, config_dict: dict) -> None:
        for key, value in config_dict.items():
            setattr(self, key, value)
        self.sender_mail = ''
        self.sender_password = ''

    def get_subject_full_path(self) -> str:
        return self.assets_folder_path + '/mail/subject/' + self.subject_file_name

    def get_body_full_path(self) -> str:
        return self.assets_folder_path + '/mail/body/' + self.body_file_name

    def get_greeting_full_path(self) -> str:
        return self.assets_folder_path + '/mail/greeting/' + self.greeting_file_name

    def get_closing_full_path(self) -> str:
        return self.assets_folder_path + '/mail/closing/' + self.closing_file_name

    def get_template_full_path(self) -> str:
        return self.assets_folder_path + '/mail/template/' + self.template_file_name

    def get_receiver_full_path(self) -> str:
        return self.assets_folder_path + '/mail/receiver/' + self.receiver_file_name

    def get_sender_full_path(self) -> str:
        return self.assets_folder_path + '/mail/sender/' + self.sender_file_name

    def __repr__(self) -> str:
        return self.__dict__.__repr__()