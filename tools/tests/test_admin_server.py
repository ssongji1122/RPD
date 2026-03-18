from __future__ import annotations

import http.client
import json
import os
import socket
import subprocess
import sys
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class AdminServerSecurityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.port = _find_free_port()
        env = os.environ.copy()
        env["ADMIN_KEY"] = "test-admin-key"
        env["PYTHONUNBUFFERED"] = "1"
        cls.proc = subprocess.Popen(
            [
                sys.executable,
                "tools/admin-server.py",
                "--host",
                "127.0.0.1",
                "--port",
                str(cls.port),
            ],
            cwd=ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        last_error = "server did not start"
        for _ in range(60):
            try:
                status, _, _ = cls.request("GET", "/api/admin/session")
                if status in (200, 401):
                    return
            except Exception as exc:  # pragma: no cover - startup polling
                last_error = str(exc)
                time.sleep(0.1)

        output = ""
        if cls.proc.stdout is not None:
            output = cls.proc.stdout.read()
        raise RuntimeError(f"admin server failed to start: {last_error}\n{output}")

    @classmethod
    def tearDownClass(cls) -> None:
        if getattr(cls, "proc", None) is None:
            return
        cls.proc.terminate()
        try:
            cls.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:  # pragma: no cover - defensive cleanup
            cls.proc.kill()
            cls.proc.wait(timeout=5)

    @classmethod
    def request(
        cls,
        method: str,
        path: str,
        body: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> tuple[int, dict[str, str], str]:
        connection = http.client.HTTPConnection("127.0.0.1", cls.port, timeout=5)
        try:
            connection.request(method, path, body=body, headers=headers or {})
            response = connection.getresponse()
            payload = response.read().decode("utf-8", errors="replace")
            return response.status, dict(response.getheaders()), payload
        finally:
            connection.close()

    def test_unauthorized_curriculum_is_rejected(self) -> None:
        status, _, payload = self.request("GET", "/api/curriculum")
        self.assertEqual(status, 401)
        self.assertIn("Unauthorized", payload)

    def test_cross_origin_login_is_rejected(self) -> None:
        status, _, payload = self.request(
            "POST",
            "/api/admin/login",
            body=json.dumps({"password": "test-admin-key"}),
            headers={
                "Content-Type": "application/json",
                "Origin": "https://evil.example",
            },
        )
        self.assertEqual(status, 403)
        self.assertIn("Cross-origin", payload)

    def test_login_sets_cookie_and_allows_curriculum_read(self) -> None:
        status, headers, payload = self.request(
            "POST",
            "/api/admin/login",
            body=json.dumps({"password": "test-admin-key"}),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(status, 200, payload)
        cookie = headers.get("Set-Cookie", "")
        self.assertIn("rpd_admin_session=", cookie)

        read_status, _, read_payload = self.request(
            "GET",
            "/api/curriculum",
            headers={"Cookie": cookie.split(";", 1)[0]},
        )
        self.assertEqual(read_status, 200, read_payload)
        parsed = json.loads(read_payload)
        self.assertIn("data", parsed)
        self.assertIn("version", parsed)

    def test_public_quiz_sync_is_disabled(self) -> None:
        status, _, payload = self.request(
            "POST",
            "/api/notion-quiz",
            body=json.dumps({"week": 1}),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(status, 410)
        self.assertIn("disabled", payload)


if __name__ == "__main__":
    unittest.main()
