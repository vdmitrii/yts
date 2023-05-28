from time import sleep

import requests
import streamlit as st
from PIL import Image

# https://discuss.streamlit.io/t/version-0-64-0-deprecation-warning-for-st-file-uploader-decoding/4465
st.set_option("deprecation.showfileUploaderEncoding", False)

st.title("Summarizer app for Youtube video")

text_input = st.text_input(
    label="Please enter Youtube link",
    placeholder="https://www.youtube.com/watch?v=zUES9s-yNl8",
    value="https://www.youtube.com/watch?v=q9ifYJJHSbU",
)
# if text_input:
#     st.write("You entered: ", text_input)

# TODO: add progress bar and popup then success message
if st.button("Get summary"):
    if text_input is not None:  # and style is not None:
        res = requests.post(f"http://web:8000/summaries/", json={"url": text_input})
        id_summary = res.json()["id"]
        summary = requests.get(f"http://web:8000/summaries/{id_summary}")
        # sleep(20)
        mark_summary = summary.json()["summary"]
        # if not summary:
        #     st.write("No summary found")
        st.markdown("""---""")
        st.markdown(mark_summary)
        st.markdown("""---""")


# STYLES = {
#     "read": "candy",
#     "create": "composition_vii",
#     "feathers": "feathers",
#     "la_muse": "la_muse",
#     "mosaic": "mosaic",
#     "starry night": "starry_night",
#     "the scream": "the_scream",
#     "the wave": "the_wave",
#     "udnie": "udnie",
# }

# image = st.file_uploader("Choose an video")

# style = st.selectbox("Choose the style", [i for i in STYLES.keys()])

# if st.button("Style Transfer"):
#     if image is not None and style is not None:
#         files = {"file": image.getvalue()}
#         res = requests.post(f"http://web:8000/{style}", files=files)
#         img_path = res.json()
#         image = Image.open(img_path.get("name"))
#         st.image(image, width=500)
