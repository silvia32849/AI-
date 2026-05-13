import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv
import uuid

# 1. 설정 로드
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# --- 사이드바 메뉴 구성 ---
st.sidebar.title("🚀 키오스크 관리 센터")
menu = st.sidebar.radio("이동할 메뉴", ["❓ FAQ 관리", "🍔 메뉴 관리", "📢 공지사항 설정"])

# --- 1. FAQ 관리 메뉴 ---
if menu == "❓ FAQ 관리":
    st.title("🛡️ FAQ 관리 시스템")
    
    with st.expander("➕ 새 FAQ 등록하기", expanded=True):
        with st.form("faq_form"):
            q = st.text_input("질문 내용")
            a = st.text_area("답변 내용")
            img = st.file_uploader("이미지 첨부 (선택)", type=['jpg', 'png', 'jpeg'])
            submit = st.form_submit_button("DB에 저장하기")

            if submit:
                img_url = None
                if img:
                    file_name = f"faq_{uuid.uuid4()}.png"
                    supabase.storage.from_("images").upload(file_name, img.getvalue())
                    img_url = supabase.storage.from_("images").get_public_url(file_name)
                
                supabase.table("faqs").insert({
                    "question": q, 
                    "answer": a, 
                    "image_url": img_url
                }).execute()
                st.success("성공적으로 등록되었습니다!")

    st.divider()
    st.subheader("📋 현재 등록된 FAQ 목록")
    try:
        faqs = supabase.table("faqs").select("*").order("id", desc=True).execute().data
        for f in faqs:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**Q: {f['question']}**")
                if f['image_url']:
                    st.image(f['image_url'], width=200)
            with col2:
                if st.button("삭제", key=f"del_{f['id']}"):
                    supabase.table("faqs").delete().eq("id", f['id']).execute()
                    st.rerun()
    except Exception as e:
        st.info("아직 등록된 FAQ가 없거나 테이블 설정을 확인해주세요.")

# --- 2. 메뉴 관리 (간이 버전) ---
elif menu == "🍔 메뉴 관리":
    st.title("🍔 상품/메뉴 관리")
    st.write("키오스크에 표시될 상품 정보를 관리합니다.")
    
    with st.expander("✨ 새 상품 등록", expanded=False):
        with st.form("menu_form"):
            item_name = st.text_input("상품명")
            item_price = st.number_input("가격", min_value=0, step=100)
            is_soldout = st.checkbox("품절 여부")
            m_submit = st.form_submit_button("상품 등록")
            
            if m_submit:
                st.info("여기에 DB 저장 코드를 추가할 수 있습니다. (테이블 생성 필요)")

    st.info("FAQ와 동일한 방식으로 테이블을 만들어 데이터를 쌓으면 됩니다.")

# --- 3. 공지사항 설정 ---
elif menu == "📢 공지사항 설정":
    st.title("📢 키오스크 공지사항")
    
    notice_text = st.text_area("공지 내용", placeholder="예: 현재 시스템 점검 중입니다.")
    show_notice = st.toggle("키오스크에 공지사항 노출")
    
    if st.button("설정 저장"):
        st.success("공지사항 설정이 저장되었습니다.")
        