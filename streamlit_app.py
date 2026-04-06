import streamlit as st
import requests
import time
import json

API = "https://ai-research-assistant-production-9f6e.up.railway.app"

st.set_page_config(page_title="AI Research Assistant")
st.title("AI Research Assistant")

# 登入狀態管理
if "token" not in st.session_state:
    st.session_state.token = None

# 登入介面
if not st.session_state.token:
    st.subheader("歡迎使用 AI Research Assistant")
    
    tab1, tab2 = st.tabs(["登入", "註冊"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("密碼", type="password", key="login_password")
        if st.button("登入", use_container_width=True):
            res = requests.post(f"{API}/auth/login", json={"email": email, "password": password})
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.rerun()
            else:
                st.error("登入失敗，請確認帳號密碼")
    
    with tab2:
        email = st.text_input("Email", key="register_email")
        password = st.text_input("密碼", type="password", key="register_password")
        if st.button("註冊", use_container_width=True):
            res = requests.post(f"{API}/auth/register", json={"email": email, "password": password})
            if res.status_code == 201:
                # 註冊成功自動登入
                login_res = requests.post(f"{API}/auth/login", json={"email": email, "password": password})
                st.session_state.token = login_res.json()["access_token"]
                st.rerun()
            else:
                st.error("註冊失敗，Email 可能已被使用")

# 主介面
else:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("登出"):
            st.session_state.token = None
            st.rerun()

    st.subheader("建立研究任務")
    topic = st.text_input("輸入研究主題", placeholder="例如：人工智慧發展趨勢")
    
    if st.button("開始研究", type="primary"):
        if topic:
            res = requests.post(f"{API}/research/", json={"topic": topic}, headers=headers)
            if res.status_code == 201:
                st.success(f"任務建立成功！任務 ID：{res.json()['id']}，Agent 正在背景執行...")
            else:
                st.error("建立失敗")

    st.divider()
    st.subheader("研究歷史")
    
    if st.button("重新整理"):
        st.rerun()
    
    res = requests.get(f"{API}/research/", headers=headers)
    if res.status_code == 200:
        researches = res.json()
        if not researches:
            st.info("還沒有研究任務")
        running = any(r['status'] in ['pending', 'running'] for r in researches)
        if running:
            st.info("有任務執行中，5 秒後自動重新整理...")
            time.sleep(5)
            st.rerun()
        for r in reversed(researches):
            with st.expander(f"#{r['id']} {r['topic']} — {r['status']}"):
                st.write(f"建立時間：{r['created_at']}")
                if r['status'] == 'completed' and r['result']:
                    report = json.loads(r['result'])
                    st.markdown(f"### {report['title']}")
                    st.markdown(f"**摘要：** {report['summary']}")
                    st.markdown("**重點：**")
                    for point in report['key_points']:
                        st.markdown(f"- {point}")
                    st.markdown(f"**結論：** {report['conclusion']}")
                elif r['status'] == 'running':
                    st.info("Agent 正在執行中...")
                elif r['status'] == 'failed':
                    st.error("執行失敗")