import streamlit as st
import requests

st.title("🚀 Page Performance Checker")

# ---- API Key ----
API_KEY = st.secrets["api_keys"]["pagespeed"]

# ---- URL Input ----
url = st.text_input("Enter the URL to check:", "")

if st.button("Run PageSpeed Audit") and url:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    with st.spinner("Running PageSpeed Insights..."):
        # ---- Mobile ----
        mobile_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&key={API_KEY}"
        mobile_response = requests.get(mobile_url)

        if mobile_response.status_code == 200:
            m_data = mobile_response.json()

            m_score = m_data['lighthouseResult']['categories']['performance']['score'] * 100
            m_fcp = m_data['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
            m_lcp = m_data['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']
            m_tbt = m_data['lighthouseResult']['audits']['total-blocking-time']['displayValue']

            st.header("📱 Mobile Performance")
            st.success(f"✅ Mobile PageSpeed Score: **{m_score} / 100**")
            st.write(f"**First Contentful Paint:** {m_fcp}")
            st.write(f"**Largest Contentful Paint:** {m_lcp}")
            st.write(f"**Total Blocking Time:** {m_tbt}")

        else:
            st.error("Failed to fetch Mobile PageSpeed data.")

        # ---- Desktop ----
        desktop_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=desktop&key={API_KEY}"
        desktop_response = requests.get(desktop_url)

        if desktop_response.status_code == 200:
            d_data = desktop_response.json()

            d_score = d_data['lighthouseResult']['categories']['performance']['score'] * 100
            d_fcp = d_data['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
            d_lcp = d_data['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']
            d_tbt = d_data['lighthouseResult']['audits']['total-blocking-time']['displayValue']

            st.header("💻 Desktop Performance")
            st.success(f"✅ Desktop PageSpeed Score: **{d_score} / 100**")
            st.write(f"**First Contentful Paint:** {d_fcp}")
            st.write(f"**Largest Contentful Paint:** {d_lcp}")
            st.write(f"**Total Blocking Time:** {d_tbt}")

        else:
            st.error("Failed to fetch Desktop PageSpeed data.")

        st.info("""
        **Why This Matters:**  
        Faster pages rank better on Google, keep users engaged longer, and drive more qualified conversions.
        """)
