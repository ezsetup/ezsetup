from raven import Client

client = Client('https://895b854bf0c341e687981dd5215b6a09:ff2920d177f6421daee140381b35d293@sentry.io/194123')

try:
    1 / 0
except Exception:
    client.captureException()

