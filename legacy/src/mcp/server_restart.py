import psutil
import subprocess
import time
import logging
from pathlib import Path
from typing import List, Optional
logger = logging.getLogger(__name__)

def _is_mcp_server_process(proc_info: dict, bot_name: str=None) -> bool:
    name = proc_info.get('name', '').lower()
    if 'python' not in name:
        return False
    cmdline = proc_info.get('cmdline') or []
    cmdline_str = ' '.join(cmdline)
    if 'mcp_server' not in cmdline_str:
        return False
    return bot_name is None or bot_name in cmdline_str

def find_mcp_server_processes(bot_name: str=None) -> List[int]:
    pids = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            pid = _try_get_process_pid(proc, bot_name)
            if pid is not None:
                pids.append(pid)
    except Exception as e:
        logger.warning(f'Error finding MCP processes: {e}')
    return pids

def _try_get_process_pid(proc, bot_name: str) -> Optional[int]:
    try:
        if _is_mcp_server_process(proc.info, bot_name):
            return proc.info['pid']
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        logger.debug(f'Could not access process info: {e}')
    return None

def terminate_processes(pids: List[int], timeout: int=5) -> dict:
    result = {'terminated': [], 'killed': [], 'failed': []}
    processes = _send_sigterm_to_processes(pids, result)
    gone, alive = psutil.wait_procs(processes, timeout=timeout)
    _record_terminated_processes(gone, result)
    _force_kill_remaining(alive, result)
    return result

def _send_sigterm_to_processes(pids: List[int], result: dict) -> list:
    processes = []
    for pid in pids:
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            processes.append(proc)
            logger.info(f'Sent SIGTERM to process {pid}')
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logger.warning(f'Could not terminate process {pid}: {e}')
            result['failed'].append(pid)
    return processes

def _record_terminated_processes(gone: list, result: dict):
    for proc in gone:
        result['terminated'].append(proc.pid)
        logger.info(f'Process {proc.pid} terminated gracefully')

def _force_kill_remaining(alive: list, result: dict):
    for proc in alive:
        try:
            proc.kill()
            proc.wait(timeout=2)
            result['killed'].append(proc.pid)
            logger.info(f'Process {proc.pid} force killed')
        except Exception as e:
            logger.error(f'Failed to kill process {proc.pid}: {e}')
            result['failed'].append(proc.pid)

def clear_python_cache(root_path: Path) -> int:
    cleared = 0
    root = Path(root_path)
    for pycache_dir in root.rglob('__pycache__'):
        try:
            for cache_file in pycache_dir.glob('*.pyc'):
                cache_file.unlink()
            for cache_file in pycache_dir.glob('*.pyo'):
                cache_file.unlink()
            pycache_dir.rmdir()
            cleared += 1
            logger.info(f'Cleared cache: {pycache_dir}')
        except Exception as e:
            logger.warning(f'Failed to clear cache {pycache_dir}: {e}')
    return cleared

def restart_mcp_server(workspace_root: Path, bot_name: str, bot_location: str) -> dict:
    result = {'status': 'unknown', 'previous_pids': [], 'new_pid': None, 'cache_cleared': False, 'error': None}
    try:
        pids = _find_and_terminate_processes(bot_name, result)
        if result.get('error'):
            return result
        _clear_cache_and_set_status(workspace_root, pids, result)
        return result
    except Exception as e:
        _handle_restart_error(e, result)
        return result

def _find_and_terminate_processes(bot_name: str, result: dict) -> List[int]:
    logger.info(f'Finding {bot_name} MCP server processes...')
    pids = find_mcp_server_processes(bot_name)
    if not pids:
        return []
    logger.info(f'Found {len(pids)} processes: {pids}')
    term_result = terminate_processes(pids, timeout=5)
    result['previous_pids'] = term_result['terminated'] + term_result['killed']
    if term_result['failed']:
        result['error'] = f"Failed to terminate processes: {term_result['failed']}"
    return pids

def _clear_cache_and_set_status(workspace_root: Path, pids: List[int], result: dict) -> None:
    logger.info('Clearing Python bytecode cache...')
    cache_root = workspace_root / 'agile_bot'
    cleared = clear_python_cache(cache_root)
    result['cache_cleared'] = cleared > 0
    logger.info(f'Cleared {cleared} cache directories')
    result['status'] = 'restarted' if pids else 'ready_to_start'
    result['message'] = 'Processes terminated and cache cleared. MCP server will restart automatically.'

def _handle_restart_error(e: Exception, result: dict) -> None:
    logger.error(f'Error during restart: {e}', exc_info=True)
    result['error'] = str(e)
    result['status'] = 'failed'