from flask import Flask, render_template_string, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

url = "https://yjtnvcydrrxjoitjqtzg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlqdG52Y3lkcnJ4am9pdGpxdHpnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg2MjA1NDAsImV4cCI6MjA5NDE5NjU0MH0.9WXlEv82kg48PmDJudJ_DW0X5C5eqDR771ZXxj8zb6s"
supabase: Client = create_client(url, key)

@app.route('/')
def index():
    response = supabase.table("faqs").select("*").execute()
    faqs = response.data

    top_3_faqs = sorted(faqs, key=lambda x: x.get('click_count', 0), reverse=True)[:3]

    category_order = ["💳 카드 / 결제", "📱 쿠폰 / 바코드", "🥤 이용방법", "기타"]
    grouped_faqs = {cat: [] for cat in category_order}
    
    for item in faqs:
        cat = item.get('category', '기타')
        if cat not in grouped_faqs:
            grouped_faqs[cat] = []
        grouped_faqs[cat].append(item)

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
                <details class="category-group">
                    <summary>{{ category }}</summary>
                    {% for item in items %}
                    <details class="question-item" ontoggle="if(this.open) triggerClick('{{ item.id }}')">
                        <summary>
                            {{ item.question }}
                            {% if item.top_in_category %}
                            <span class="hot-badge">🏆 인기 1위</span>
                            {% endif %}
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
    // 이미 클릭된 항목을 기록하여 중복 카운트 방지
    let clickedMap = {};

    function triggerClick(id) {
        // 이미 이번 페이지 세션에서 클릭했다면 리턴
        if (clickedMap[id]) return;
        clickedMap[id] = true;

        // 화면에 조회수가 표시된 엘리먼트가 있는지 확인
        let target = document.getElementById('count-' + id);
        let nextNum = 1; // 기본값

        if (target) {
            let currentNum = parseInt(target.textContent.trim(), 10) || 0;
            nextNum = currentNum + 1;
            target.textContent = nextNum; // 즉시 새로고침 없이 화면 반영
        } else {
            // 만약 화면에 엘리먼트가 없더라도 DB에는 반영하기 위해 
            // 현재 click_count 값을 정확히 모르므로, 백엔드에서 +1을 해주는 것이 안전합니다.
            // 아래 대안을 참고해 주세요.
        }

        // 백엔드로 비동기(Fetch) 요청 보내기
        fetch('/update_click', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({id: id, count: nextNum})
        })
        .then(res => res.json())
        .then(data => {
            console.log("조회수 업데이트 성공:", data);
        })
        .catch(err => console.error("조회수 업데이트 실패:", err));
    }

    function openModal(question, answer, id) {
        document.getElementById('modal-title').innerText = "💡 " + question;
        document.getElementById('modal-body').innerText = answer;
        document.getElementById('custom-modal').style.display = 'flex';
        
        // 모달창이 열릴 때도 실시간 조회수 증가 함수 호출
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
        # DB에서 현재 click_count 값을 안전하게 새로 가져옴
        row = supabase.table("faqs").select("click_count").eq("id", faq_id).single().execute()
        if row.data:
            current_count = row.data.get('click_count', 0)
            # 가져온 값에 정확히 +1을 해서 업데이트
            supabase.table("faqs").update({"click_count": current_count + 1}).eq("id", faq_id).execute()
            return jsonify({"status": "success", "new_count": current_count + 1})
    except Exception as e:
        print(f"조회수 업데이트 중 오류 발생: {e}")
        
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)