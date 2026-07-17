## Summary

<!-- What does this PR change and why? -->

## Type of change

- [ ] Bug fix (pipeline stage failure, wrong output)
- [ ] New compiler family or operator
- [ ] Semantic resolver improvement (alias coverage, schema binding)
- [ ] Plan critic rule addition
- [ ] Contract validator enhancement
- [ ] ConversaBench test case addition
- [ ] Demo script improvement
- [ ] Documentation update

## ConversaBench impact

<!-- If this changes pipeline behaviour, run ConversaBench and document the delta -->

| Metric | Before | After | Delta |
|---|---|---|---|
| Exact match F1 | | | |
| Schema pass rate | | | |
| Contract pass rate | | | |

## Checklist

- [ ] Demo script runs cleanly: `python demo/examples/01_basic_query.py`
- [ ] If adding a compiler family: documented in `docs/Architecture.md` and `docs/ModelCard.md`
- [ ] If changing rejection behaviour: Stage 2 or Stage 5 documented in Architecture.md
- [ ] If new ADR warranted: created in `docs/decisions/`
- [ ] No LLM-generated code executed at runtime (check Stage 4 compilers)
