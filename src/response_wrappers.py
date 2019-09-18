class Responses:
    """
    Contains wrappers to aid plugin developers with handling return values to the bot

    ...

    Methods
    -------
    respond_message()
        Returns a formated dictionary indicating a message response type and the str response as message_str

    respond_photo()
        Returns a formated dictionary indicating a photo response type, and optional str caption
        and the path to the photo file_path
    """

    @staticmethod
    def respond_message(message_str):
        """
        Returns a formated dictionary indicating a message response type and the str response as message_str

        ...

        Parameters
        ----------
        message_str: str
            A str message to be sent as a response to a command or message
        """

        return {"type":"message", "message": message_str}

    @staticmethod
    def respond_photo(caption_str, file_path):
        """
        Returns a formated dictionary indicating a photo response type, and optional str caption
        and the path to the photo file_path

        ...

        Parameters
        ----------
        caption_str: str
            A str message to be captioned under a photo
        file_path: str
            The full path to the photo to be sent
        """

        if not caption_str:
            return {"type": "photo", "caption": "", "file_name": file_path}
        return {"type": "photo", "caption": caption_str, "file_name": file_path}