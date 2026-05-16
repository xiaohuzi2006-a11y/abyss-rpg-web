import streamlit as st
import pandas as pd
import numpy as np

# 1. 设置页面配置 (必须在所有 Streamlit 命令的最前面)
st.set_page_config(
    page_title="我的 Streamlit 应用",
    page_icon="🚀",
    layout="wide"
)

# 2. 侧边栏设置
st.sidebar.header("⚙️ 控制面板")
user_name = st.sidebar.text_input("请输入您的名字", "访客")
data_points = st.sidebar.slider("选择要生成的数据点数量", min_value=10, max_value=200, value=50)

# 3. 主页面内容
st.title(f"欢迎来到 Streamlit 的世界, {user_name}! 👋")
st.markdown("""
这是一个用于演示的 Streamlit 基础模板项目。
你可以将这套代码直接推送到 **GitHub**，并通过 [Streamlit Community Cloud](https://streamlit.io/cloud) 实现免费的一键在线部署！
""")

st.divider() # 分割线

# 4. 数据生成与可视化
st.subheader("📊 动态数据可视化")
st.write(f"当前图表正在展示 **{data_points}** 个随机数据点。你可以通过左侧的滑动条实时调整！")

# 使用 numpy 和 pandas 生成模拟数据
@st.cache_data # 使用缓存机制提升加载速度
def generate_data(points):
    return pd.DataFrame(
        np.random.randn(points, 3),
        columns=['产品 A', '产品 B', '产品 C']
    )

chart_data = generate_data(data_points)

# 绘制折线图
st.line_chart(chart_data)

# 5. 交互组件演示
st.divider()
st.subheader("💡 交互测试")
if st.button("点击这里触发惊喜！"):
    st.balloons() # 释放气球动画
    st.success("恭喜！你已经成功运行并交互了这个 Streamlit 应用！")