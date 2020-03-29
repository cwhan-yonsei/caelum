from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +
            str(user.is_active)
        )


account_activation_token = ActivationTokenGenerator()

class PWResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +
            str(user.is_active)
        )


pw_reset_token = PWResetTokenGenerator()
