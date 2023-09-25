import requests
import streamlit as st

# https://discuss.streamlit.io/t/version-0-64-0-deprecation-warning-for-st-file-uploader-decoding/4465
st.set_option("deprecation.showfileUploaderEncoding", False)

st.title("Summarizer app for Youtube video")

text_input = st.text_input(
    label="Please enter Youtube link",
    placeholder="https://www.youtube.com/watch?v=zUES9s-yNl8",
    value="https://www.youtube.com/watch?v=q9ifYJJHSbU",
)

if st.button("Get summary"):
    if not text_input:
        st.error("You should add link for video", icon="🚨")

    res = requests.post(f"http://web:8000/summaries/", json={"url": text_input})
    id_summary = res.json()["id"]
    summary = requests.get(f"http://web:8000/summaries/{id_summary}")
    if summary:
        mark_summary = summary.json()["summary"]
        st.divider()
        st.success("Done!")
        st.markdown(mark_summary)
    else:
        st.warning("There are not subtitles. Sorry.", icon="⚠️")
