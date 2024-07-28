from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, email, role):
        return f"{email}{role}"


generate_token = AppTokenGenerator()
