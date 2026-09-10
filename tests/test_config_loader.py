from src.config_loader import load_assets


def test_load_assets():

    config = load_assets()

    assert "stocks" in config
    assert "crypto" in config

    assert len(config["stocks"]) > 0
    assert len(config["crypto"]) > 0