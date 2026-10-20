import sympy as sp

def compute_nonlinear(eq_str, x0, tol, method):
    x = sp.Symbol('x')
    expr = sp.sympify(eq_str.replace('^', '**'))
    df = sp.diff(expr, x)
    x_val = float(x0)
    tol = float(tol)
    steps = []

    for n in range(1, 31):
        fx = float(expr.subs(x, x_val))
        dfx = float(df.subs(x, x_val))

        if "Newton" in method:
            if dfx == 0:
                raise ValueError("Derivative is zero! Division by zero error.")
            x_next = x_val - (fx / dfx)
        else:
            x_next = fx

        err = abs(x_next - x_val)
        steps.append((n, round(x_val, 5), round(fx, 5), round(x_next, 5), round(err, 5)))

        if err < tol:
            return steps, f"Result: Root ≈ {x_next:.5f}  (Converged in {n} iterations)"
        x_val = x_next

    return steps, f"Result: Max iterations reached. Approx Root ≈ {x_val:.5f}"


def compute_linear(A, b, tol, method):
    x = [0.0, 0.0, 0.0]
    steps = [(0, 0.0, 0.0, 0.0, "-")]

    for k in range(1, 31):
        x_old = x.copy()
        for i in range(3):
            if A[i][i] == 0:
                raise ValueError("Zero on main diagonal! Cannot divide by zero.")
            vals = x_old if "Jacobi" in method else x
            sigma = sum(A[i][j] * vals[j] for j in range(3) if j != i)
            x[i] = (b[i] - sigma) / A[i][i]

        err = max(abs(x[i] - x_old[i]) for i in range(3))
        steps.append((k, round(x[0], 4), round(x[1], 4), round(x[2], 4), round(err, 5)))

        if err < tol:
            return steps, f"Result: x = {x[0]:.4f},  y = {x[1]:.4f},  z = {x[2]:.4f}  (in {k} iterations)"

    return steps, f"Result: x = {x[0]:.4f},  y = {x[1]:.4f},  z = {x[2]:.4f}  (Max iterations reached)"


def compute_errors(t_val, a_val):
    if t_val == 0:
        raise ValueError("True value cannot be zero.")
    abs_err = abs(t_val - a_val)
    rel_err = abs_err / abs(t_val)
    perc_err = rel_err * 100
    return f"Result: Absolute Error = {abs_err:g}   |   Relative Error = {rel_err:.5f}   |   Percentage Error = {perc_err:.3f} %"