"""Intentionally broken training code. Do not copy into production."""


def get_customer(fetch, customer_id):
    for _ in range(3):
        try:
            response = fetch("/customers/" + customer_id)
            if response.status_code != 200:
                continue
            break
        except Exception:
            continue
    return response.json()["customer"]

