# FLL Trajectory Optimizer — Replan (May 2026)

**Goal**: Generate time-optimal, trackable trajectories for LEGO differential-drive robots (FLL).  
**Non-goal**: GUI, web interface, or visual path editor. CLI and raw math only.

---

## Current State Assessment

| Component        | Status  | Pain Point                                                          |
| ---------------- | ------- | ------------------------------------------------------------------- |
| `robot_model.py` | OK      | Parses Choreo config; motor curve physics are fine                  |
| `optimizer.py`   | ✅ DONE | CasADi + IPOPT; sub-second solves, physically feasible trajectories |
| `main.py`        | ✅ DONE | `--accuracy-weight` flag wired to optimizer                         |
| `plotter.py`     | OK      | Diagnostic plots work                                               |
| Output `.traj`   | ✅ DONE | Validated + controller export (`--validate`, `--export-format`)     |

Phase 1 (solver), Phase 2 (accuracy), and Phase 3 (validation/export) are all complete.

---

## Phased Plan

### Phase 1 — Solver Upgrade (CasADi + IPOPT) ✅ DONE

**Priority: Critical** | **Effort: Medium**

Replaced scipy SLSQP with CasADi symbolic NLP + IPOPT.

- **Delivered**:
  - `optimizer.py` rewritten with `casadi.Opti()` + IPOPT, trapezoidal collocation preserved.
  - `robot_model.py` added `max_linear_speed` property; wheel-speed bounds now derived from motor no-load speed instead of an arbitrary `2.0 m/s`.
- **Key fixes discovered during implementation**:
  - The old motor model clamped max force to 0 above no-load speed (~0.88 m/s), yet wheel-speed bounds allowed 2.0 m/s. This created an **infeasible region** that IPOPT correctly rejected (SLSQP silently violated it).
  - IPOPT settings tuned for trajectory NLPs: `tol=1e-2`, `acceptable_tol=1e-1`, `hessian_approximation=limited-memory`, `nlp_scaling_method=gradient-based`.
- **Performance**:
  - 2-waypoint path: **67 ms** (was minutes / non-convergent with SLSQP).
  - 5-waypoint path: **383 ms** with clean convergence.
- **Deliverable**: `optimizer.py` v2 — same CLI contract, solves in **sub-second** time.

### Phase 2 — Time vs. Accuracy Tradeoff ✅ DONE

**Priority: High** | **Effort: Low**

Added tunable smoothness penalty to the objective.

- **Delivered**:
  - `optimizer.py`: `solve()` now accepts `accuracy_weight` parameter.
  - `main.py`: `--accuracy-weight` / `-a` CLI flag (default `0.0`).
  - Penalty: `sum((al_{k+1} - al_k)^2 + (ar_{k+1} - ar_k)^2)` — second-difference on wheel accelerations.
- **Test results** (complex 5-waypoint path, `--samples 10`):

  | accuracy_weight | Total Time      | Max Accel        | Max Jerk         |
  | --------------- | --------------- | ---------------- | ---------------- |
  | 0.0 (pure time) | 6.765 s         | 1.70 m/s²        | 10.63 m/s³       |
  | 1.0 (smooth)    | 6.987 s (+3.3%) | 1.10 m/s² (-35%) | 6.29 m/s³ (-41%) |

- **Deliverable**: `main.py -a 0.5` produces measurably smoother, more trackable trajectories at a modest time cost.

### Phase 3 — Trajectory Validation & Controller Export ✅ DONE

**Priority: High** | **Effort: Medium**

Added validation and controller-ready export.

- **Delivered**:
  - `validator.py`: forward-integration (1 ms RK4), constraint re-audit, metric report, pass/fail verdict.
  - `export.py`: resamples variable-timestep trajectory to fixed `dt`, emits `(t, vl, vr, v, omega, x, y, heading)`.
  - `main.py`: `--validate` flag, `--export-format controller`, `--controller-dt`.
- **Test results** (complex 5-waypoint path):
  - Optimization: **392 ms**
  - Constraint violations: **0**
  - Forward-integration max position error: **5.0 mm**
  - Final position error: **0.8 mm**
  - Exported **339 controller samples** at 20 ms dt.
- **Deliverable**: `main.py --validate --export-format controller --controller-dt 0.02` generates a verified, robot-ready profile.

### Phase 4 — Field Geometry (Optional)

**Priority: Low** | **Effort: High**

Add FLL field obstacle / keep-out constraints.

- **What**: Polygonal no-go zones (walls, mission model keep-out radii) as NLP inequalities.
- **Caveat**: Direct collocation with obstacle constraints is finicky (local minima, infeasible starts). May need a sampling-based front-end (RRT\*) to seed the optimizer.
- **Deliverable**: Only if Phase 1-3 are solid and you actually need it for a specific season.

---

## Architecture Decisions

| Decision                              | Rationale                                                                                                                 |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Keep direct collocation (trapezoidal) | Simple, derivative-free, works with diff-drive kinematics. Hermite-Simpson is a future upgrade if we need fewer nodes.    |
| Keep Choreo-like config format        | Already have parsers; FLL teams may migrate from Choreo.                                                                  |
| No GUI                                | CLI + matplotlib diagnostics is sufficient. A GUI adds zero value to the solver math.                                     |
| Python, not C++                       | Solver time dominates execution; Python overhead is irrelevant. Port to C++ only if deploying optimizer on-robot (never). |

---

## Immediate Next Action

**Phase 4 (field obstacles)** is optional. The core pipeline is complete and ready for FLL use.

---

## Output Roadmap

| Phase | File Changes                                                                 | New Files                   |
| ----- | ---------------------------------------------------------------------------- | --------------------------- |
| 1     | `optimizer.py` (rewrite)                                                     | —                           |
| 2     | `optimizer.py` (add weighted objective), `main.py` (add `--accuracy-weight`) | —                           |
| 3     | `main.py` (add `--export-format`)                                            | `export.py`, `validator.py` |
| 4     | `optimizer.py` (add obstacle constraints)                                    | `field_geometry.py`         |
