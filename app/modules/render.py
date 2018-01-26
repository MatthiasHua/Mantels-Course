from flask import Blueprint, render_template

def render_template_with_user(url, **kwarg):
    r = render_template
    r.role = session.get('role', '')
    r.username = session.get('username', '')
    return r(url, kwarg)
