import streamlit as st

def calculate_valuation(mrr, growth, churn):
    # 基本計算 (ARR)
    arr = mrr * 12
    
    # マルチプル (倍率) の計算
    multiple = 3.0 # 基本倍率
    
    # 成長率ボーナス
    if growth >= 10:
        multiple += 1.0
    elif growth >= 5:
        multiple += 0.5
        
    # 解約率ペナルティ
    if churn < 5:
        multiple += 0.5
    elif churn >= 20:
        multiple -= 2.0
    elif churn >= 10:
        multiple -= 1.0
        
    # 最低倍率の保証
    if multiple < 0.5:
        multiple = 0.5
        
    valuation = arr * multiple
    return valuation, multiple

# --- 画面表示部分 (UI) ---
st.title("ExitSignal: SaaS Valuation AI 🚀")
st.write("Calculate your SaaS valuation in seconds.\n\nあなたのSaaSサービスの適正売却価格を算出します。")

# 入力フォーム (サイドバー)
st.sidebar.header("Input Metrics")

# 【ここを修正】 ラベルを英語メイン・日本語併記に変更
# 10k JPY = 1万円 という意味です
mrr = st.sidebar.number_input("Monthly MRR (万円 / 10k JPY)", value=50.0, step=10.0)
growth = st.sidebar.slider("Monthly Growth Rate (月次成長率) [%]", 0, 50, 10)
churn = st.sidebar.slider("Churn Rate (解約率) [%]", 0, 30, 5)

# 計算実行
if st.button("Calculate Valuation (価格を診断する)"):
    valuation, multiple = calculate_valuation(mrr, growth, churn)
    
    st.markdown("---")
    st.subheader("Results (診断結果)")
    
    # 通貨計算 (1ドル150円換算)
    USD_JPY_RATE = 150.0
    valuation_usd = (valuation * 10000) / USD_JPY_RATE

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🇯🇵 JPY")
        st.metric(label="Valuation (円)", value=f"{valuation:,.1f} 万円")
    
    with col2:
        st.subheader("🇺🇸 USD")
        st.metric(label="Valuation ($)", value=f"${valuation_usd:,.0f}")

    # マルチプルの表示
    st.metric(label="Multiple (適用マルチプル)", value=f"{multiple}x (ARR)")

    # アドバイス表示 (日英対応)
    if multiple >= 4.0:
        st.success("🦄 Amazing! Investors would kill for this SaaS.\n\n素晴らしい！投資家が殺到するレベルです。")
    elif multiple <= 1.0:
        st.error("⚠️ Warning: Churn is too high or growth is too low.\n\n注意：解約率が高すぎるか、成長率が低すぎます。")
    else:
        st.info("👍 Standard valuation. Lowering churn will increase value.\n\n標準的な価格です。解約率を下げると価値が上がります。")

# サイドバーのフッター
st.sidebar.markdown("---")
st.sidebar.subheader("About Maker 🇯🇵")
st.sidebar.write("Hi! I'm Takumi, a student developer from Japan. I built this in 24h!")

# SNSリンク
if st.sidebar.button("Contact on X (Twitter)"):
    st.sidebar.markdown("[Click here to DM me!](https://twitter.com/)")

st.sidebar.info("🚧 This is an MVP. Feedback is welcome!")
