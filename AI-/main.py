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

    # 3. 전체에서 조회수 높은 TOP 3 뽑기
    top_3_faqs = sorted(faqs, key=lambda x: x.get('click_count', 0), reverse=True)[:3]

    # 4. 카테고리 순서 정의
    category_order = ["💳 카드 / 결제", "📱 쿠폰 / 바코드", "🥤 이용방법", "기타"]
    grouped_faqs = {cat: [] for cat in category_order}
    
    for item in faqs:
        cat = item.get('category', '기타')
        if cat not in grouped_faqs:
            grouped_faqs[cat] = []
        grouped_faqs[cat].append(item)

    # 5. 각 카테고리 내부 정렬 및 1등 질문 표시 (처음 로딩용)
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
            body { font-family: 'Malgun Gothic', sans-serif; display: flex; justify-content: center; background-color: #f4f4f4; padding: 50px 0; }
            .faq-container { width: 480px; }
            .faq-box { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
            
            .top3-section { margin-bottom: 25px; }
            .top3-title { font-size: 16px; font-weight: bold; color: #e67e22; margin-bottom: 10px; display: flex; align-items: center; }
            .top3-card-container { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 5px; }
            
            .top3-card { 
                min-width: 130px; max-width: 140px; background: #fff8ed; border: 1px solid #ffeaa7; padding: 12px; 
                border-radius: 12px; font-size: 13px; font-weight: bold; cursor: pointer; transition: 0.2s;
                word-break: break-all; white-space: normal; line-height: 1.4;
            }
            .top3-card:hover { transform: translateY(-3px); box-shadow: 0 5px 10px rgba(0,0,0,0.05); }
            .top3-rank { color: #e67e22; font-size: 11px; margin-bottom: 4px; display: block; }

            .category-group { margin-bottom: 15px; border: 2px solid #3498db; border-radius: 12px; overflow: hidden; }
            .category-group > summary { padding: 15px; background: #3498db; color: white; font-size: 17px; font-weight: bold; cursor: pointer; list-style: none; }
            .question-item { border-top: 1px solid #eee; background: #fff; }
            /* [수정] 자바스크립트 제어를 위해 각 카테고리 박스에 data-category 속성을 추적할 수 있도록 함 */
            .question-item summary { padding: 12px; font-size: 14px; font-weight: bold; color: #333; cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; }
            .answer { padding: 12px 15px; background: #fafafa; color: #666; font-size: 13px; line-height: 1.6; border-top: 1px dashed #eee; }
            
            .hot-badge { background: #e67e22; color: #fff; font-size: 10px; padding: 2px 6px; border-radius: 8px; font-weight: bold; }

            .modal-overlay {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0, 0, 0, 0.4); display: flex; justify-content: center; align-items: center; z-index: 1000;
            }
            .modal-content {
                background: white; width: 360px; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                text-align: center; animation: fadeIn 0.2s ease-out;
            }
            .modal-header { font-size: 16px; font-weight: bold; color: #e67e22; margin-bottom: 15px; text-align: left; }
            .modal-body { font-size: 14px; color: #444; line-height: 1.6; margin-bottom: 20px; text-align: left; background: #fafafa; padding: 15px; border-radius: 12px; border: 1px solid #eee; }
            .modal-close-btn { background: #3498db; color: white; border: none; padding: 10px 30px; font-size: 14px; font-weight: bold; border-radius: 10px; cursor: pointer; transition: 0.2s; width: 100%; }
            .modal-close-btn:hover { background: #2980b9; }

            @keyframes fadeIn {
                from { opacity: 0; transform: scale(0.95); }
                to { opacity: 1; transform: scale(1); }
            }
        </style>
    </head>
    <body>
        <div class="faq-container">
            <div class="faq-box">
                <h2 style="text-align: center; color: #2c3e50; margin-bottom: 25px;">도움말 센터</h2>

                <div class="top3-section">
                    <div class="top3-title">🔥 실시간 인기 질문</div>
                    <div class="top3-card-container">
                        {% for item in top_3 %}
                        <div class="top3-card" onclick="openModal('{{ item.question }}', '{{ item.answer }}', '{{ item.id }}')">
                            <span class="top3-rank">TOP {{ loop.index }}</span>
                            {{ item.question }}
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
                    <details class="question-item" data-faq-id="{{ item.id }}" ontoggle="if(this.open) triggerClick('{{ item.id }}')">
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
                            <div style="font-size: 11px; color: #ccc; margin-top: 8px;">
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
                <button class="modal-close-btn" onclick="closeModal()">확인</button>
            </div>
        </div>

        <script>
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
                            // 💡 숫자가 바뀌었으니 실시간으로 카테고리 1등을 다시 계산하는 함수를 실행합니다!
                            updateCategoryBadges();
                        }
                    }
                })
                .catch(err => console.error("조회수 업데이트 실패:", err));
            }

            // 🏆 실시간으로 각 카테고리별 조회수 1등을 찾아 뱃지를 새로 달아주는 함수
            function updateCategoryBadges() {
                const groups = document.querySelectorAll('.category-group');
                
                groups.forEach(group => {
                    const items = group.querySelectorAll('.question-item');
                    let maxCount = -1;
                    let topItem = null;

                    // 1. 해당 카테고리 안에서 조회수가 가장 높은 질문 찾기
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

                    // 2. 기존에 붙어있던 '인기 1위' 뱃지 전부 떼기
                    items.forEach(item => {
                        const badgeContainer = item.querySelector('.badge-container');
                        if (badgeContainer) badgeContainer.innerHTML = '';
                    });

                    // 3. 실시간 1등으로 뽑힌 질문에만 새 뱃지 달아주기
                    if (topItem && maxCount > 0) {
                        const badgeContainer = topItem.querySelector('.badge-container');
                        if (badgeContainer) {
                            badgeContainer.innerHTML = '<span class="hot-badge">🏆 인기 1위</span>';
                        }
                    }
                });
            }

            function openModal(question, answer, id) {
                document.getElementById('modal-title').innerText = "💡 " + question;
                document.getElementById('modal-body').innerText = answer;
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