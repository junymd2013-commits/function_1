import streamlit as st
import random
import sympy as sp
from fractions import Fraction

x = sp.Symbol('x')

# -----------------------------
# 問題生成関数
# -----------------------------

def generate_easy():
    """易しいレベル：定数関数,1次・2次関数の場合"""
    problems = []

    # 1題は定数関数
    C = random.randint(-10, 10)
    f = C
    f_prime = sp.diff(f, x)
    x_val = random.randint(-5, 5)
    problems.append((str(f), x_val, f_prime.subs(x, x_val)))

    # 残り4題は2次関数
    for _ in range(4):
        a = random.randint(1, 5)
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
        f = a*x**2 + b*x + c
        f_prime = sp.diff(f, x)
        x_val = random.randint(-5, 5)
        problems.append((str(f), x_val, f_prime.subs(x, x_val)))

    return problems


def generate_normal():
    """普通レベル：2次・3次関数、係数は整数の場合"""
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
        problems.append((str(f), x_val, f_prime.subs(x, x_val)))

    return problems

def generate_hard():
    """難しいレベル：4次関数1題必須、最高次係数が分数 or マイナスを最大3題。
       すべての問題で f'(x) が整数になるように調整。
    """
    problems = []

    # -------------------------
    # 4次関数1題（分数 or マイナス）
    # -------------------------
    coef_type = random.choice(["fraction", "negative"])
    if coef_type == "fraction":
        p = random.randint(1, 5)
        q = random.randint(2, 6)
        a = Fraction(p, q)
        # x は q の倍数にする
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
    problems.append((format_expr(f), x_val, f_prime.subs(x, x_val)))

    # -------------------------
    # 残り4題
    # -------------------------
    special_count = 1
    for _ in range(4):
        degree = random.choice([2, 3, 4])

        # 最高次係数の種類
        if special_count < 3 and random.random() < 0.5:
            coef_type = random.choice(["fraction", "negative"])
            special_count += 1
        else:
            coef_type = "integer"

        # 係数の決定
        if coef_type == "fraction":
            p = random.randint(1, 5)
            q = random.randint(2, 6)
            a = Fraction(p, q)
            # x は q の倍数にする
            x_val = random.choice([q, -q, 2*q, -2*q])
        elif coef_type == "negative":
            a = -random.randint(1, 5)
            x_val = random.randint(-5, 5)
        else:
            a = random.randint(1, 5)
            x_val = random.randint(-5, 5)

        # 残りの係数は整数
        coeffs = [random.randint(-5, 5) for _ in range(degree)]
        f = a*x**degree
        for i, c in enumerate(coeffs):
            f += c * x**(degree - 1 - i)

        f_prime = sp.diff(f, x)
        problems.append((format_expr(f), x_val, f_prime.subs(x, x_val)))

    return problems


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("微分計算アプリ（難易度3段階・5題セット）")

level = st.selectbox("難易度を選んでください", ["易しい", "普通", "難しい"])

if st.button("問題を生成する"):
    if level == "易しい":
        st.session_state.problems = generate_easy()
    elif level == "普通":
        st.session_state.problems = generate_normal()
    else:
        st.session_state.problems = generate_hard()

if "problems" not in st.session_state:
    st.stop()

problems = st.session_state.problems

st.subheader(f"【{level}レベル：5題】")

user_answers = []
for i, (formula, x_val, correct) in enumerate(problems):
    st.write(f"**第 {i+1} 問： f(x) = {formula}、x = {x_val} のとき f'(x) = ?**")
    ans = st.number_input(f"あなたの解答（第{i+1}問）", key=f"ans_{i}", step=1.0)
    user_answers.append(ans)

if st.button("採点する"):
    score = 0
    st.subheader("【採点結果】")

    for i, (formula, x_val, correct) in enumerate(problems):
        if float(user_answers[i]) == float(correct):
            st.success(f"第 {i+1} 問：正解 → {correct}")
            score += 1
        else:
            st.error(f"第 {i+1} 問：不正解（あなたの答え = {user_answers[i]}、正解 = {correct}）")

    st.write(f"### 合計得点：**{score} / 5**")

    # -------------------------
    # 微分の解説（ここを追加）
    # -------------------------
    st.subheader("【微分の解説】")

    st.markdown("""
### ■ 基本公式
- **(xⁿ)' = n·xⁿ⁻¹**
- **(a·xⁿ)' = a·n·xⁿ⁻¹**
- **和の微分： (f(x) + g(x))' = f'(x) + g'(x)**
- **定数の微分： (C)' = 0**

---

### ■ 2次関数の微分


\[
f(x) = ax^2 + bx + c
\]




\[
f'(x) = 2ax + b
\]



---

### ■ 3次関数の微分


\[
f(x) = ax^3 + bx^2 + cx + d
\]




\[
f'(x) = 3ax^2 + 2bx + c
\]



---

### ■ 4次関数の微分


\[
f(x) = ax^4 + bx^3 + cx^2 + dx + e
\]




\[
f'(x) = 4ax^3 + 3bx^2 + 2cx + d
\]



---

### ■ 例題（一般的な例）


\[
f(x) = 3x^3 - 2x^2 + 5x - 7
\]




\[
f'(x) = 9x^2 - 4x + 5
\]



---

必要なときに見返せるよう、基本公式と典型例をまとめています。
""")
