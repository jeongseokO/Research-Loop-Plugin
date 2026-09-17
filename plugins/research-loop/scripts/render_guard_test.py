"""Small process-control tests; no heavy render or CPU workloads."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import render_guard as guard


class GuardTests(unittest.TestCase):
    def test_lock_rejects_concurrent_run_and_releases(self):
        with tempfile.TemporaryDirectory() as temporary, patch.object(guard.tempfile, "gettempdir", return_value=temporary):
            with guard.render_lock():
                with self.assertRaisesRegex(guard.RenderLimitError, "Another"):
                    with guard.render_lock():
                        self.fail("concurrent lock acquired")
            with guard.render_lock():
                pass

    def test_child_thread_environment_and_timeout(self):
        with tempfile.TemporaryDirectory() as temporary, patch.object(guard.tempfile, "gettempdir", return_value=temporary):
            script = Path(temporary) / "child.py"
            script.write_text("import os\nassert os.environ['OPENBLAS_NUM_THREADS'] == '1'\nassert os.environ['MPLBACKEND'] == 'Agg'\n")
            self.assertEqual(guard.run_python(script), 0)
            script.write_text("import time\ntime.sleep(10)\n")
            with self.assertRaisesRegex(guard.RenderLimitError, "stopped"):
                guard.run_python(script, timeout=0.05)
            # Timeout releases the lock, allowing the next small job to start.
            script.write_text("pass\n")
            self.assertEqual(guard.run_python(script), 0)

    def test_invalid_timeout_before_spawn(self):
        for timeout in (0, -1, 121, float("inf"), float("nan"), True):
            with patch.object(guard.subprocess, "Popen") as spawn:
                with self.assertRaises(guard.RenderLimitError):
                    guard.run_python("unused.py", timeout=timeout)
                spawn.assert_not_called()


if __name__ == "__main__":
    unittest.main()
