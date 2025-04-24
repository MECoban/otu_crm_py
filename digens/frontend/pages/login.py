import streamlit as st
import requests
import json

# Sayfa yapılandırması
st.set_page_config(
    page_title="Digens CRM - Giriş",
    page_icon="🔐",
    layout="centered"
)

def login(email: str, password: str) -> bool:
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            # Token'ı session state'e kaydet
            st.session_state["token"] = data["access_token"]
            return True
        return False
    except Exception as e:
        st.error(f"Bağlantı hatası: {str(e)}")
        return False

def main():
    if "token" not in st.session_state:
        st.title("Digens CRM'e Hoş Geldiniz")
        
        with st.form("login_form"):
            email = st.text_input("E-posta")
            password = st.text_input("Şifre", type="password")
            submit = st.form_submit_button("Giriş Yap")
            
            if submit:
                if login(email, password):
                    st.success("Giriş başarılı!")
                    st.experimental_rerun()
                else:
                    st.error("Giriş başarısız. Lütfen bilgilerinizi kontrol edin.")
    else:
        st.success("Zaten giriş yapmışsınız!")
        if st.button("Çıkış Yap"):
            del st.session_state["token"]
            st.experimental_rerun()

if __name__ == "__main__":
    main() 