from flask import Flask, render_template_string, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# 1. 서영님의 Supabase 정보
url = "https://yjtnvcydrrxjoitjqtzg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlqdG52Y3lkcnJ4am9pdGpxdHpnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg2MjA1NDAsImV4cCI6MjA5NDE5NjU0MH0.9WXlEv82kg48PmDJudJ_DW0X5C5eqDR771ZXxj8zb6s"
supabase: Client = create_client(url, key)

@app.route('/')
def index():
    # 2. 데이터 가져오기
    response = supabase.table("faqs").select("*").execute()
    faqs = response.data

    # 3. 전체에서 조회수 높은 TOP 3 뽑기 (초기 로딩용)
    top_3_faqs = sorted(faqs, key=lambda x: x.get('click_count', 0), reverse=True)[:3]

    # 4. 카테고리 순서 정의
    category_order = ["💳 카드 / 결제", "📱 쿠폰 / 바코드", "🥤 이용방법", "기타"]
    grouped_faqs = {cat: [] for cat in category_order}
    
    for item in faqs:
        cat = item.get('category', '기타')
        if cat not in grouped_faqs:
            grouped_faqs[cat] = []
        grouped_faqs[cat].append(item)

    # 5. 각 카테고리 내부 정렬 및 1등 질문 표시
    for cat in grouped_faqs:
        if grouped_faqs[cat]:
            grouped_faqs[cat].sort(key=lambda x: x.get('click_count', 0), reverse=True)
            grouped_faqs[cat][0]['top_in_category'] = True

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>키오스크 도움말 센터</title>
        <style>
            /* 전체 배경 및 기본 텍스트 블랙(#000000) 세팅 */
            body { font-family: 'Malgun Gothic', sans-serif; display: flex; justify-content: center; background-color: #f8f9fa; padding: 50px 0; color: #000000; }
            .faq-container { width: 480px; }
            
            /* 메인 박스는 순백색(#FFFFFF) */
            .faq-box { background: #FFFFFF; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); }
            
            .top3-section { margin-bottom: 25px; }
            /* 인기 질문 타이틀은 선배님의 딥그린(#00754a) */
            .top3-title { font-size: 16px; font-weight: bold; color: #00754a; margin-bottom: 12px; display: flex; align-items: center; }
            .top3-card-container { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 5px; }
            
            /* TOP 3 카드는 연한 민트그린(#d4e9e2) 배경으로 은은하고 세련되게! */
            .top3-card { 
                min-width: 130px; max-width: 140px; background: #d4e9e2; border: 1px solid #b2dfdb; padding: 12px; 
                border-radius: 12px; font-size: 13px; font-weight: bold; cursor: pointer; transition: 0.3s ease;
                color: #000000; word-break: break-all; white-space: normal; line-height: 1.4;
            }
            .top3-card:hover { transform: translateY(-3px); box-shadow: 0 5px 12px rgba(0,117,74,0.15); }
            .top3-rank { color: #00754a; font-size: 11px; margin-bottom: 4px; display: block; }

            /* 카테고리 그룹 테두리와 타이틀 바를 선배님의 메인 딥그린(#00754a)으로 깔끔하게 매칭 */
            .category-group { margin-bottom: 15px; border: 2px solid #00754a; border-radius: 12px; overflow: hidden; background: #FFFFFF; }
            .category-group > summary { padding: 15px; background: #00754a; color: #FFFFFF; font-size: 17px; font-weight: bold; cursor: pointer; list-style: none; }
            
            .question-item { border-top: 1px solid #eef2f0; background: #FFFFFF; }
            .question-item summary { padding: 12px; font-size: 14px; font-weight: bold; color: #000000; cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; }
            
            .answer { padding: 14px 15px; background: #fafdff; color: #333333; font-size: 13px; line-height: 1.6; border-top: 1px dashed #e0e0e0; }
            .answer-img { max-width: 100%; height: auto; margin-top: 10px; border-radius: 8px; display: block; border: 1px solid #e0e0e0; }
            
            /* 인기 1위 뱃지도 딥그린(#00754a) 베이스로 톤앤매너 통일 */
            .hot-badge { background: #00754a; color: #FFFFFF; font-size: 10px; padding: 2px 7px; border-radius: 8px; font-weight: bold; }

            .modal-overlay {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0, 0, 0, 0.4); display: flex; justify-content: center; align-items: center; z-index: 1000;
            }
            .modal-content {
                background: #FFFFFF; width: 360px; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                text-align: center; animation: fadeIn 0.2s ease-out;
            }
            /* 모달 헤더 텍스트 딥그린(#00754a) */
            .modal-header { font-size: 16px; font-weight: bold; color: #00754a; margin-bottom: 15px; text-align: left; }
            .modal-body { font-size: 14px; color: #000000; line-height: 1.6; margin-bottom: 20px; text-align: left; background: #fdfdfd; padding: 15px; border-radius: 12px; border: 1px solid #eee; }
            
            .modal-img { max-width: 100%; height: auto; margin-top: 10px; border-radius: 10px; border: 1px solid #ddd; display: none; }
            
            /* 확인 버튼을 시그니처 딥그린(#00754a)으로 강조 */
            .modal-close-btn { background: #00754a; color: #FFFFFF; border: none; padding: 11px 30px; font-size: 14px; font-weight: bold; border-radius: 10px; cursor: pointer; transition: 0.2s; width: 100%; }
            .modal-close-btn:hover { background: #005938; }

            @keyframes fadeIn {
                from { opacity: 0; transform: scale(0.95); }
                to { opacity: 1; transform: scale(1); }
            }
        </style>
    </head>
    <body>
        <div class="faq-container">
            <div class="faq-box">
                <h2 style="text-align: center; color: #000000; margin-bottom: 25px; font-weight: 800;">도움말 센터</h2>

                <div class="top3-section">
                    <div class="top3-title">🔥 실시간 인기 질문</div>
                    <div id="top3-container" class="top3-card-container">
                        {% for item in top_3 %}
                        <div class="top3-card" id="top3-card-{{ item.id }}" onclick="openModal({{ item.question|tojson|safe }}, {{ item.answer|tojson|safe }}, '{{ item.id }}', {{ item.image_url|tojson|safe }})" data-faq-id="{{ item.id }}">
                            <span class="top3-rank">TOP {{ loop.index }}</span>
                            <span class="top3-text">{{ item.question }}</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>

                <hr style="border: 0; border-top: 1px solid #eee; margin-bottom: 25px;">

                {% for category, items in final_data.items() %}
                {% if items %}
                <details class="category-group" data-category-group="{{ category }}">
                    <summary>{{ category }}</summary>
                    {% for item in items %}
                    <details class="question-item" id="faq-item-{{ item.id }}" data-faq-id="{{ item.id }}" data-question-text="{{ item.question }}" data-answer-text="{{ item.answer }}" data-image-url="{{ item.image_url if item.image_url else '' }}" ontoggle="if(this.open) triggerClick('{{ item.id }}')">
                        <summary>
                            <span class="q-text">{{ item.question }}</span>
                            <span class="badge-container">
                                {% if item.top_in_category %}
                                <span class="hot-badge">🏆 인기 1위</span>
                                {% endif %}
                            </span>
                        </summary>
                        <div class="answer">
                            {{ item.answer }}
                            
                            {% if item.image_url %}
                            <img src="{{ item.image_url }}" class="answer-img" alt="도움말 이미지">
                            {% endif %}
                            
                            <div style="font-size: 11px; color: #999; margin-top: 8px;">
                                조회수: <span id="count-{{ item.id }}" class="click-number">{{ item.click_count }}</span>
                            </div>
                        </div>
                    </details>
                    {% endfor %}
                </details>
                {% endif %}
                {% endfor %}
            </div>
        </div>

        <div id="custom-modal" class="modal-overlay" style="display: none;">
            <div class="modal-content">
                <div id="modal-title" class="modal-header">💡 질문 내용</div>
                <div id="modal-body" class="modal-body">답변 내용</div>
                
                <img id="modal-image" class="modal-img" src="" alt="도움말 이미지">
                <div style="margin-bottom: 20px;"></div>
                
                <button class="modal-close-btn" onclick="closeModal()">확인</button>
            </div>
        </div>

        <script>
            // [카드 배경 리셋용 색상 상수 정의]
            const MINT_BG = "#d4e9e2";

            function triggerClick(id) {
                fetch('/update_click', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({id: id})
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === "success") {
                        let target = document.getElementById('count-' + id);
                        if (target) {
                            target.textContent = data.new_count;
                            updateCategoryBadges();
                            updateTop3Cards();
                        }
                    }
                })
                .catch(err => console.error("조회수 업데이트 실패:", err));
            }

            function updateCategoryBadges() {
                const groups = document.querySelectorAll('.category-group');
                groups.forEach(group => {
                    const items = group.querySelectorAll('.question-item');
                    let maxCount = -1;
                    let topItem = null;

                    items.forEach(item => {
                        const id = item.getAttribute('data-faq-id');
                        const countEl = document.getElementById('count-' + id);
                        if (countEl) {
                            const count = parseInt(countEl.textContent.trim(), 10) || 0;
                            if (count > maxCount) {
                                maxCount = count;
                                topItem = item;
                            }
                        }
                    });

                    items.forEach(item => {
                        const badgeContainer = item.querySelector('.badge-container');
                        if (badgeContainer) badgeContainer.innerHTML = '';
                    });

                    if (topItem && maxCount > 0) {
                        const badgeContainer = topItem.querySelector('.badge-container');
                        if (badgeContainer) {
                            badgeContainer.innerHTML = '<span class="hot-badge">🏆 인기 1위</span>';
                        }
                    }
                });
            }

            function updateTop3Cards() {
                const allFaqItems = document.querySelectorAll('.question-item');
                let faqList = [];

                allFaqItems.forEach(item => {
                    const id = item.getAttribute('data-faq-id');
                    const question = item.getAttribute('data-question-text');
                    const answer = item.getAttribute('data-answer-text');
                    const imageUrl = item.getAttribute('data-image-url') || '';
                    const countEl = document.getElementById('count-' + id);
                    const count = countEl ? (parseInt(countEl.textContent.trim(), 10) || 0) : 0;
                    
                    faqList.push({ id, question, answer, imageUrl, count });
                });

                faqList.sort((a, b) => b.count - a.count);
                const top3Data = faqList.slice(0, 3);

                const container = document.getElementById('top3-container');
                container.innerHTML = '';

                top3Data.forEach((item, index) => {
                    const safeQuestion = item.question.replace(/'/g, "\\'");
                    const safeAnswer = item.answer.replace(/'/g, "\\'");
                    const safeImageUrl = item.imageUrl.replace(/'/g, "\\'");

                    // 💡 상단 카드 리셋 시 선배님의 연민트 색상(#d4e9e2)이 유지되도록 적용
                    const cardHtml = `
                        <div class="top3-card" style="background: ${MINT_BG};" id="top3-card-${item.id}" onclick="openModal('${safeQuestion}', '${safeAnswer}', '${item.id}', '${safeImageUrl}')" data-faq-id="${item.id}">
                            <span class="top3-rank">TOP ${index + 1}</span>
                            <span class="top3-text">${item.question}</span>
                        </div>
                    `;
                    container.insertAdjacentHTML('beforeend', cardHtml);
                });
            }

            function openModal(question, answer, id, imgUrl) {
                document.getElementById('modal-title').innerText = "💡 " + question;
                document.getElementById('modal-body').innerText = answer;
                
                const modalImg = document.getElementById('modal-image');
                if (imgUrl && imgUrl.trim() !== "" && imgUrl !== "NULL") {
                    modalImg.src = imgUrl;
                    modalImg.style.display = "block";
                } else {
                    modalImg.src = "";
                    modalImg.style.display = "none";
                }
                
                document.getElementById('custom-modal').style.display = 'flex';
                triggerClick(id);
            }

            function closeModal() {
                document.getElementById('custom-modal').style.display = 'none';
            }
        </script>
    </body>
    </html>
    """

    final_data = {cat: grouped_faqs[cat] for cat in category_order if cat in grouped_faqs}
    return render_template_string(html_template, final_data=final_data, top_3=top_3_faqs)

@app.route('/update_click', methods=['POST'])
def update_click():
    data = request.json
    faq_id = data.get('id')
    
    try:
        row = supabase.table("faqs").select("click_count").eq("id", faq_id).single().execute()
        if row.data:
            current_count = row.data.get('click_count', 0)
            new_count = current_count + 1
            supabase.table("faqs").update({"click_count": new_count}).eq("id", faq_id).execute()
            return jsonify({"status": "success", "new_count": new_count})
    except Exception as e:
        print(f"조회수 업데이트 중 오류 발생: {e}")
        
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)