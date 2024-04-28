from helpers import SpiceShopClientFactory


def app():
    SpiceShopClientFactory.create()


if __name__ == "__main__":
    app()
