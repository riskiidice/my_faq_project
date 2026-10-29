def evidence_budget(context_limit: int, used: int, reserve: int) -> int:
    return max(0, context_limit - used - reserve)


def fits_context(context_limit: int, used: int, reserve: int, extra: int) -> bool:
    return used + reserve + extra <= context_limit