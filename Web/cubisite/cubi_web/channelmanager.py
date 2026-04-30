from django_eventstream.channelmanager import DefaultChannelManager


class UserChannelManager(DefaultChannelManager):
    def can_read_channel(self, user, channel):
        if not user or not user.is_authenticated:
            return False
        return channel == f'user-{user.pk}'
