from collections.abc import Callable, Iterable
from multiprocessing import Event, Process, Queue
from queue import Empty
from typing import Any


class ParallelAttackManager:
    def __init__(
        self,
        process_count: int,
        stop_event=None,
        result_queue=None
    ):
        if process_count <= 0:
            raise ValueError(
                "Process count must be greater than 0."
            )

        self.process_count = process_count

        self.stop_event = (
            stop_event
            if stop_event is not None
            else Event()
        )

        self.result_queue = (
            result_queue
            if result_queue is not None
            else Queue()
        )

        self.processes: list[Process] = []

    def run(
        self,
        worker: Callable[[Any, Any], Any | None],
        tasks: Iterable[Any]
    ) -> Any | None:
       #Starting proccesses
       #worker: function making one task returning result or none
        self.stop_event.clear()
        self.processes.clear()
        self._clear_result_queue()

        task_queue = Queue()
        task_count = 0

        for task in tasks:
            task_queue.put(task)
            task_count += 1

        if task_count == 0:
            return None

        worker_count = min(
            self.process_count,
            task_count
        )

        for _ in range(worker_count):
            process = Process(
                target=self._worker_loop,
                args=(
                    worker,
                    task_queue,
                    self.result_queue,
                    self.stop_event
                )
            )

            process.start()
            self.processes.append(process)

        result = None
        finished_workers = 0

        try:
            while finished_workers < worker_count:
                try:
                    message_type, value = self.result_queue.get(
                        timeout=0.1
                    )
                except Empty:
                    if not any(
                        process.is_alive()
                        for process in self.processes
                    ):
                        break

                    continue

                if message_type == "found":
                    result = value
                    self.stop_event.set()

                elif message_type == "error":
                    self.stop_event.set()

                    raise RuntimeError(
                        f"Worker process failed: {value}"
                    )

                elif message_type == "finished":
                    finished_workers += 1

        finally:
            self._cleanup_processes()

        return result

    def stop(self) -> None:
        """Przekazuje wszystkim procesom żądanie zatrzymania."""
        self.stop_event.set()

    def is_running(self) -> bool:
        return any(
            process.is_alive()
            for process in self.processes
        )

    def _cleanup_processes(self) -> None:
        for process in self.processes:
            process.join(timeout=1)

            if process.is_alive():
                process.terminate()
                process.join()

        self.processes.clear()

    def _clear_result_queue(self) -> None:
        while True:
            try:
                self.result_queue.get_nowait()
            except Empty:
                break

    @staticmethod
    def _worker_loop(
        worker: Callable[[Any, Any], Any | None],
        task_queue,
        result_queue,
        stop_event
    ) -> None:
        try:
            while not stop_event.is_set():
                try:
                    task = task_queue.get_nowait()
                except Empty:
                    break

                result = worker(task, stop_event)

                if result is not None:
                    result_queue.put(
                        ("found", result)
                    )

                    stop_event.set()
                    break

        except Exception as error:
            result_queue.put(
                ("error", repr(error))
            )

            stop_event.set()

        finally:
            result_queue.put(
                ("finished", None)
            )