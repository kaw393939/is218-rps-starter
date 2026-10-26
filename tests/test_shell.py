"""Checks for the supplied browser shell, not the unfinished game rules.

These tests stub the rule function. Students add tests/test_game.py with all
nine real matchups from SPEC.md and a real request/result check for RPS-001.
"""

# pytest injects fixtures by their function names; descriptive test names act
# as the test documentation. Keep all other Pylint diagnostics enabled.
# pylint: disable=redefined-outer-name,missing-function-docstring

import pytest

import app as web

pytestmark = pytest.mark.integration


@pytest.fixture
def client():
    web.app.config.update(TESTING=True)
    return web.app.test_client()


def test_page_has_three_labeled_moves(client):
    response = client.get("/")
    assert response.status_code == 200
    for move in ("rock", "paper", "scissors"):
        assert f'name="move" value="{move}"'.encode() in response.data
        assert move.capitalize().encode() in response.data


def test_completed_rules_hide_initial_starter_notice(client, monkeypatch):
    monkeypatch.setattr(web.game, "determine_winner", lambda _player, _computer: "tie")
    response = client.get("/")
    assert response.status_code == 200
    assert b"game rules not built yet" not in response.data


@pytest.mark.parametrize(
    ("outcome", "heading"),
    [("win", "You win!"), ("lose", "Computer wins"), ("tie", "It’s a tie")],
)
def test_shell_displays_stubbed_result(client, monkeypatch, outcome, heading):
    monkeypatch.setattr(web.random, "choice", lambda _moves: "scissors")
    monkeypatch.setattr(
        web.game, "determine_winner", lambda _player, _computer: outcome
    )
    response = client.post("/", data={"move": "rock"})
    page = response.get_data(as_text=True)
    assert response.status_code == 200
    assert heading in page
    assert 'data-outcome="' + outcome + '"' in page
    assert "You chose" in page and "Computer chose" in page
    assert "Rock" in page and "Scissors" in page
    assert "game rules not built yet" not in page


@pytest.mark.parametrize("method", ["GET", "POST"])
def test_unfinished_rules_have_friendly_message(client, monkeypatch, method):
    def unfinished(_player, _computer):
        raise NotImplementedError

    monkeypatch.setattr(web.game, "determine_winner", unfinished)
    response = client.open("/", method=method, data={"move": "paper"})
    assert response.status_code == 200
    assert b"Starter: game rules not built yet." in response.data
    assert b"data-outcome=" not in response.data


@pytest.mark.parametrize("move", ["lizard", "<script>alert(1)</script>", ""])
def test_invalid_move_is_rejected_before_rules(client, monkeypatch, move):
    def should_not_run(_player, _computer):
        pytest.fail("Invalid input must not reach the rule function")

    monkeypatch.setattr(web.game, "determine_winner", should_not_run)
    response = client.post("/", data={"move": move})
    assert response.status_code == 400
    assert b"Choose Rock, Paper, or Scissors to play." in response.data
    assert b"<script>" not in response.data


def test_missing_move_is_rejected(client, monkeypatch):
    def should_not_run(_player, _computer):
        pytest.fail("A missing move must not reach the rule function")

    monkeypatch.setattr(web.game, "determine_winner", should_not_run)
    response = client.post("/")
    assert response.status_code == 400
    assert b"Choose Rock, Paper, or Scissors to play." in response.data


def test_stylesheet_is_available(client):
    response = client.get("/static/style.css")
    assert response.status_code == 200
    assert b"focus-visible" in response.data


def test_check_server_has_no_development_refresh(client):
    assert b"dev-refresh.js" not in client.get("/").data
    assert client.get("/__dev__/revision").status_code == 404
