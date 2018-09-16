# -*- coding: utf-8 -*-

import passwordmeter
from prompt_toolkit.validation import Validator, ValidationError


class PasswordQualityValidator(Validator):
    def validate(self, document):
        pw = document.text
        strength, _ = passwordmeter.test(pw)
        if strength < 0.9:
            raise ValidationError(message='strength {0:.3} < 90 ({1})'.format(strength * 100, 'too weak'))


class ConfirmValidator(Validator):
    def __init__(self, match, *args, **kwargs):
        self.match = match
        super(ConfirmValidator, self).__init__(*args, **kwargs)

    def validate(self, document):
        if document.text != self.match:
            raise ValidationError(message='the passwords must match')
