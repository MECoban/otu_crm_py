import streamlit as st
import requests
from datetime import datetime

# Sayfa yapılandırması
st.set_page_config(
    page_title="MultiERP Dashboard",
    page_icon="🏢",
    layout="wide"
)

# Token kontrolü
if "token" not in st.session_state:
    st.warning("Lütfen önce giriş yapın!")
    st.stop()

# API istekleri için header
headers = {
    "Authorization": f"Bearer {st.session_state['token']}"
}

# Başlık ve açıklama
st.title("MultiERP Dashboard")
st.markdown("""
Bu dashboard üzerinden organizasyonunuzu ve şirketlerinizi yönetebilirsiniz.
""")

# Sidebar menüsü
with st.sidebar:
    st.title("Navigasyon")
    selected_page = st.radio(
        "Sayfa Seçin:",
        ["Dashboard", "Organizasyonlar", "Şirketler", "Kullanıcılar", "Müşteriler"]
    )
    
    if st.button("Çıkış Yap"):
        del st.session_state["token"]
        st.experimental_rerun()

# Kullanıcı verilerini getir
try:
    users_response = requests.get(
        "http://localhost:8000/api/v1/users/",
        headers=headers
    )
    if users_response.status_code == 200:
        users = users_response.json()
        total_users = len(users)
    else:
        total_users = 0
except:
    total_users = 0

# Ana içerik
if selected_page == "Dashboard":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Toplam Organizasyon", value="0")
    
    with col2:
        st.metric(label="Toplam Şirket", value="0")
    
    with col3:
        st.metric(label="Toplam Kullanıcı", value=total_users)

elif selected_page == "Organizasyonlar":
    st.header("Organizasyonlar")
    st.info("Backend bağlantısı henüz kurulmadı. Yakında burada organizasyonlarınızı görebileceksiniz.")

elif selected_page == "Şirketler":
    st.header("Şirketler")
    st.info("Backend bağlantısı henüz kurulmadı. Yakında burada şirketlerinizi görebileceksiniz.")

elif selected_page == "Kullanıcılar":
    st.header("Kullanıcılar")
    try:
        response = requests.get(
            "http://localhost:8000/api/v1/users/",
            headers=headers
        )
        if response.status_code == 200:
            users = response.json()
            for user in users:
                with st.expander(f"{user['first_name']} {user['last_name']}"):
                    st.write(f"Email: {user['email']}")
                    st.write(f"Rol: {user['role']}")
                    st.write(f"Durum: {'Aktif' if user['is_active'] else 'Pasif'}")
        else:
            st.error("Kullanıcı verileri alınamadı.")
    except Exception as e:
        st.error(f"Bağlantı hatası: {str(e)}")

elif selected_page == "Müşteriler":
    st.header("Müşteriler")
    st.info("Backend bağlantısı henüz kurulmadı. Yakında burada müşterilerinizi görebileceksiniz.") 