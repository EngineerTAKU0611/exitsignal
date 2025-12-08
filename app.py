import streamlit as st

def calculate_valuation(mrr, growth, churn):
    # 基本計算 (ARR)
    arr = mrr * 12
    
    # マルチプル（倍率）の計算
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
st.write("あなたのSaaSサービスの適正売却価格を算出します。")

# 入力フォーム（サイドバー）
st.sidebar.header("Input Metrics")
mrr = st.sidebar.number_input("月次売上 (MRR) [万円]", value=50.0, step=10.0)
growth = st.sidebar.slider("月次成長率 (Growth Rate) [%]", 0, 50, 10)
churn = st.sidebar.slider("解約率 (Churn Rate) [%]", 0, 30, 5)

# 計算実行
if st.button("価格を診断する (Calculate)"):
    valuation, multiple = calculate_valuation(mrr, growth, churn)
    
    st.markdown("---")
    st.subheader("診断結果 (Result)")
    
    # 結果を大きく表示
    st.metric(label="推定売却価格 (Valuation)", value=f"{valuation:,.1f} 万円")
    st.metric(label="適用マルチプル (Multiple)", value=f"{multiple}x (ARR比)")
    
    # アドバイス表示
    if multiple >= 4.0:
        st.success("素晴らしい！投資家が殺到するレベルです。")
    elif multiple <= 1.0:
        st.error("注意：解約率が高すぎるか、成長率が低すぎます。")
    else:
        st.info("標準的な価格です。解約率を下げると価値が上がります。")