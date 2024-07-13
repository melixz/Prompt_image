import streamlit as st
import replicate
from typing import Dict, Any

st.markdown("# :red[Prompt and image]")

REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]


def configure_sidebar() -> Dict[str, Any]:
    with st.sidebar:
        with st.form("my_form"):
            width = st.number_input("Ширина картинки", min_value=256, max_value=2048, value=1024)
            height = st.number_input("Высота картинки", min_value=256, max_value=2048, value=1024)
            prompt = st.text_area("Введите промпт:")
            submitted = st.form_submit_button("Отправить", type="primary")

        return {
            "width": width,
            "height": height,
            "prompt": prompt,
            "submitted": submitted,
        }


@st.cache_data
def generate_image(width: int, height: int, prompt: str) -> str:
    try:
        result = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "width": width,
                "height": height,
                "prompt": prompt,
            }
        )
        return result[0]
    except Exception as e:
        st.error(f"Произошла ошибка при генерации изображения: {e}")
        return ""


def main_page(width: int, height: int, prompt: str, submitted: bool):
    if submitted:
        with st.spinner("В процессе загрузки"):
            image_url = generate_image(width, height, prompt)
            if image_url:
                with st.container():
                    st.image(image_url, caption="Ваша картинка")


def main():
    data = configure_sidebar()
    main_page(**data)


if __name__ == "__main__":
    main()
