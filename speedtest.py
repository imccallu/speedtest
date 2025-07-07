import streamlit as st
import requests

st.title("🚀 Page Performace Checker")

# ---- API Key ----
API_KEY = st.secrets["api_keys"]["pagespeed"]

# ---- URL Input ----
url = st.text_input("Enter the URL to check:", "")

if st.button("Run PageSpeed Audit") and url:
    if not url.startswith("http"):
        st.error("❌ Please enter a valid URL starting with http or https.")
    else:
        # run the API call...
    with st.spinner("Running PageSpeed Insights..."):
        api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&key={API_KEY}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()

            score = data['lighthouseResult']['categories']['performance']['score'] * 100
            fcp = data['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
            lcp = data['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']
            tbt = data['lighthouseResult']['audits']['total-blocking-time']['displayValue']

            st.success(f"✅ Mobile PageSpeed Score: **{score} / 100**")
            st.write(f"**First Contentful Paint:** {fcp}")
            st.write(f"**Largest Contentful Paint:** {lcp}")
            st.write(f"**Total Blocking Time:** {tbt}")

            st.info("""
            **Why This Matters:**  
            Slow pages rank lower on Google and frustrate users — improving your score can boost rankings, engagement, and qualified calls.
            """)
        else:
            st.error("Failed to fetch PageSpeed data. Check your API key or try again later.")

