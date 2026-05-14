import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv
import uuid

# 설정 및 DB 연결
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# --- 2. 관리자 로그인 로직 추가 ---
def check_password():
    """로그인 성공 시 True를 반환합니다."""
    def password_entered():
        # 입력된 비밀번호가 설정한 값과 일치하는지 확인
        if st.session_state["username"] == "admin" and st.session_state["password"] == "1234": # 비밀번호를 원하는 대로 바꾸세요!
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # 보안을 위해 세션에서 비밀번호 삭제
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # 로그인 폼 화면
        st.title("🔐 관리자 인증")
        st.text_input("아이디", key="username")
        st.text_input("비밀번호", type="password", key="password")
        st.button("로그인", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        # 로그인 실패 시
        st.title("🔐 관리자 인증")
        st.text_input("아이디", key="username")
        st.text_input("비밀번호", type="password", key="password")
        st.button("로그인", on_click=password_entered)
        st.error("😕 사용자 아이디 또는 비밀번호가 틀렸습니다.")
        return False
    else:
        # 인증 성공
        return True

# 로그인 체크 실행
if check_password():
    # --- 로그인 성공 시에만 아래의 기존 관리자 페이지 코드가 실행됩니다 ---
    
    # 로그아웃 버튼 (선택 사항)
    if st.sidebar.button("로그아웃"):
        del st.session_state["password_correct"]
        st.rerun()

    # --- 사이드바 메뉴 구성 ---
    st.sidebar.title("🚀 통합 관리 센터")
    menu = st.sidebar.radio("관리 설정", ["❓ FAQ 관리", "🍔 메뉴 관리", "📢 공지사항 설정"])

    # --- 1. FAQ 관리 메뉴 (등록/수정/삭제 통합) ---
    if menu == "❓ FAQ 관리":
        st.title("❓FAQ 관리 시스템")
        
        # [탭 구성] 등록과 수정을 분리
        tab1, tab2 = st.tabs(["➕ 새 FAQ 등록", "📝 기존 FAQ 수정/삭제"])

        # --- 새 FAQ 등록 ---
        with tab1:
            with st.form("faq_insert_form"):
                q = st.text_input("질문 내용")
                a = st.text_area("답변 내용")
                cat = st.selectbox("카테고리 선택", ["💳 카드 / 결제", "🥤 이용방법", "📱 쿠폰 / 바코드", "🎆진행중인 행사", "🗨️기타"], key="add_cat")
                img = st.file_uploader("이미지 첨부 (선택)", type=['jpg', 'png', 'jpeg'])
                submit = st.form_submit_button("DB에 저장하기", use_container_width=True)

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

        # --- 기존 FAQ 수정 및 삭제 ---
        with tab2:
            try:
                response = supabase.table("faqs").select("*").order("id", desc=True).execute()
                faq_list = response.data

                if faq_list:
                    # 수정할 질문 선택
                    titles = [f"[{item.get('category') or '미지정'}] {item['question']}" for item in faq_list]
                    selected_title = st.selectbox("수정 또는 삭제할 FAQ를 선택하세요", titles)

                    selected_item = faq_list[titles.index(selected_title)]
                    
                    st.divider()
                    
                    # 수정 양식
                    with st.form("faq_edit_form"):
                        # 제목 줄 구성: 제목 + 삭제 버튼(오른쪽)
                        header_col1, header_col2 = st.columns([5, 1.4]) 
                        with header_col1:
                            st.subheader("📝 내용 수정")
                        with header_col2:
                            # 삭제 버튼을 제목 옆 오른쪽 끝으로 배치
                            delete_btn = st.form_submit_button("🗑️ 이 FAQ 삭제", type="primary")

                        new_q = st.text_input("질문 수정", value=selected_item['question'])
                        new_a = st.text_area("답변 수정", value=selected_item['answer'])
                        
                        current_cat = selected_item.get('category') or '이용안내'
                        cat_options = ["💳 카드 / 결제", "🥤 이용방법", "📱 쿠폰 / 바코드", "🎆진행중인 행사", "🗨️기타"]
                        default_idx = cat_options.index(current_cat) if current_cat in cat_options else 0
                        new_cat = st.selectbox("카테고리 수정", cat_options, index=default_idx)
                        
                        st.write("") # 간격 조절용
                        
                        # 하단 버튼 구성: 가운데 길게
                        update_btn = st.form_submit_button("💾 변경사항 저장", use_container_width=True)

                        # 로직 처리
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