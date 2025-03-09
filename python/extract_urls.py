import re
import requests
import streamlit as st

st.set_page_config(page_title="Web Page URL Extractor", layout="wide")

st.title("🔗 Web Page URL Extractor")
st.write("Enter a website URL to extract all links from the page source.")

with st.form("url_form"):
    url = st.text_input("Enter Website URL", "")
    submit_button = st.form_submit_button("Extract URLs")

if submit_button:
    if url.startswith("www"):
        url = "https://" + url
    elif not url.startswith("www") or not url.startswith("http"):
        url = "https://www." + url
    
    st.info("Fetching URLs, please wait...")

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        urls = sorted(set(re.findall(r'https?://[^\s"\'<>]+', response.text)))

        if urls:
            st.success(f"✅ Found {len(urls)} URLs:")
            for link in urls:
                st.markdown(f"- [{link}]({link})")  # Clickable links
        else:
            st.warning("⚠️ No URLs found.")

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Error fetching URL. Is the URL correctly formatted?")
        st.error(f"Error details: {e}")