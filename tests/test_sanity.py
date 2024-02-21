from r2k.config import Config


def test_read_config(tmp_path):
    """Config can be saved and read."""
    config_contents = """
    {
        "kindle_address": "test@kindle.com",
        "send_from": "test@gmail.com"
    }
    """
    config_file = tmp_path / "config.yml"
    config_file.write_text(config_contents)

    config = Config()
    config.load(config_file)

    assert config.kindle_address == "test@kindle.com"
    assert config.send_from == "test@gmail.com"
