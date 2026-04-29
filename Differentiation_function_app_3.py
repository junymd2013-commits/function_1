import streamlit as st
import random
import sympy as sp
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np

x = sp.Symbol('x')

# --------------------------------
# 文字列表記を x^4 形式に統一
# --------------------------------
def format_expr(expr):
    s = str(expr)
    s = s.replace("**", "^")
    return s

# --------------------------------
# 4択の選択肢を作る
# --------------------------------
def make_choices(correct):
    choices = {correct}
    while len(choices) < 4:
        wrong = correct + random.randint(-10, 10)
        if wrong != correct:
            choices.add(wrong)
    choices = list(choices)
    random.shuffle(choices)
    return choices

# --------------------------------
# 易しいレベル
# --------------------------------
def generate_easy():
    problems = []

    # 定数関数1題
    C = random.randint(-10, 10)
    f = C
    f_prime = sp.diff(f, x)
    x_val = random.randint(-5, 5)
    correct = f_prime.subs(x, x_val)
    problems.append((format_expr(f), x_val, correct, make_choices(correct)))

    # 残り4題は2次関数
    for _ in range(4):
        a = random.randint(1, 5)
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
        f = a*x**2 + b*x + c
        f_prime = sp.diff(f, x)
        x_val = random.randint(-5, 5)
        correct = f_prime.subs(x, x_val)
        problems.append((format_expr(f), x_val, correct, make_choices(correct)))

    return problems

# --------------------------------
# 普通レベル
# --------------------------------
def generate_normal():
    problems = []
    for _ in range(5):
        degree = random.choice([2, 3])
        if degree == 2:
            a = random.randint(1, 5)
            b = random.randint(-5, 5)
            c = random.randint(-5, 5)
            f = a*x**2 + b*x + c
        else:
            a = random.randint(1, 3)
            b = random.randint(-5, 5)
            c = random.randint(-5, 5)
            d = random.randint(-5, 5)
            f = a*x**3 + b*x**2 + c*x + d

        f_prime = sp.diff(f, x)
        x_val = random.randint(-5, 5)
        correct = f_prime.subs(x, x_val)
        problems.append((format_expr(f), x_val, correct, make_choices(correct)))

    return problems

# --------------------------------
# 難しいレベル（整数解保証）
# --------------------------------
def generate_hard():
    problems = []

    # 4次関数1題（分数 or マイナス）
    coef_type = random.choice(["fraction", "negative"])
    if coef_type == "fraction":
        p = random.randint(1, 5)
        q = random.randint(2, 6)
        a = Fraction(p, q)
        x_val = random.choice([q, -q, 2*q, -2*q])
    else:
        a = -random.randint(1, 5)
        x_val = random.randint(-5, 5)

    b = random.randint(-5, 5)
    c = random.randint(-5, 5)
    d = random.randint(-5, 5)
    e = random.randint(-5, 5)

    f = a*x**4 + b*x**3 + c*x**2 + d*x + e
    f_prime = sp.diff(f, x)
    correct = f_prime.subs(x, x_val)
    problems.append((format_expr(f), x_val, correct, make_choices(correct)))

    # 残り4題
    special_count = 1
    for _ in range(4):
        degree = random.choice([2, 3, 4])

        if special_count < 3 and random.random() < 0.5:
            coef_type = random.choice(["fraction", "negative"])
            special_count += 1
        else:
            coef_type = "integer"

        if coef_type == "fraction":
            p = random.randint(1, 5)
            q = random.randint(2, 6)
            a = Fraction(p, q)
            x_val = random.choice([q, -q, 2*q, -2*q])
        elif coef_type == "negative":
            a = -random.randint(1, 5)
            x_val = random.randint(-5, 5)
        else:
            a = random.randint(1, 5)
            x_val = random.randint(-5, 5)

        coeffs = [random.randint(-5, 5) for _ in range(degree)]
        f = a*x**degree
        for i, c in enumerate(coeffs):
            f += c * x**(degree - 1 - i)

        f_prime = sp.diff(f, x)
        correct = f_prime.subs(x, x_val)
        problems.append((format_expr(f), x_val, correct, make_choices(correct)))

    return problems

# --------------------------------
# Streamlit UI
# --------------------------------

st.title("微分計算アプリ（難易度3段階・5題セット）")

level = st.radio("難易度を選んでください", ["易しい", "普通", "難しい"])

# 問題生成ボタン
if st.button("問題を生成する"):
    st.session_state.answers = {}     # 解答リセット
    st.session_state.problems = []    # 問題リセット

    if level == "易しい":
        st.session_state.problems = generate_easy()
    elif level == "普通":
        st.session_state.problems = generate_normal()
    else:
        st.session_state.problems = generate_hard()

if "problems" not in st.session_state or not st.session_state.problems:
    st.stop()

problems = st.session_state.problems

st.subheader(f"【{level}レベル：5題】")

# 4択表示（最初は index=None で未選択）
for i, (formula, x_val, correct, choices) in enumerate(problems):
    st.write(f"**第 {i+1} 問： f(x) = {formula}、x = {x_val} のとき f'(x) = ?**")
    st.session_state.answers[i] = st.radio(
        f"あなたの解答（第{i+1}問）",
        choices,
        key=f"q{i}",
        index=None
    )

# --------------------------------
# 採点
# --------------------------------
if st.button("採点する"):
    score = 0
    st.subheader("【採点結果】")

    for i, (formula, x_val, correct, choices) in enumerate(problems):
        user_ans = st.session_state.answers[i]
        if user_ans == correct:
            st.success(f"第 {i+1} 問：正解 → {correct}")
            score += 1
        else:
            st.error(f"第 {i+1} 問：不正解（あなたの答え = {user_ans}、正解 = {correct}）")

    st.write(f"### 合計得点：**{score} / 5**")

    # --------------------------------
    # グラフ表示（f(x), f'(x), 接線）
    # --------------------------------
    st.subheader("Graph: f(x), f'(x), and Tangent Line")

    for i, (formula, x_val, correct, choices) in enumerate(problems):
        st.write(f"### Graph for Question {i+1}")

        # SymPy → 数値関数
        f_expr = sp.sympify(formula.replace("^", "**"))
        f_prime_expr = sp.diff(f_expr, x)

        f_lam = sp.lambdify(x, f_expr, "numpy")
        f_prime_lam = sp.lambdify(x, f_prime_expr, "numpy")

        # グラフ範囲
        X = np.linspace(x_val - 5, x_val + 5, 400)

        Y1 = f_lam(X)
        Y2 = f_prime_lam(X)

        # ★ スカラー対応（定数関数）
        if np.isscalar(Y1):
            Y1 = np.full_like(X, Y1)
        if np.isscalar(Y2):
            Y2 = np.full_like(X, Y2)

        # ★ 接線の式
        f_x0 = f_lam(x_val)
        slope = f_prime_lam(x_val)
        tangent = slope * (X - x_val) + f_x0

        fig, ax = plt.subplots()

        ax.plot(X, Y1, label="f(x)", color="blue")
        ax.plot(X, Y2, label="f'(x)", color="red")
        ax.plot(X, tangent, label="tangent line", color="green")

        ax.axvline(x_val, color="gray", linestyle="--", alpha=0.5)
        ax.scatter([x_val], [f_x0], color="green")

        ax.set_title(f"f(x), f'(x), Tangent (Q{i+1})")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)


    # --------------------------------
    # 微分の解説
    # --------------------------------
    st.subheader("【微分の解説】")
    st.markdown("""
### ■ 基本公式
- (xⁿ)' = n·xⁿ⁻¹  
- (a·xⁿ)' = a·n·xⁿ⁻¹  
- 和の微分： (f(x) + g(x))' = f'(x) + g'(x)  
- 定数の微分： (C)' = 0  

---

### ■ 2次関数


\[
f(x) = ax^2 + bx + c
\]




\[
f'(x) = 2ax + b
\]



### ■ 3次関数


\[
f(x) = ax^3 + bx^2 + cx + d
\]




\[
f'(x) = 3ax^2 + 2bx + c
\]



### ■ 4次関数


\[
f(x) = ax^4 + bx^3 + cx^2 + dx + e
\]




\[
f'(x) = 4ax^3 + 3bx^2 + 2cx + d
\]


""")

    # --------------------------------
    # もう一度・終了ボタン
    # --------------------------------
    if st.button("もう一度"):
        st.session_state.answers = {}
        st.session_state.problems = []
        st.experimental_rerun()

    if st.button("終了"):
        st.session_state.clear()
        st.write("お疲れさまでした。アプリを終了します。")
