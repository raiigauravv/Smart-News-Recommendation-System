import streamlit as st
import pandas as pd
import urllib.parse
import random
from nltk.corpus import stopwords

# Try to import transformers, fall back to simple summarization if not available
try:
    from transformers import pipeline
    import torch  # Check if PyTorch is available
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    TRANSFORMERS_AVAILABLE = True
except (ImportError, NameError, OSError) as e:
    print(f"Warning: Transformers not available ({e}). Using fallback summarization.")
    summarizer = None
    TRANSFORMERS_AVAILABLE = False
from utils.recommenders import (
    get_user_recommendations,
    get_article_recommendations,
    get_hybrid_recommendations,
    get_news_metadata,
    get_bert4rec_recommendations,
    get_trending_articles,
    get_user_histories,
    get_unique_articles_df
)
from dotenv import load_dotenv
import os
from utils.pdf_utils import generate_pdf_from_articles

# Load environment variables
load_dotenv()

def generate_summary(title, abstract):
    try:
        if TRANSFORMERS_AVAILABLE and summarizer:
            full_text = f"{title}. {abstract}"
            summary = summarizer(full_text, max_length=60, min_length=15, do_sample=False)
            return summary[0]['summary_text']
        else:
            # Fallback: return first 100 characters of abstract
            if abstract and len(abstract) > 100:
                return abstract[:100] + "..."
            return abstract or "No summary available."
    except Exception as e:
        print("Summarization error:", e)
        # Fallback: return first 100 characters of abstract
        if abstract and len(abstract) > 100:
            return abstract[:100] + "..."
        return abstract or "No summary available."

st.set_page_config(page_title="😮 Smart News Recommender", layout="wide")

# Apply static dark theme only
st.markdown("""
    <style>
    html, body, .main, [class^="css"] {
        background-color: #121212 !important;
        color: #ffffff !important;
    }
    .stSidebar, .css-1d391kg {
        background-color: #1e1e1e !important;
    }
    </style>
""", unsafe_allow_html=True)

# Trigger session state
if "trigger_keyword_search" not in st.session_state:
    st.session_state["trigger_keyword_search"] = False
if "trigger_hybrid_search" not in st.session_state:
    st.session_state["trigger_hybrid_search"] = False

def trigger_keyword_search():
    st.session_state["trigger_keyword_search"] = True

def trigger_hybrid_search():
    st.session_state["trigger_hybrid_search"] = True

# Sidebar – Navigation
st.sidebar.title("🔧 NEWS RECOMMENDER")
view_mode = st.sidebar.radio("Choose a mode", ["🔍 Browse by Keyword", "👤 Personalized (User ID)"])
top_n = st.sidebar.slider("Top N Recommendations", 1, 20, 5)

if view_mode == "👤 Personalized (User ID)":
    use_bert = st.sidebar.checkbox("🧠 Use BERT4Rec model")
    user_id = st.sidebar.text_input("Enter your User ID", value="U13740")
    alpha = st.sidebar.slider("Hybrid Alpha (0 = CF, 1 = CBF)", 0.0, 1.0, 0.0)

st.title("📰 Smart News Recommendation System")

if view_mode == "🔍 Browse by Keyword":
    st.subheader("📚 Explore News by Keyword")
    st.markdown("Try examples: `Sports`, `Travel`, `Finance`, `Health`")
    keyword = st.text_input("Enter a keyword to explore", key="keyword_input", on_change=trigger_keyword_search)

    if st.session_state["trigger_keyword_search"] and keyword:
        recs = get_article_recommendations(keyword, top_k=top_n)

        if not recs:  # Check if list is empty
            st.warning("No articles found for this keyword.")
        else:
            rec_df = []
            for rec in recs:  # Iterate over list directly
                meta = get_news_metadata(rec['NewsID'])
                if meta:
                    rec_df.append(meta)
                    with st.expander(f"📰 {meta['Title']}"):
                        st.markdown(f"**Category:** {meta['Category']} / {meta['SubCategory']}")
                        st.markdown(f"**Abstract:** {meta['Abstract']}")
                        st.markdown("🔒 This article is not publicly accessible.")
                        summary = generate_summary(meta['Title'], meta['Abstract'])
                        st.markdown(f"🧠 **AI Summary:** {summary}")
                        search_query = urllib.parse.quote(str(meta['Title']) if meta['Title'] else "")
                        search_url = f"https://www.bing.com/news/search?q={search_query}"
                        st.markdown(f"[🔍 Search this article on Bing]({search_url})")

            rec_df = pd.DataFrame(rec_df)
            if not rec_df.empty:
                st.download_button("📥 Download Recommendations as CSV", data=rec_df.to_csv(index=False), file_name="keyword_recommendations.csv", mime="text/csv", key="csv_keyword")
                pdf_path = generate_pdf_from_articles(rec_df.to_dict('records'), user_id="guest")
                with open(pdf_path, "rb") as f:
                    st.download_button("📄 Download Recommendations as PDF", data=f, file_name=pdf_path, mime="application/pdf", key="pdf_keyword")

            user_clicked_ids = get_user_histories().get("guest", [])
            clicked_categories = get_unique_articles_df()[get_unique_articles_df()['NewsID'].isin(user_clicked_ids)]['Category'].dropna()
            if not clicked_categories.empty:
                top_cats = clicked_categories.value_counts().head(3).index.tolist()
                st.caption(f"🧠 Based on your history, you're likely interested in: {', '.join(top_cats)}")
            else:
                st.caption("🧠 We couldn't determine strong category preferences yet.")

elif view_mode == "👤 Personalized (User ID)":
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔄 User-Based",
        "⚡ Hybrid",
        "🧪 Keyword + Hybrid",
        "🔥 Daily Trends"
    ])

    with tab1:
        st.subheader("🌟 Personalized Recommendations")
        if user_id:
            recs = get_bert4rec_recommendations(user_id, top_n) if use_bert else get_user_recommendations(user_id, top_n)
            if not recs:
                st.warning("⚠️ User ID not found or has no recommendation history.")
            else:
                for rec in recs:
                    meta = get_news_metadata(rec['NewsID'])
                    if meta:
                        with st.expander(f"📰 {meta['Title']}"):
                            st.markdown(f"**Category:** {meta['Category']} / {meta['SubCategory']}")
                            st.markdown(f"**Abstract:** {meta['Abstract']}")
                            st.markdown("🔒 This article is not publicly accessible.")
                            summary = generate_summary(meta['Title'], meta['Abstract'])
                            st.markdown(f"🧠 **AI Summary:** {summary}")
                            search_query = urllib.parse.quote(meta['Title'])
                            search_url = f"https://www.bing.com/news/search?q={search_query}"
                            st.markdown(f"[🔍 Search this article on Bing]({search_url})")

    with tab2:
        st.subheader("⚡ Hybrid Recommendations (User + Content)")
        if user_id:
            recs = get_hybrid_recommendations(user_id, top_k=top_n)
            if not recs:
                st.warning("⚠️ User ID not found or has no recommendation history.")
            else:
                for rec in recs:
                    meta = get_news_metadata(rec['NewsID'])
                    if meta:
                        with st.expander(f"📰 {meta['Title']}"):
                            st.markdown(f"**Category:** {meta['Category']} / {meta['SubCategory']}")
                            st.markdown(f"**Abstract:** {meta['Abstract']}")
                            st.markdown("🔒 This article is not publicly accessible.")
                            summary = generate_summary(meta['Title'], meta['Abstract'])
                            st.markdown(f"🧠 **AI Summary:** {summary}")
                            search_query = urllib.parse.quote(meta['Title'])
                            search_url = f"https://www.bing.com/news/search?q={search_query}"
                            st.markdown(f"[🔍 Search this article on Bing]({search_url})")

    with tab3:
        st.subheader("🧪 Keyword + Hybrid Recommendations")
        keyword_combo = st.text_input("Enter keyword to blend with personalization", key="hybrid_keyword_input", on_change=trigger_hybrid_search)

        if st.session_state["trigger_hybrid_search"] and keyword_combo and user_id:
            recs_keyword = get_article_recommendations(keyword_combo, top_k=5)

            if recs_keyword:  # Check if list is not empty
                target_news_id = recs_keyword[0]['NewsID']  # Get first result
                st.caption(f"🔗 Blending user history with article: `{target_news_id}` for keyword **{keyword_combo}**")
                recs = get_hybrid_recommendations(user_id, top_k=top_n)

                if not recs:
                    st.warning("⚠️ No hybrid recommendations found for the given user + keyword combo.")
                else:
                    for rec in recs:
                        meta = get_news_metadata(rec['NewsID'])
                        if meta:
                            with st.expander(f"📰 {meta['Title']}"):
                                st.markdown(f"**Category:** {meta['Category']} / {meta['SubCategory']}")
                                st.markdown(f"**Abstract:** {meta['Abstract']}")
                                st.markdown("🔒 This article is not publicly accessible.")
                                summary = generate_summary(meta['Title'], meta['Abstract'])
                                st.markdown(f"🧠 **AI Summary:** {summary}")
                                search_query = urllib.parse.quote(meta['Title'])
                                search_url = f"https://www.bing.com/news/search?q={search_query}"
                                st.markdown(f"[🔍 Search this article on Bing]({search_url})")

    with tab4:
        st.subheader("🔥 Top Trending News Today")
        trending_articles = get_trending_articles(top_k=top_n)

        if trending_articles:
            for article in trending_articles:
                meta = get_news_metadata(article['NewsID'])
                if meta:
                    with st.expander(f"📰 {meta['Title']}"):
                        st.markdown(f"**Category:** {meta['Category']} / {meta['SubCategory']}")
                        st.markdown(f"**Abstract:** {meta['Abstract']}")
                        st.markdown("🔒 This article is not publicly accessible.")
                        summary = generate_summary(meta['Title'], meta['Abstract'])
                        st.markdown(f"🧠 **AI Summary:** {summary}")
                        search_query = urllib.parse.quote(str(meta['Title']) if meta['Title'] else "")
                        search_url = f"https://www.bing.com/news/search?q={search_query}"
                        st.markdown(f"[🔍 Search this article on Bing]({search_url})")
        else:
            st.info("No trending articles found today.")
