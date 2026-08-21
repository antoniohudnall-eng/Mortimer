---
name: aocros-verify
description: Self-verification skill - agents verify their own output before marking complete. Prevents "lying about completion" and catches bugs early.
metadata:
  clawdbot:
    emoji: ✅
    triggers:
      - /verify
      - check this
      - verify output
      - self-check
---

# AOCROS Verify Skill

Self-verification protocol. Claude-style verification loops for AOCROS agents.

## The Problem

- 40% of AI-generated code has security vulnerabilities
- Agents often claim completion when things are broken
- Easy to miss bugs until they crash in production

## Verification Protocol

### Phase 1: Build Verification

Before marking complete, agent must:
1. **Syntax Check** - Does the code parse?
2. **Import Check** - All dependencies available?
3. **Logic Check** - Does the flow make sense?
4. **Test Pass** - Run existing tests

### Phase 2: Edge Case Testing

For code/automations:
1. Submit invalid inputs - does it handle gracefully?
2. Test boundary conditions
3. Try edge cases a human would miss
4. Document what was tested

### Phase 3: Visual/Output Check

For UI/content:
1. Take screenshots or samples
2. Verify all sections render
3. Check responsive behavior
4. Validate all links work

## Usage

```
/verify [what was built]
```

Or add to any task:
```
Build X and verify before completion
```

## Output Format

```
=== VERIFICATION REPORT ===

🔍 SYNTAX: [PASS/FAIL]
📦 IMPORTS: [PASS/FAIL]
🔄 LOGIC: [PASS/FAIL]
🧪 TESTS: [PASS/FAIL]

⚡ EDGE CASES TESTED:
- [ ] Invalid input handling
- [ ] Boundary conditions
- [ ] Error paths

📸 OUTPUT VERIFIED:
[Screenshot/result verification]

🚨 ISSUES FOUND:
[If any - must fix before completion]

✅ DEFINITION OF DONE MET
```

## Definition of Done

Before claiming complete:
- [ ] All verification phases passed
- [ ] Zero visible errors
- [ ] Edge cases documented
- [ ] Human can review quickly

## Notes

- "Finished" ≠ "Working"
- Verification takes time but saves more time later
- If verification fails, iterate until it passes
- Always document what was tested
