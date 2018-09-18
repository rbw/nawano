# -*- coding: utf-8 -*-

import passwordmeter
from prompt_toolkit.validation import Validator, ValidationError


class PasswordQualityValidator(Validator):
    def validate(self, document):
        pw = document.text
        strength = passwordmeter.test(pw)[0] * 100
        min_strength = 80
        if strength < min_strength:
            raise ValidationError(message='strength {0:.3} < {1} ({2})'.format(strength, min_strength, 'too weak'))


class ConfirmValidator(Validator):
    def __init__(self, match, *args, **kwargs):
        self.match = match
        super(ConfirmValidator, self).__init__(*args, **kwargs)

    def validate(self, document):
        if document.text != self.match:
            raise ValidationError(message='the passwords must match')
