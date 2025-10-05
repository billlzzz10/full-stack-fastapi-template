from unittest.mock import MagicMock, patch

from app.backend_pre_start import init, logger


def test_init_successful_connection() -> None:
    engine_mock = MagicMock()

    session_mock = MagicMock()
    session_mock.__enter__.return_value = session_mock
    session_mock.exec.return_value = True

    sentinel_statement = object()

    with (
        patch("app.backend_pre_start.Session", return_value=session_mock),
        patch("app.backend_pre_start.select", return_value=sentinel_statement) as select_mock,
        patch.object(logger, "info"),
        patch.object(logger, "error"),
        patch.object(logger, "warn"),
    ):
        try:
            init(engine_mock)
            connection_successful = True
        except Exception:
            connection_successful = False

    assert (
        connection_successful
    ), "The database connection should be successful and not raise an exception."

    select_mock.assert_called_once_with(1)
    session_mock.exec.assert_called_once_with(sentinel_statement)
