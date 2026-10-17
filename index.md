---
layout: default
title: 현장 압수 절차
---

<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

<style>
/* Streamlit 앱과 동일한 Dark Slate & Sky-blue 하이콘트라스트 테마 */
:root {
  --bg-main: #0f172a;
  --card-bg: #1e293b;
  --border-color: #334155;
  --accent-blue: #0284c7;
  --accent-sky: #38bdf8;
  --accent-yellow: #f59e0b;
  --accent-green: #10b981;
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
}

/* GitHub Pages Cayman 테마 헤더 조정 */
.page-header {
  padding: 1.5rem 1rem !important;
  background-color: #0b1120 !important;
  background-image: linear-gradient(135deg, #0f172a 0%, #0369a1 100%) !important;
  display: none !important; /* 모바일 앱 느낌을 위해 기본 헤더 숨김 */
}

body {
  background-color: var(--bg-main) !important;
  color: var(--text-primary) !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  margin: 0;
  padding: 0;
  -webkit-font-smoothing: antialiased;
}

.main-content {
  max-width: 580px !important;
  margin: 0 auto !important;
  padding: 1.25rem 1rem 4rem 1rem !important;
  background-color: var(--bg-main) !important;
}

/* 제목 스타일 */
.app-title {
  text-align: center;
  font-size: 1.6rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0.5rem 0 1.2rem 0;
  letter-spacing: -0.02em;
}

/* 카드 컨테이너 */
.app-card {
  background-color: #0b1329;
  border: 1px solid var(--border-color);
  border-radius: 18px;
  padding: 1.4rem 1.25rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
  margin-bottom: 1.25rem;
}

/* 입력 필드 */
.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 0.4rem;
}

.form-input, .form-textarea, .form-select {
  width: 100%;
  box-sizing: border-box;
  background-color: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  color: #f8fafc;
  font-size: 0.95rem;
  padding: 12px 14px;
  outline: none;
  transition: all 0.2s ease;
}

.form-input:focus, .form-textarea:focus, .form-select:focus {
  border-color: var(--accent-sky);
  box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.3);
}

/* 라디오 버튼 카드 그리드 */
.radio-group {
  display: flex;
  gap: 12px;
  margin-top: 6px;
}

.radio-card {
  flex: 1;
  min-height: 54px;
  background-color: #1e293b;
  border: 2px solid #334155;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
  text-align: center;
  padding: 4px 8px;
}

.radio-card:hover {
  background-color: #273549;
  border-color: var(--accent-sky);
}

.radio-card.active {
  background: rgba(2, 132, 199, 0.25);
  border-color: var(--accent-sky);
  color: var(--accent-sky);
  box-shadow: 0 4px 14px rgba(56, 189, 248, 0.35);
}

/* 버튼 스타일 */
.btn-primary {
  width: 100%;
  min-height: 56px;
  background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
  border: 1px solid var(--accent-sky);
  border-radius: 14px;
  color: #ffffff;
  font-size: 1.15rem;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(2, 132, 199, 0.45);
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 0.75rem;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
  box-shadow: 0 6px 18px rgba(56, 189, 248, 0.5);
}

.btn-secondary {
  flex: 1;
  min-height: 48px;
  background-color: #1e293b;
  border: 1px solid #475569;
  border-radius: 12px;
  color: #f1f5f9;
  font-size: 0.98rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-secondary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 프로그레스 바 */
.progress-container {
  margin: 1.2rem 0;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 600;
  margin-bottom: 6px;
}

.progress-bar-bg {
  width: 100%;
  height: 8px;
  background-color: #1e293b;
  border-radius: 9999px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #38bdf8 0%, #0284c7 100%);
  border-radius: 9999px;
  transition: width 0.3s ease;
  box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
}

/* 알림 박스 (주의/안내/완료) */
.alert-box {
  border-radius: 12px;
  padding: 12px 14px;
  margin: 1rem 0;
  font-size: 0.92rem;
  line-height: 1.55;
}

.alert-warning {
  border-left: 4px solid var(--accent-yellow);
  background: rgba(245, 158, 11, 0.1);
  color: #fef08a;
}

.alert-info {
  border-left: 4px solid var(--accent-sky);
  background: rgba(2, 132, 199, 0.12);
  color: #e0f2fe;
}

.alert-success {
  border-left: 4px solid var(--accent-green);
  background: rgba(16, 185, 129, 0.12);
  color: #a7f3d0;
}

/* 체크박스 항목 */
.custom-checkbox {
  background-color: #0f172a;
  border: 1px solid #1e293b;
  border-radius: 12px;
  padding: 12px 14px;
  margin: 0.6rem 0;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease;
}

.custom-checkbox.checked {
  background-color: rgba(16, 185, 129, 0.12);
  border-color: var(--accent-green);
}

.custom-checkbox.checked span {
  color: #34d399;
  font-weight: 700;
}

.custom-checkbox input[type="checkbox"] {
  width: 20px;
  height: 20px;
  accent-color: #0284c7;
}

/* 상단 헤더 줄 */
.step-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.role-badge {
  color: var(--accent-sky);
  font-size: 0.88rem;
  font-weight: 700;
}

.btn-home {
  background: #1e293b;
  border: 1px solid #475569;
  color: #e2e8f0;
  padding: 6px 14px;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
}

/* 화면 전환용 숨김/표시 */
.screen { display: none; }
.screen.active { display: block; }

/* 요약 배너 */
.notice-summary {
  background: rgba(245, 158, 11, 0.12);
  border: 1.5px solid #f59e0b;
  border-radius: 12px;
  padding: 12px 16px;
  margin-top: 18px;
  color: #fef08a;
  font-size: 0.92rem;
  line-height: 1.55;
  font-weight: 500;
}
</style>

<div class="main-content">

  <!-- =======================================================================
       화면 1: 시작 화면 (render_start)
       ======================================================================= -->
  <div id="screen-start" class="screen active">
    <h1 class="app-title">현장 압수 절차</h1>

    <div class="app-card">
      <div class="form-group">
        <label class="form-label">사건번호</label>
        <input type="text" id="inp-case-number" class="form-input" placeholder="예: 2026-고합-1234">
      </div>

      <div class="form-group">
        <label class="form-label">담당 수사관 (성명/소속)</label>
        <input type="text" id="inp-officer" class="form-input" placeholder="예: 경위 홍길동 / 사이버수사대">
      </div>

      <div class="form-group">
        <label class="form-label">피의자(소지자) 성명</label>
        <input type="text" id="inp-suspect" class="form-input" placeholder="피의자 또는 소지자 성명">
      </div>

      <div class="form-group">
        <label class="form-label">현장 위치</label>
        <input type="text" id="inp-location" class="form-input" placeholder="압수수색 장소">
      </div>

      <div class="form-group">
        <label class="form-label">압수 일시 (YYYY-MM-DD HH:MM)</label>
        <input type="text" id="inp-seized-at" class="form-input">
      </div>

      <div class="form-group" style="margin-top: 1.2rem;">
        <label class="form-label">현장 수행 주체</label>
        <div class="radio-group" id="role-radio-group">
          <div class="radio-card active" onclick="selectRole('수사관', this)">수사관</div>
          <div class="radio-card" onclick="selectRole('포렌식분석관', this)">포렌식분석관</div>
        </div>
      </div>

      <button type="button" class="btn-primary" onclick="startGuide()">절차 안내 시작 ▶</button>
    </div>

    <!-- 하단 요약 안내 (노란색) -->
    <div class="notice-summary">
      <span style="color: #fbbf24; font-weight: 800; font-size: 1rem; margin-right: 4px;">⚡ 현장 안내 요약</span><br>
      • 본 가이드는 현장 보존(사진·전원·네트워크·해시·Chain of Custody) 기록용입니다.<br>
      • 잠금해제 및 데이터 추출은 공인 장비와 권한을 가진 전문 인력이 수행해야 합니다.
    </div>
  </div>


  <!-- =======================================================================
       화면 2: 단계별 안내 화면 (render_guide)
       ======================================================================= -->
  <div id="screen-guide" class="screen">
    <div class="step-top-bar">
      <div>
        <h2 style="font-size: 1.35rem; margin: 0; font-weight: 800; color: #fff;">현장 압수 절차</h2>
        <span id="guide-role-badge" class="role-badge">[수사관]</span>
      </div>
      <button class="btn-home" onclick="goToStart()">⌂ 처음으로</button>
    </div>

    <!-- 프로그레스 바 -->
    <div class="progress-container">
      <div class="progress-header">
        <span id="step-counter-text">1 / 4 단계</span>
        <span id="device-type-display">기기 미선택</span>
      </div>
      <div class="progress-bar-bg">
        <div id="progress-bar-fill" class="progress-bar-fill" style="width: 25%;"></div>
      </div>
    </div>

    <!-- 단계 내용 카드 -->
    <div class="app-card">
      <h3 id="step-title" style="font-size: 1.25rem; margin-top: 0; color: #f8fafc; font-weight: 800;">1. 단계 제목</h3>
      
      <!-- 본문 안내 내용 -->
      <div id="step-detail-container" style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.65; margin: 1rem 0;"></div>

      <!-- 주의 박스 (노란색) -->
      <div id="step-caution-container" class="alert-box alert-warning" style="display: none;"></div>

      <!-- 기기 선택 인터페이스 (2단계일 때 노출) -->
      <div id="device-select-area" style="display: none; margin: 1.2rem 0;">
        <label class="form-label" style="font-size: 0.95rem;">기기 유형 선택</label>
        <div class="radio-group">
          <div class="radio-card" id="btn-device-pc" onclick="selectDevice('PC')">PC</div>
          <div class="radio-card" id="btn-device-iphone" onclick="selectDevice('iPhone')">iPhone</div>
          <div class="radio-card" id="btn-device-android" onclick="selectDevice('Android')">Android</div>
        </div>
      </div>

      <!-- iPhone 특화 설정 체크리스트 (포렌식분석관 + iPhone 4단계) -->
      <div id="iphone-settings-area" style="display: none; margin: 1.2rem 0;">
        <label class="form-label" style="color: #38bdf8; font-weight: 700;">⚙️ iPhone 현장 필수 설정 확인 (BFU 방지)</label>
        <label class="custom-checkbox" onclick="toggleCheckbox(this)">
          <input type="checkbox" id="chk-ip-autolock">
          <span>1. 자동 잠금 '안 함' 설정 완료 (화면 꺼짐/BFU 진입 방지)</span>
        </label>
        <label class="custom-checkbox" onclick="toggleCheckbox(this)">
          <input type="checkbox" id="chk-ip-wifi">
          <span>2. [설정] 앱에서 Wi-Fi 끔(OFF) (원격 초기화 방지)</span>
        </label>
        <label class="custom-checkbox" onclick="toggleCheckbox(this)">
          <input type="checkbox" id="chk-ip-bt">
          <span>3. [설정] 앱에서 Bluetooth 끔(OFF) (자동 재연결 방지)</span>
        </label>
        <label class="custom-checkbox" onclick="toggleCheckbox(this)">
          <input type="checkbox" id="chk-ip-airplane">
          <span>4. 에어플레인 모드 ON 및 상시 충전 케이블 연결 (AFU 유지)</span>
        </label>
      </div>

      <!-- 결정 라디오 (decision 타입 단계) -->
      <div id="decision-area" style="display: none; margin: 1.2rem 0;">
        <label class="form-label" style="color: #38bdf8; font-weight: 700;">▶ 처리 경로 결정</label>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <div class="radio-card" style="text-align: left; padding: 12px 14px;" id="dec-1" onclick="selectDecision('현장 즉시 이미지 추출')">1. 현장 즉시 이미지 추출</div>
          <div class="radio-card" style="text-align: left; padding: 12px 14px;" id="dec-2" onclick="selectDecision('압수 후 실험실 이송')">2. 압수 후 실험실 이송</div>
          <div class="radio-card" style="text-align: left; padding: 12px 14px;" id="dec-3" onclick="selectDecision('보류 (책임자 추가 판단 필요)')">3. 보류 (책임자 추가 판단 필요)</div>
        </div>
        <div id="decision-branch-info" class="alert-box alert-info" style="display: none; margin-top: 10px;"></div>
      </div>

      <!-- 포렌식 도구 선택 (tool_select) -->
      <div id="tool-select-area" style="display: none; margin: 1.2rem 0;">
        <label class="form-label">사용 장비 선택 (보유 포렌식 도구)</label>
        <select id="sel-tool" class="form-select" onchange="onToolChange(this.value)">
          <option value="">도구를 선택하세요</option>
        </select>
      </div>

      <!-- 이 단계 완료 체크 -->
      <label class="custom-checkbox" id="step-done-checkbox" onclick="toggleCheckbox(this)" style="margin-top: 1.2rem;">
        <input type="checkbox" id="chk-step-done">
        <span>이 단계의 절차 및 확인을 완료했습니다</span>
      </label>

      <!-- 현장 메모 -->
      <div class="form-group" style="margin-top: 1rem;">
        <label class="form-label">현장 메모 / 특이사항</label>
        <textarea id="txt-step-note" class="form-textarea" rows="2" placeholder="이 단계의 특이사항이나 일련번호, 해시값 등을 기록하세요" oninput="saveCurrentNote(this.value)"></textarea>
      </div>
    </div>

    <!-- 이전 / 다음 버튼 -->
    <div style="display: flex; gap: 10px;">
      <button type="button" class="btn-secondary" id="btn-prev" onclick="goPrevStep()">◀ 이전 단계</button>
      <button type="button" class="btn-primary" style="flex: 1; margin-top: 0; min-height: 48px; font-size: 1rem;" id="btn-next" onclick="goNextStep()">다음 단계 ▶</button>
    </div>

    <!-- 완료 안내 및 보고서 인쇄 -->
    <div id="finish-area" style="display: none; margin-top: 1.5rem;">
      <div class="alert-box alert-success" id="finish-message">
        절차가 완료되었습니다. 아래 버튼을 눌러 현장 기록 보고서를 인쇄하거나 PDF로 저장하세요.
      </div>
      <button type="button" class="btn-primary" onclick="printReport()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-color: #34d399;">
        📄 현장 압수 절차 리포트 인쇄 / PDF 저장
      </div>
    </div>
  </div>

</div>

<script>
// ===========================================================================
// 앱 상태 및 절차 데이터 정의 (app.py 완벽 대응)
// ===========================================================================
const state = {
  stage: 'start',
  role: '수사관',
  deviceType: null,
  currentIndex: 0,
  caseInfo: {},
  records: {},
  selectedDecision: null,
  selectedTool: null
};

const COMMON_PRE_STEPS = [
  {
    title: "현장 안전 및 권한 확인",
    detail: "• 압수수색영장 등 법적 권한 범위를 먼저 확인한다.\n• 현장 책임자(소지자/관리자)에게 신분과 목적을 고지한다.\n• 입회인(참관인) 확보 여부를 확인한다.",
    caution: "법적 권한 없이는 어떠한 기기도 조작/압수하지 않는다."
  },
  {
    title: "압수 대상 기기 유형 선택",
    type: "device_select",
    detail: "현장에서 확보한 기기의 유형을 선택한다. 선택한 유형에 따라 이후 단계의 세부 절차(전원/네트워크 보존 방법, 식별 항목, 추출 방식 등)가 달라진다.",
    caution: "여러 기기를 동시에 압수하는 경우, 기기마다 각각 기록한다."
  },
  {
    title: "현장 사진/영상 기록",
    detail: "• 기기의 위치, 화면 상태(켜짐/꺼짐), 주변 배선, 연결된 주변기기를 촬영한다.\n• 타임스탬프가 남도록 촬영하고, 전체 현장 → 기기 근접 순으로 기록한다.",
    caution: "사진 촬영 전에는 어떤 기기도 만지지 않는다."
  }
];

const PC_STEPS = [
  ...COMMON_PRE_STEPS,
  {
    title: "전원 상태 확인 및 네트워크 차단 검토",
    detail: "[전원 상태]\n• 모니터 화면과 본체 상태(LED, 팬 소음 등)로 전원 ON/OFF를 확인한다.\n• 화면이 켜져 있다면 현재 실행 중인 프로그램/화면을 그대로 촬영한다.\n\n[네트워크 차단 검토]\n• 원격 삭제/암호화/동기화를 막기 위해 랜케이블 분리, Wi-Fi 차단을 검토한다.\n• 휘발성 데이터(RAM) 수집이 필요한 경우, 네트워크 차단 시점과 방법을 미리 정한다.",
    caution: "전원이 꺼져 있다면 절대 켜지 않는다. 켜져 있다면 임의로 끄지 않는다. 네트워크 차단이 오히려 증거를 훼손할 수 있으니 사전 교육된 절차를 따른다."
  },
  {
    title: "휘발성 메모리(RAM) 수집 판단 및 저장매체 식별",
    role_override: {
      "수사관": {
        detail: "• 기기가 켜져 있고 암호화가 의심되는 경우, RAM 수집이 필요한지는 동행한 포렌식 분석관과 협의하여 판단한다.\n• 저장매체(HDD/SSD/M.2 등) 식별도 분석관과 함께 확인한다.\n• 수사관 단독으로 RAM 수집 도구를 설치/실행하지 않는다."
      },
      "포렌식분석관": {
        detail: "• 기기가 켜져 있고 암호화(BitLocker 등)가 의심되는 경우, RAM 이미징을 통한 복호화 키 확보 필요 여부를 직접 판단한다.\n• RAM 수집이 필요하면 보유 장비로 직접 수행한다.\n• 저장매체 모델명, 용량, 일련번호를 식별·기록한다."
      }
    },
    caution: "비전문 인력이 임의 프로그램을 설치/실행하면 증거가 훼손될 수 있다."
  },
  {
    title: "전원 차단, 케이블 라벨링 및 쓰기방지장치 준비",
    detail: "• 휘발성 데이터, 암호화 상태, 시스템 안정성 및 기관 SOP를 고려해 종료 방법을 결정한다.\n• 모든 케이블에 라벨을 붙이고 연결 위치를 사진으로 남긴 뒤 분리한다.\n• 이미징 시 반드시 쓰기방지장치(Write Blocker)를 사용하여 원본이 변경되지 않도록 준비한다.",
    caution: "노트북 배터리 분리 등 물리적 조작은 기기 구조와 보존 목표에 따라 승인된 절차로 수행한다. 쓰기방지장치 없이 원본 저장매체를 분석용 PC에 직접 연결하지 않는다."
  },
  {
    title: "현장 이미지 추출 여부 결정",
    type: "decision",
    options: ["현장 즉시 이미지 추출", "압수 후 실험실 이송", "보류 (책임자 추가 판단 필요)"],
    detail: "현장에서 바로 저장매체를 이미징할지, PC 또는 저장매체를 압수해 실험실로 옮긴 뒤 처리할지를 아래 기준으로 판단해 선택한다.\n\n판단 기준:\n• 시간 민감성: 암호화 재잠금, 시스템 자동 종료 위험이 임박했는가\n• 현장 장비: 공인 이미징 장비와 전문 인력이 현장에 있는가\n• 공간/환경: 전력, 작업 테이블 등 여건이 되는가\n• 법적 권한 범위: 영장/동의 범위가 현장 이미징까지 포함하는가",
    caution: "결정 권한은 현장 책임자에게 있다. 애매하면 '보류'를 선택하고 책임자 지시를 받는다.",
    branch_info: {
      "현장 즉시 이미지 추출": "→ 전력, 공간 등 현장 작업 여건을 지원하며 공인 장비로 이미징한다. 해시값(SHA-256)을 산출하고 압수목록을 교부한다.",
      "압수 후 실험실 이송": "→ PC 또는 저장매체를 봉인하여 실험실로 이송한다. 이송 책임자와 시각을 기록한다.",
      "보류 (책임자 추가 판단 필요)": "→ 책임자 지시가 있을 때까지 현재 보존 상태를 유지한다."
    }
  },
  {
    title: "포렌식 이미징 및 해시값 기록",
    tool_select: true,
    tools: ["디지털 콜렉터", "DFT", "AXIOM"],
    role_override: {
      "수사관": { detail: "• 포렌식 이미징은 동행한 포렌식 분석관이 보유 장비로 직접 수행한다. 수사관은 해시값과 사용 장비명을 전달받아 기록한다." },
      "포렌식분석관": { detail: "• 보유 장비 중 이 매체에 적합한 도구를 선택하여 비트 단위 이미지를 생성한다.\n• 기관 SOP에 따라 SHA-256 해시값을 산출·기록한다." }
    },
    caution: "해시값이 다르면 반드시 원인을 기록하고 재시도한다."
  },
  {
    title: "증거물 포장 및 봉인",
    detail: "• 정전기 방지 봉투(Anti-static bag)에 저장매체를 담는다.\n• 봉인 스티커에 서명/날짜를 기입하고 봉인 상태를 사진으로 남긴다.",
    caution: "충격/자기장에 노출되지 않도록 운반에 유의한다."
  },
  {
    title: "증거물 목록 및 인수인계 기록 작성",
    detail: "• 압수물 목록(품명, 수량, 일련번호, 상태)을 작성한다.\n• Chain of Custody(증거보관연계) 문서에 담당자, 시각, 장소를 기록한다.",
    caution: "이후 모든 취급자는 인계 시점마다 서명을 남긴다."
  }
];

const IPHONE_STEPS = [
  ...COMMON_PRE_STEPS,
  {
    title: "전원 상태 확인 및 네트워크·배터리 보존",
    iphone_settings: true,
    detail: "[전원/잠금 상태]\n• 화면이 켜져 있는지, 잠금 상태인지 확인하고 촬영한다.\n• 켜져 있다면 전원을 끄지 않는다.\n\n[네트워크 격리]\n• 원격 삭제를 막기 위해 즉시 네트워크로부터 격리한다(페러데이백 또는 비행기 모드).\n\n[배터리 방전 방지]\n• 전용 충전 케이블 또는 보조배터리를 즉시 연결한다.",
    caution: "꺼져 있던 기기라면 임의로 전원을 켜지 않는다. 충전 중에도 네트워크 격리 상태가 유지되는지 확인한다.",
    role_override: {
      "포렌식분석관": {
        detail: "[1. 자동 잠금 방지]\n• '설정' > '디스플레이 및 밝기' > '자동 잠금' > '안 함'으로 변경 (BFU 진입 방지)\n\n[2. 네트워크 완전 차단]\n• ⚠️ 제어 센터 사용 금지 (새벽 재연결 위험)\n• 반드시 [설정] 앱 내부에서 Wi-Fi OFF, Bluetooth OFF, 에어플레인 모드 ON\n\n[3. 전원 및 배터리 상시 유지]\n• 보조배터리 즉시 연결하여 AFU 상태 유지",
        caution: "제어 센터 토글이 아닌 반드시 [설정] 앱 내부에서 Wi-Fi/Bluetooth를 비활성화해야 원격 초기화를 완전히 방지할 수 있습니다."
      }
    }
  },
  {
    title: "기기 식별 및 보안상태 확인",
    detail: "• 모델명, iOS 버전, 일련번호/IMEI 확인\n• Face ID / Touch ID 사용 여부 확인\n• 화면에 노출된 Apple ID / iCloud 계정 정보 기록",
    caution: "잠금 해제를 시도하며 비밀번호를 추측하지 않는다."
  },
  {
    title: "현장 이미지 추출 여부 결정",
    type: "decision",
    options: ["현장 즉시 이미지 추출", "압수 후 실험실 이송", "보류 (책임자 추가 판단 필요)"],
    detail: "현장에서 바로 이미지를 뜰지, 기기를 압수해 실험실로 옮길지를 판단한다.",
    caution: "결정 권한은 현장 책임자에게 있다."
  },
  {
    title: "잠금해제/복호화 - 전문 추출팀 인계 체크리스트",
    detail: "• 모델명 / iOS 버전\n• Face ID / Touch ID 사용 여부\n• 마지막 잠금 해제 경과 시간\n• 배터리 잔량(%)\n• Apple ID 계정 정보\n• SIM 카드 장착 여부",
    caution: "소지자에게 암호 제공을 강요하지 않는다."
  },
  {
    title: "전문 추출팀 인계 / 포렌식 추출",
    tool_select: true,
    tools: ["MD-NEXT", "인사이트 UFED (Cellebrite)", "AXIOM"],
    role_override: {
      "수사관": { detail: "• 공인 모바일 포렌식 장비를 보유한 전문 인력에게 법적 절차에 따라 인계한다." },
      "포렌식분석관": { detail: "• 본인이 보유 장비 중 적합한 도구를 선택해 직접 추출을 수행한다. 작업 시각과 산출된 해시값을 기록한다." }
    },
    caution: "비전문 인력의 임의 추출 시도는 증거능력을 저해할 수 있다."
  },
  {
    title: "증거물 포장 및 봉인",
    detail: "• 페러데이백째로 정전기 방지 봉투에 추가 포장, 봉인 스티커 서명/날짜 기입 및 촬영.",
    caution: "운반 중 충격, 고온, 자기장 노출 주의."
  },
  {
    title: "증거물 목록 및 인수인계 기록 작성",
    detail: "• 압수물 목록과 Chain of Custody 문서를 작성한다.",
    caution: "모든 접촉/이동 이력을 빠짐없이 기록한다."
  }
];

const ANDROID_STEPS = [
  ...COMMON_PRE_STEPS,
  {
    title: "전원 상태 확인 및 네트워크·배터리 보존",
    detail: "[전원/화면 상태]\n• 화면 켜짐/꺼짐, 잠금 여부를 확인하고 촬영한다.\n• 켜져 있다면 전원을 끄지 않는다.\n\n[네트워크 격리]\n• 원격 초기화 방지를 위해 페러데이백 또는 비행기 모드로 격리한다.\n\n[배터리 유지]\n• 보조배터리를 즉시 연결한다.",
    caution: "꺼져 있던 기기라면 임의로 전원을 켜지 않는다."
  },
  {
    title: "기기 식별 및 보안상태 확인",
    detail: "• 제조사/모델명, Android 버전, IMEI/시리얼 확인\n• USB 디버깅 활성화 여부 확인\n• 루팅 여부 및 구글 계정 확인",
    caution: "잠금 해제를 시도하거나 코드를 추측하지 않는다."
  },
  {
    title: "현장 이미지 추출 여부 결정",
    type: "decision",
    options: ["현장 즉시 이미지 추출", "압수 후 실험실 이송", "보류 (책임자 추가 판단 필요)"],
    detail: "현장 즉시 추출 여부를 판단한다.",
    caution: "결정 권한은 현장 책임자에게 있다."
  },
  {
    title: "잠금해제/추출 - 전문 추출팀 인계 체크리스트",
    detail: "• 제조사/모델명 / Android 버전 / 보안 패치 수준\n• 생체인증 사용 여부\n• 배터리 잔량(%)\n• USB 디버깅 여부\n• SIM 카드 장착 여부",
    caution: "비밀번호 추측 입력 금지."
  },
  {
    title: "전문 추출팀 인계 / 포렌식 추출",
    tool_select: true,
    tools: ["MD-NEXT", "인사이트 UFED (Cellebrite)", "AXIOM"],
    role_override: {
      "수사관": { detail: "• 공인 모바일 포렌식 장비를 보유한 전문 인력에게 인계한다." },
      "포렌식분석관": { detail: "• 본인이 보유 장비로 직접 추출을 수행하고 해시값을 기록한다." }
    },
    caution: "비전문 인력 임의 조작 금지."
  },
  {
    title: "증거물 포장 및 봉인",
    detail: "• 정전기 방지 봉투/페러데이백 포장 후 봉인 스티커 서명/날짜 기입.",
    caution: "운반 중 충격 주의."
  },
  {
    title: "증거물 목록 및 인수인계 기록 작성",
    detail: "• 압수물 목록과 Chain of Custody 문서를 작성한다.",
    caution: "모든 접촉/이동 이력을 빠짐없이 기록한다."
  }
];

// 현재 시간에 맞는 KST 일시 초기화
function initDateTime() {
  const now = new Date();
  const kstOffset = 9 * 60;
  const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
  const kst = new Date(utc + (kstOffset * 60000));
  
  const yyyy = kst.getFullYear();
  const mm = String(kst.getMonth() + 1).padStart(2, '0');
  const dd = String(kst.getDate()).padStart(2, '0');
  const hh = String(kst.getHours()).padStart(2, '0');
  const min = String(kst.getMinutes()).padStart(2, '0');
  
  document.getElementById('inp-seized-at').value = `${yyyy}-${mm}-${dd} ${hh}:${min}`;
}

// 역할 선택
function selectRole(role, el) {
  state.role = role;
  document.querySelectorAll('#role-radio-group .radio-card').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
}

// 시작하기
function startGuide() {
  state.caseInfo = {
    caseNumber: document.getElementById('inp-case-number').value,
    officer: document.getElementById('inp-officer').value,
    suspect: document.getElementById('inp-suspect').value,
    location: document.getElementById('inp-location').value,
    seizedAt: document.getElementById('inp-seized-at').value
  };
  state.deviceType = null;
  state.currentIndex = 0;
  state.stage = 'guide';
  
  document.getElementById('screen-start').classList.remove('active');
  document.getElementById('screen-guide').classList.add('active');
  
  renderGuideStep();
}

function goToStart() {
  state.stage = 'start';
  document.getElementById('screen-guide').classList.remove('active');
  document.getElementById('screen-start').classList.add('active');
}

// 현재 단계 목록 가져오기
function getCurrentStepList() {
  if (state.deviceType === 'PC') return PC_STEPS;
  if (state.deviceType === 'iPhone') return IPHONE_STEPS;
  if (state.deviceType === 'Android') return ANDROID_STEPS;
  return COMMON_PRE_STEPS;
}

// 단계 렌더링
function renderGuideStep() {
  const steps = getCurrentStepList();
  const totalSteps = state.role === '수사관' ? 4 : steps.length;
  const curPos = state.currentIndex + 1;
  const step = steps[state.currentIndex];
  
  // 배지 및 카운터
  document.getElementById('guide-role-badge').innerText = state.deviceType ? `[${state.deviceType} · ${state.role}]` : `[${state.role}]`;
  document.getElementById('step-counter-text').innerText = `${curPos} / ${totalSteps} 단계`;
  document.getElementById('device-type-display').innerText = state.deviceType ? `기기: ${state.deviceType}` : '기기 선택 전';
  
  // 프로그레스 바 계산
  const percent = Math.min(100, Math.round((curPos / totalSteps) * 100));
  document.getElementById('progress-bar-fill').style.width = `${percent}%`;
  
  // 제목 및 내용
  document.getElementById('step-title').innerText = `${curPos}. ${step.title}`;
  
  let detailText = step.detail || '';
  let cautionText = step.caution || '';
  if (step.role_override && step.role_override[state.role]) {
    if (step.role_override[state.role].detail) detailText = step.role_override[state.role].detail;
    if (step.role_override[state.role].caution) cautionText = step.role_override[state.role].caution;
  }
  
  document.getElementById('step-detail-container').innerHTML = detailText.replace(/\n/g, '<br>');
  
  const cautionEl = document.getElementById('step-caution-container');
  if (cautionText) {
    cautionEl.innerHTML = `⚠️ <strong>주의:</strong> ${cautionText}`;
    cautionEl.style.display = 'block';
  } else {
    cautionEl.style.display = 'none';
  }
  
  // 기기 선택 영역
  const devSelectArea = document.getElementById('device-select-area');
  if (step.type === 'device_select') {
    devSelectArea.style.display = 'block';
    updateDeviceButtons();
  } else {
    devSelectArea.style.display = 'none';
  }
  
  // iPhone 특화 설정 영역
  const ipArea = document.getElementById('iphone-settings-area');
  if (step.iphone_settings && state.role === '포렌식분석관') {
    ipArea.style.display = 'block';
  } else {
    ipArea.style.display = 'none';
  }
  
  // 결정 영역
  const decArea = document.getElementById('decision-area');
  if (step.type === 'decision') {
    decArea.style.display = 'block';
  } else {
    decArea.style.display = 'none';
  }
  
  // 도구 선택 영역
  const toolArea = document.getElementById('tool-select-area');
  if (step.tool_select && state.role === '포렌식분석관') {
    toolArea.style.display = 'block';
    const select = document.getElementById('sel-tool');
    select.innerHTML = '<option value="">도구를 선택하세요</option>';
    (step.tools || []).forEach(t => {
      select.innerHTML += `<option value="${t}">${t}</option>`;
    });
  } else {
    toolArea.style.display = 'none';
  }
  
  // 완료 체크 및 메모 복원
  const rec = state.records[state.currentIndex] || {};
  const chkDone = document.getElementById('chk-step-done');
  chkDone.checked = !!rec.done;
  const labelDone = document.getElementById('step-done-checkbox');
  if (rec.done) labelDone.classList.add('checked'); else labelDone.classList.remove('checked');
  document.getElementById('txt-step-note').value = rec.note || '';
  
  // 버튼 활성화 처리
  document.getElementById('btn-prev').disabled = (state.currentIndex === 0);
  
  const finishArea = document.getElementById('finish-area');
  const btnNext = document.getElementById('btn-next');
  
  const isLast = (curPos >= totalSteps);
  if (isLast) {
    btnNext.style.display = 'none';
    finishArea.style.display = 'block';
    const finishMsg = document.getElementById('finish-message');
    if (state.role === '수사관') {
      finishMsg.innerText = "수사관 절차는 4단계까지입니다. 이후 기술적 절차는 포렌식분석관이 이어서 수행합니다. 아래에서 리포트를 인쇄하거나 PDF로 저장하세요.";
    } else {
      finishMsg.innerText = "모든 포렌식 절차가 완료되었습니다. 아래 버튼을 눌러 리포트를 인쇄하거나 PDF로 저장하세요.";
    }
  } else {
    btnNext.style.display = 'flex';
    finishArea.style.display = 'none';
  }
}

// 기기 선택
function selectDevice(device) {
  state.deviceType = device;
  updateDeviceButtons();
  setTimeout(() => {
    goNextStep();
  }, 200);
}

function updateDeviceButtons() {
  ['PC', 'iPhone', 'Android'].forEach(d => {
    const btn = document.getElementById(`btn-device-${d.toLowerCase()}`);
    if (btn) {
      if (state.deviceType === d) btn.classList.add('active');
      else btn.classList.remove('active');
    }
  });
}

// 결정 선택
function selectDecision(decision) {
  state.selectedDecision = decision;
  const steps = getCurrentStepList();
  const step = steps[state.currentIndex];
  const infoEl = document.getElementById('decision-branch-info');
  if (step.branch_info && step.branch_info[decision]) {
    infoEl.innerText = step.branch_info[decision];
    infoEl.style.display = 'block';
  }
}

// 체크박스 토글
function toggleCheckbox(label) {
  const chk = label.querySelector('input[type="checkbox"]');
  setTimeout(() => {
    if (chk.checked) label.classList.add('checked');
    else label.classList.remove('checked');
    
    if (chk.id === 'chk-step-done') {
      if (!state.records[state.currentIndex]) state.records[state.currentIndex] = {};
      state.records[state.currentIndex].done = chk.checked;
    }
  }, 10);
}

// 메모 저장
function saveCurrentNote(val) {
  if (!state.records[state.currentIndex]) state.records[state.currentIndex] = {};
  state.records[state.currentIndex].note = val;
}

// 이전 / 다음 이동
function goPrevStep() {
  if (state.currentIndex > 0) {
    state.currentIndex--;
    renderGuideStep();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

function goNextStep() {
  const steps = getCurrentStepList();
  const totalSteps = state.role === '수사관' ? 4 : steps.length;
  
  // 2단계에서 기기 선택 여부 확인
  if (steps[state.currentIndex].type === 'device_select' && !state.deviceType) {
    alert("기기 유형(PC / iPhone / Android)을 먼저 선택해주세요.");
    return;
  }
  
  if (state.currentIndex < totalSteps - 1) {
    state.currentIndex++;
    renderGuideStep();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

// 리포트 인쇄 / PDF 저장
function printReport() {
  window.print();
}

window.onload = function() {
  initDateTime();
};
</script>
