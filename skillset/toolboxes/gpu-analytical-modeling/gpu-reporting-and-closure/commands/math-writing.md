# Math Writing

## Workflow

When writing model equations, execute the following steps in order.

1. **Choose concise symbols**. Use symbols such as `T`, `B`, `N`, `d`, `u`, `c`, `P`, or locally meaningful variants instead of long code variable names.
2. **Define notation near use**. Explain each symbol when it first appears in the surrounding paragraph or table.
3. **Keep units explicit**. State cycles, seconds, bytes, transactions, elements, operations, warps, SMs, or counters as appropriate.
4. **Separate code identifiers from math**. Use code names only when naming implementation fields, files, or APIs.
5. **Check fit and readability**. Split long max expressions, tables, or metric names so they do not overflow the intended document format.

If the user's task does not map cleanly to these steps, use your native planning tool to build a math-writing plan from the formulas, notation, units, and target document constraints, then execute the plan. If mathematical notation would hide an important implementation detail, state the symbol and then name the implementation field separately.

## Good Shape

Use compact formulas such as `\hat{c} = \arg\max_{u \in U} T_u`, then define `U`, `T_u`, and `\hat{c}` near the equation.

## Common Mistakes

- Writing `predicted_saturated_component` inside a formula instead of a mathematical symbol.
- Defining all notation far away from the equation that uses it.
- Removing units while making notation shorter.
