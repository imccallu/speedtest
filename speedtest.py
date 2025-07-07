import streamlit as st
import requests
from bs4 import BeautifulSoup
import json

st.title("🚀 Quick SEO Audit Tool")

# ---- API Key ----
API_KEY = st.secrets["api_keys"]["pagespeed"]

# ---- Form for URL input + Return key support ----
with st.form("audit_form"):
    url = st.text_input("Enter the URL to check:", "")
    submit = st.form_submit_button("Run Full Audit")

if submit and url:
    # ---- Fix missing http(s) ----
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    st.subheader("📱 Mobile Performance")
    with st.spinner("Running Mobile PageSpeed Insights..."):
        mobile_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&key={API_KEY}"
        mobile_response = requests.get(mobile_url)

        if mobile_response.status_code == 200:
            m_data = mobile_response.json()
            m_score = m_data['lighthouseResult']['categories']['performance']['score'] * 100
            m_fcp = m_data['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
            m_lcp = m_data['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']
            m_tbt = m_data['lighthouseResult']['audits']['total-blocking-time']['displayValue']

            st.success(f"✅ Mobile PageSpeed Score: **{m_score:.0f} / 100**")
            st.write(f"**First Contentful Paint:** {m_fcp}")
            st.write(f"**Largest Contentful Paint:** {m_lcp}")
            st.write(f"**Total Blocking Time:** {m_tbt}")
        else:
            st.error("❌ Mobile PageSpeed fetch failed.")

    st.subheader("💻 Desktop Performance")
    with st.spinner("Running Desktop PageSpeed Insights..."):
        desktop_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=desktop&key={API_KEY}"
        desktop_response = requests.get(desktop_url)

        if desktop_response.status_code == 200:
            d_data = desktop_response.json()
            d_score = d_data['lighthouseResult']['categories']['performance']['score'] * 100
            d_fcp = d_data['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
            d_lcp = d_data['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']
            d_tbt = d_data['lighthouseResult']['audits']['total-blocking-time']['displayValue']

            st.success(f"✅ Desktop PageSpeed Score: **{d_score:.0f} / 100**")
            st.write(f"**First Contentful Paint:** {d_fcp}")
            st.write(f"**Largest Contentful Paint:** {d_lcp}")
            st.write(f"**Total Blocking Time:** {d_tbt}")
        else:
            st.error("❌ Desktop PageSpeed fetch failed.")

    # ---- 🔎 Schema check ----
    st.subheader("🔎 Schema Markup Detected")
    with st.spinner("Scanning for JSON-LD and Microdata Schema Markup..."):
        try:
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html.parser')
            schemas_found = []

            # ---- JSON-LD ----
            for tag in soup.find_all('script', type='application/ld+json'):
                try:
                    data = json.loads(tag.string)
                    if isinstance(data, list):
                        for item in data:
                            schemas_found.append(item.get('@type', 'Unknown'))
                    else:
                        schemas_found.append(data.get('@type', 'Unknown'))
                except:
                    continue

            # ---- Microdata ----
            microdata_types = []
            for tag in soup.find_all(attrs={"itemscope": True}):
                itemtype = tag.get("itemtype")
                if itemtype:
                    microdata_types.append(itemtype.split("/")[-1])

            # Combine both
            all_schema_types = list(set(schemas_found + microdata_types))

            if all_schema_types:
                st.success("✅ Schema types found:")
                for s in all_schema_types:
                    st.write(f"- {s}")
            else:
                st.warning("⚠️ No JSON-LD or Microdata Schema types found.")

            # 📍 Recommended schemas
            st.subheader("📍 Suggested Schema Markup to Add")
            recommended = [
                "Organization",
                "WebPage",
                "QAPage",
                "Location",
                "Service",
                "Author",
                "BreadcrumbList",
                "Review",
                "ImageObject"
            ]

            missing = [r for r in recommended if r not in all_schema_types]

            if missing:
                st.warning("👉 **Recommended to add:**")
                for m in missing:
                    st.write(f"- {m}")
            else:
                st.success("🎉 Great job! Your site has all the recommended schema types.")

        except Exception as e:
            st.error(f"❌ Error fetching schema: {e}")

    st.info("""
    **Why This Matters:**  
    ✅ **PageSpeed**: Higher scores help rankings & boost conversions.  
    ✅ **Schema**: Better markup means richer search results (stars, breadcrumbs, FAQs) — driving more qualified traffic.
    """)
