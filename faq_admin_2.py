import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv
import uuid

# 1. 설정 및 DB 연결
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# --- 사이드바 메뉴 구성 ---
st.sidebar.title("🚀 통합 관리 센터")
menu = st.sidebar.radio("이동할 메뉴", ["❓ FAQ 관리", "🍔 메뉴 관리", "📢 공지사항 설정"])

# --- 1. FAQ 관리 메뉴 (등록/수정/삭제 통합) ---
if menu == "❓ FAQ 관리":
    st.title("🛡️ FAQ 관리 시스템")
    
    # [탭 구성] 등록과 수정을 깔끔하게 분리
    tab1, tab2 = st.tabs(["➕ 새 FAQ 등록", "📝 기존 FAQ 수정/삭제"])

    # --- 탭 1: 새 FAQ 등록 ---
    with tab1:
        with st.form("faq_insert_form"):
            q = st.text_input("질문 내용")
            a = st.text_area("답변 내용")
            cat = st.selectbox("카테고리 선택", ["이용안내", "결제", "취소/환불"], key="add_cat")
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
                    "category": cat,
                    "image_url": img_url
                }).execute()
                st.success("✅ 성공적으로 등록되었습니다!")
                st.rerun()

    # --- 탭 2: 기존 FAQ 수정 및 삭제 ---
    with tab2:
        try:
            # 전체 FAQ 데이터 가져오기
            response = supabase.table("faqs").select("*").order("id", desc=True).execute()
            faq_list = response.data

            if faq_list:
                # 1. 수정을 위한 질문 선택
                titles = [f"[{item.get('category', '일반')}] {item['question']}" for item in faq_list]
                selected_title = st.selectbox("수정 또는 삭제할 FAQ를 선택하세요", titles)
                
                # 선택된 항목 찾기
                selected_item = faq_list[titles.index(selected_title)]
                
                st.divider()
                
                # 2. 수정 양식
                with st.form("faq_edit_form"):
                    st.subheader("📝 내용 수정")
                    new_q = st.text_input("질문 수정", value=selected_item['question'])
                    new_a = st.text_area("답변 수정", value=selected_item['answer'])
                    new_cat = st.selectbox("카테고리 수정", ["이용안내", "결제", "취소/환불"], 
                                         index=["이용안내", "결제", "취소/환불"].index(selected_item.get('category', '이용안내')))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        update_btn = st.form_submit_button("💾 변경사항 저장")
                    with col2:
                        delete_btn = st.form_submit_button("🗑️ 이 FAQ 삭제", type="primary")

                    if update_btn:
                        supabase.table("faqs").update({
                            "question": new_q,
                            "answer": new_a,
                            "category": new_cat
                        }).eq("id", selected_item['id']).execute()
                        st.success("✅ 수정 완료!")
                        st.rerun()

                    if delete_btn:
                        supabase.table("faqs").delete().eq("id", selected_item['id']).execute()
                        st.warning("🗑️ 삭제되었습니다.")
                        st.rerun()
                
                # 이미지 미리보기 (있는 경우)
                if selected_item.get('image_url'):
                    st.image(selected_item['image_url'], caption="현재 등록된 이미지", width=300)
            else:
                st.info("등록된 FAQ가 없습니다.")
        except Exception as e:
            st.error(f"오류 발생: {e}")

# --- 2. 메뉴 관리 ---
elif menu == "🍔 메뉴 관리":
    st.title("🍔 상품/메뉴 관리")
    st.info("준비 중인 기능입니다. FAQ와 동일한 방식으로 테이블을 연동하세요.")
    
    with st.expander("✨ 새 상품 등록", expanded=False):
        with st.form("menu_form"):
            item_name = st.text_input("상품명")
            item_price = st.number_input("가격", min_value=0, step=100)
            is_soldout = st.checkbox("품절 여부")
            if st.form_submit_button("상품 등록"):
                st.success(f"'{item_name}' 상품이 등록되었습니다. (DB 연동 필요)")

# --- 3. 공지사항 설정 ---
elif menu == "📢 공지사항 설정":
    st.title("📢 키오스크 공지사항")
    
    with st.container(border=True):
        notice_text = st.text_area("공지 내용", placeholder="예: 현재 시스템 점검 중입니다.")
        show_notice = st.toggle("키오스크에 공지사항 노출")
        
        if st.button("설정 저장"):
            # 여기에 실제 DB 저장 로직을 추가할 수 있습니다.
            st.success("✅ 공지사항 설정이 저장되었습니다.")