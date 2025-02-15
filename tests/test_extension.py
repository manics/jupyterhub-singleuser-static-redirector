import requests


def test_auth_required(jupyter_server):
    url, _ = jupyter_server
    r = requests.get(f"{url}static_redirector/")
    assert r.url == f"{url}login?next=%2Fstatic_redirector%2F"


def test_static_redirector(jupyter_server, destination):
    url, token = jupyter_server
    r = requests.get(f"{url}static_redirector/?token={token}")
    assert r.status_code == 200
    assert "<h1>Redirector</h1>" in r.text
    assert (
        f'<p><a href="{destination}" target="_blank">click here to continue</a></p>'
        in r.text
    )
