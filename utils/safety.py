def add_safety_note(response: str) -> str:
    note = "\n\n⚠️ 重要提醒：本系统仅供学习和参考，不替代专业医师诊断和治疗。请务必咨询合格中医师后使用。"
    return response + note