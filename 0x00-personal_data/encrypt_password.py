#!/usr/bin/env python3
""" Python Module """
import bcrypt


def hash_password(password: str) -> bytes:
    """ function that takes a string and hash it """
    encoded_psw = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(encoded_psw, salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Validate if a has is valid """
    encoded_psw = bytes(password, 'utf-8')
    if bcrypt.checkpw(encoded_psw, hashed_password) is True:
        return True
    return False
