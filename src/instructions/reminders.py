from typing import Dict, Any, List

def inject_reminder_to_instructions(result: Dict[str, Any], reminder: str) -> Dict[str, Any]:
    instructions = _ensure_instructions_dict(result)
    base_instructions = _get_base_instructions_list(instructions)
    base_instructions.extend(['', '**NEXT BEHAVIOR REMINDER:**', reminder])
    instructions['base_instructions'] = base_instructions
    result['instructions'] = instructions
    return result

def _ensure_instructions_dict(result: Dict[str, Any]) -> Dict[str, Any]:
    if 'instructions' not in result:
        result['instructions'] = {}
    instructions = result['instructions']
    if not isinstance(instructions, dict):
        return {'base_instructions': instructions} if isinstance(instructions, list) else {}
    return instructions

def _get_base_instructions_list(instructions: Dict[str, Any]) -> List[str]:
    base = instructions.get('base_instructions', [])
    return list(base) if isinstance(base, list) else []