---
layout: default
title: 디지털 포렌식 현장 압수 가이드
---

<style>
/* 모바일 친화형 다크/하이콘트라스트 카드 스타일 */
:root {
  --primary-color: #0284c7;
  --bg-dark: #0f172a;
  --card-bg: #1e293b;
  --border-color: #334155;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --accent-yellow: #f59e0b;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: #333333;
  line-height: 1.6;
}

.main-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
}

/* 상단 탭 / 필터 버튼 */
.filter-container {
  display: flex;
  gap: 8px;
  margin: 1.5rem 0;
  flex-wrap: wrap;
}

.filter-btn {
  flex: 1 1 calc(33.333% - 8px);
  min-height: 48px;
  background-color: #f1f5f9;
  border: 2px solid #cbd5e1;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.filter-btn:hover {
  background-color: #e2e8f0;
}

.filter-btn.active {
  background-color: #0284c7;
  border-color: #0284c7;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
}

/* 절차 카드 */
.step-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 1.25rem;
  margin-bottom: 1.25rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.step-card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
}

.step-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 0.5rem;
}

.step-badge {
  background: #0284c7;
  color: #ffffff;
  font-size: 0.8rem;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 9999px;
}

.step-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.step-content {
  font-size: 0.95rem;
  color: #334155;
  margin-bottom: 0.75rem;
}

.step-content ul {
  margin: 0.5rem 0;
  padding-left: 1.25rem;
}

.step-content li {
  margin-bottom: 0.35rem;
}

.caution-box {
  background-color: #fffbeb;
  border-left: 4px solid #f59e0b;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #92400e;
  margin-top: 0.75rem;
  font-weight: 500;
}

.checklist-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-top: 0.5rem;
  padding: 8px 10px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  cursor: pointer;
}

.checklist-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin-top: 3px;
  cursor: pointer;
  accent-color: #0284c7;
}

.checklist-item.checked {
  background: #f0fdf4;
  border-color: #86efac;
}

.checklist-item.checked span {
  text-decoration: line-through;
  color: #64748b;
}

/* 요약 안내 박스 */
.notice-banner {
  background: #eff6ff;
  border: 1.5px solid #3b82f6;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  color: #1e3a8a;
}

.print-btn {
  display: inline-block;
  background-color: #0f172a;
  color: #ffffff !important;
  padding: 10px 18px;
  border-radius: 8px;
  font-weight: 700;
  text-decoration: none;
  cursor: pointer;
  margin-bottom: 1.5rem;
  border: none;
}
.print-btn:hover {
  background-color: #1e293b;
}

@media print {
  .filter-container, .print-btn, .page-header {
    display: none !important;
  }
  .step-card {
    page-break-inside: avoid;
    border: 1px solid #ccc;
    box-shadow: none;
  }
}
</style>

<div class="notice-banner">
  <strong>⚡ 디지털 포렌식 현장 매뉴얼 & 체크리스트</strong><br>
  • 현장 증거 보존(사진 촬영, 전원/네트워크 격리, 쓰기 방지, Chain of Custody) 표준 절차입니다.<br>
  • 기기 유형 탭을 선택하여 필요한 항목을 확인하고 현장에서 체크박스를 터치해 기록하세요.
</div>

<div style="display: flex; justify-content: space-between; align-items: center;">
  <span style="font-weight: 700; color: #475569;">기기 유형별 절차 보기</span>
  <button class="print-btn" onclick="window.print()">🖨 체크리스트 인쇄 / PDF 저장</button>
</div>

<!-- 기기 선택 필터 버튼 -->
<div class="filter-container">
  <button class="filter-btn active" onclick="filterDevice('all', this)">전체 공통</button>
  <button class="filter-btn" onclick="filterDevice('pc', this)">💻 PC</button>
  <button class="filter-btn" onclick="filterDevice('iphone', this)">📱 iPhone</button>
  <button class="filter-btn" onclick="filterDevice('android', this)">🤖 Android</button>
</div>

<!-- =======================================================================
     1. 공통 사전 단계
     ======================================================================= -->
<div class="step-card" data-category="common">
  <div class="step-header">
    <span class="step-badge">공통-01</span>
    <h3 class="step-title">현장 안전 및 권한 확인</h3>
  </div>
  <div class="step-content">
    <ul>
      <li>압수수색영장 등 법적 권한 범위를 먼저 확인한다.</li>
      <li>현장 책임자(소지자/관리자)에게 신분과 목적을 고지한다.</li>
      <li>입회인(참관인) 확보 여부를 확인한다.</li>
    </ul>
    <label class="checklist-item" onclick="toggleCheck(this)">
      <input type="checkbox">
      <span>영장 범위 확인, 신분/목적 고지 및 입회인 확보 완료</span>
    </label>
  </div>
  <div class="caution-box">
    ⚠️ <strong>주의:</strong> 법적 권한 없이는 어떠한 기기도 조작하거나 압수하지 않는다.
  </div>
</div>

<div class="step-card" data-category="common">
  <div class="step-header">
    <span class="step-badge">공통-02</span>
    <h3 class="step-title">압수 대상 기기 유형 식별</h3>
  </div>
  <div class="step-content">
    현장에서 확보한 기기의 유형(PC / iPhone / Android)을 식별하고 분리한다. 여러 기기를 동시에 압수하는 경우, 기기마다 각각 식별 번호를 부여하여 관리한다.
  </div>
</div>

<div class="step-card" data-category="common">
  <div class="step-header">
    <span class="step-badge">공통-03</span>
    <h3 class="step-title">현장 사진/영상 기록</h3>
  </div>
  <div class="step-content">
    <ul>
      <li>기기의 위치, 화면 상태(켜짐/꺼짐), 주변 배선, 연결된 주변기기를 촬영한다.</li>
      <li>타임스탬프가 남도록 촬영하고, 전체 현장 → 기기 근접 순으로 상세히 기록한다.</li>
    </ul>
    <label class="checklist-item" onclick="toggleCheck(this)">
      <input type="checkbox">
      <span>현장 전경 및 기기 주변 배선/화면 상태 사진 촬영 완료</span>
    </label>
  </div>
  <div class="caution-box">
    ⚠️ <strong>주의:</strong> 사진 촬영 전에는 어떠한 기기도 임의로 만지거나 조작하지 않는다.
  </div>
</div>

<!-- =======================================================================
     2. PC 절차
     ======================================================================= -->
<div class="step-card" data-category="pc">
  <div class="step-header">
    <span class="step-badge">PC-01</span>
    <h3 class="step-title">전원 상태 확인 및 네트워크 차단 검토</h3>
  </div>
  <div class="step-content">
    <strong>[전원 상태 확인]</strong>
    <ul>
      <li>모니터 화면과 본체 상태(LED, 팬 소음)로 전원 ON/OFF를 확인한다.</li>
      <li>화면이 켜져 있다면 실행 중인 프로그램 및 활성 창을 그대로 촬영한다.</li>
    </ul>
    <strong>[네트워크 차단 검토]</strong>
    <ul>
      <li>원격 삭제/암호화/동기화를 방지하기 위해 랜케이블 분리 및 Wi-Fi 차단을 검토한다.</li>
      <li>RAM 수집이 필요한 경우, 차단 시점과 방법을 미리 결정한다.</li>
    </ul>
    <label class="checklist-item" onclick="toggleCheck(this)">
      <input type="checkbox">
      <span>전원 상태 사진 기록 및 네트워크(랜선/Wi-Fi) 격리 검토 완료</span>
    </label>
  </div>
  <div class="caution-box">
    ⚠️ <strong>주의:</strong> 전원이 꺼져 있다면 절대 켜지 않는다. 켜져 있다면 임의로 끄지 않는다.
  </div>
</div>

<div class="step-card" data-category="pc">
  <div class="step-header">
    <span class="step-badge">PC-02</span>
    <h3 class="step-title">휘발성 메모리(RAM) 수집 판단 및 저장매체 식별</h3>
  </div>
  <div class="step-content">
    <ul>
      <li>기기가 켜져 있고 암호화(BitLocker 등)가 의심되는 경우, RAM 이미징을 통한 복호화 키 확보 필요 여부를 판단한다.</li>
      <li>수사관은 포렌식 분석관과 협의하며, 단독으로 RAM 수집 도구를 실행하지 않는다.</li>
      <li>HDD/SSD/M.2 등 저장매체 모델명, 용량, 일련번호를 식별·기록한다.</li>
    </ul>
  </div>
</div>

<div class="step-card" data-category="pc">
  <div class="step-header">
    <span class="step-badge">PC-03</span>
    <h3 class="step-title">전원 차단, 케이블 라벨링 및 쓰기방지장치 준비</h3>
  </div>
  <div class="step-content">
    <ul>
      <li>휘발성 데이터 및 시스템 상태를 고려하여 승인된 절차로 전원을 차단한다.</li>
      <li>모든 케이블에 라벨을 부착하고 연결 위치를 사진으로 기록한 뒤 분리한다.</li>
      <li>이미징 시 반드시 하드웨어 쓰기방지장치(Write Blocker)를 연결한다.</li>
    </ul>
    <label class="checklist-item" onclick="toggleCheck(this)">
      <input type="checkbox">
      <span>케이블 라벨링 및 쓰기방지장치(Write Blocker) 준비 완료</span>
    </label>
  </div>
  <div class="caution-box">
    ⚠️ <strong>주의:</strong> 쓰기방지장치 없이 원본 저장매체를 분석용 PC에 직접 연결하지 않는다.
  </div>
</div>

<div class="step-card" data-category="pc">
  <div class="step-header">
    <span class="step-badge">PC-04</span>
    <h3 class="step-title">현장 이미징 / 이송 결정 및 포장</h3>
  </div>
  <div class="step-content">
    <ul>
      <li><strong>현장 추출:</strong> 공인 장비(디지털 콜렉터, DFT, AXIOM 등)로 비트 단위 이미징 후 SHA-256 해시값 산출.</li>
      <li><strong>실험실 이송:</strong> 저장매체를 정전기 방지 봉투에 포장 후 봉인 스티커 부착(서명/일시 기재).</li>
    </ul>
  </div>
</div>

<!-- =======================================================================
     3. iPhone 절차
     ======================================================================= -->
<div class="step-card" data-category="iphone">
  <div class="step-header">
    <span class="step-badge">iPhone-01</span>
    <h3 class="step-title">전원 상태 확인 및 네트워크·배터리 보존 (필수 설정)</h3>
  </div>
  <div class="step-content">
    <strong>[포렌식 분석관 권장 현장 설정 - BFU 방지]</strong>
    <label class="checklist-item" onclick="toggleCheck(this)">
      <input type="checkbox">
      <span>1. 자동 잠금 '안 함' 설정 완료 (설정 > 디스플레이 및 밝기 > 자동 잠금)</span>
    </label>
    <label class="checklist-item" onclick="toggleCheck(this)">
      <input type="checkbox">
      <span>2. [설정] 앱에서 Wi-Fi 끔(OFF) (제어센터 사용 금지)</span>
    </label>
    <label class="checklist-item" onclick="toggleCheck(this)">
      <input type="checkbox">
      <span>3. [설정] 앱에서 Bluetooth 끔(OFF) (제어센터 사용 금지)</span>
    </label>
    <label class="checklist-item" onclick="toggleCheck(this)">
      <input type="checkbox">
      <span>4. 에어플레인 모드 ON 및 상시 보조배터리 연결 (AFU 상태 유지)</span>
    </label>
  </div>
  <div class="caution-box">
    ⚠️ <strong>주의:</strong> 제어 센터 토글이 아닌 반드시 [설정] 앱 내부에서 Wi-Fi/Bluetooth를 비활성화해야 원격 초기화(Find My) 및 자동 재연결을 완전히 방지할 수 있습니다.
  </div>
</div>

<div class="step-card" data-category="iphone">
  <div class="step-header">
    <span class="step-badge">iPhone-02</span>
    <h3 class="step-title">기기 식별 및 전문 추출팀 인계 체크리스트</h3>
  </div>
  <div class="step-content">
    <ul>
      <li>기기 모델명 / iOS 버전 / 일련번호(IMEI) 기록</li>
      <li>Face ID / Touch ID 활성화 여부 확인</li>
      <li>마지막 잠금 해제 경과 시간 및 배터리 잔량(%) 확인</li>
      <li>화면에 노출된 Apple ID 및 iCloud 계정 정보 확인</li>
      <li>SIM 카드 장착 여부 및 통신사 확인</li>
    </ul>
    <label class="checklist-item" onclick="toggleCheck(this)">
      <input type="checkbox">
      <span>기기 식별 정보 및 암호화 상태 인계서 작성 완료</span>
    </label>
  </div>
  <div class="caution-box">
    ⚠️ <strong>주의:</strong> 잠금 해제 코드를 임의로 추측해 입력하지 않는다 (시도 횟수 초과 시 완전 잠금).
  </div>
</div>

<div class="step-card" data-category="iphone">
  <div class="step-header">
    <span class="step-badge">iPhone-03</span>
    <h3 class="step-title">모바일 포렌식 추출 또는 차폐 포장</h3>
  </div>
  <div class="step-content">
    <ul>
      <li><strong>현장 추출:</strong> 공인 장비(MD-NEXT, Cellebrite UFED, AXIOM 등)로 수행 후 해시값 검증.</li>
      <li><strong>실험실 이송:</strong> 페러데이백(Faraday Bag)에 넣고 충전 케이블을 연결한 상태로 밀봉 포장.</li>
    </ul>
  </div>
</div>

<!-- =======================================================================
     4. Android 절차
     ======================================================================= -->
<div class="step-card" data-category="android">
  <div class="step-header">
    <span class="step-badge">Android-01</span>
    <h3 class="step-title">전원 상태 확인 및 네트워크·배터리 보존</h3>
  </div>
  <div class="step-content">
    <ul>
      <li>화면 켜짐/꺼짐 및 잠금 여부를 확인하고 촬영한다 (켜져 있다면 전원을 끄지 않음).</li>
      <li>원격 초기화(Find My Device 등) 방지를 위해 페러데이백 사용 또는 비행기 탑승 모드로 격리한다.</li>
      <li>전원이 꺼지지 않도록 보조배터리 또는 충전 케이블을 즉시 연결한다.</li>
    </ul>
    <label class="checklist-item" onclick="toggleCheck(this)">
      <input type="checkbox">
      <span>네트워크 완전 차폐 및 보조배터리 충전 연결 완료</span>
    </label>
  </div>
</div>

<div class="step-card" data-category="android">
  <div class="step-header">
    <span class="step-badge">Android-02</span>
    <h3 class="step-title">기기 식별 및 보안상태 확인</h3>
  </div>
  <div class="step-content">
    <ul>
      <li>제조사/모델명, Android 버전, IMEI/시리얼 번호 확인</li>
      <li>생체인증(지문/얼굴) 사용 여부 및 화면상 구글 계정 확인</li>
      <li>USB 디버깅 활성화 여부 및 개발자 옵션 상태 확인</li>
    </ul>
  </div>
</div>

<div class="step-card" data-category="android">
  <div class="step-header">
    <span class="step-badge">Android-03</span>
    <h3 class="step-title">모바일 추출 및 차폐 포장</h3>
  </div>
  <div class="step-content">
    <ul>
      <li><strong>현장 추출:</strong> 공인 추출 장비(MD-NEXT, Cellebrite UFED, AXIOM 등)로 추출 후 해시값 기록.</li>
      <li><strong>실험실 이송:</strong> 페러데이백 및 정전기 방지 봉투 포장, 봉인 스티커 서명 및 사진 촬영.</li>
    </ul>
  </div>
</div>

<!-- =======================================================================
     5. 최종 인수인계 및 서류 작성
     ======================================================================= -->
<div class="step-card" data-category="common">
  <div class="step-header">
    <span class="step-badge">공통-최종</span>
    <h3 class="step-title">압수물 목록 및 Chain of Custody(증거보관연계) 작성</h3>
  </div>
  <div class="step-content">
    <ul>
      <li>압수물 목록(품명, 수량, 일련번호, 상태, 해시값)을 정확히 작성한다.</li>
      <li>피압수자(소지자/입회인)에게 참관권 보장 및 압수목록 사본을 교부한다.</li>
      <li>Chain of Custody 문서에 담당자, 인계 시각, 장소를 기재하고 서명한다.</li>
    </ul>
    <label class="checklist-item" onclick="toggleCheck(this)">
      <input type="checkbox">
      <span>압수목록 교부 및 Chain of Custody 서명 날인 완료</span>
    </label>
  </div>
</div>

<script>
// 필터 기능 (전체 / PC / iPhone / Android)
function filterDevice(category, btn) {
  const buttons = document.querySelectorAll('.filter-btn');
  buttons.forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  const cards = document.querySelectorAll('.step-card');
  cards.forEach(card => {
    const cardCat = card.getAttribute('data-category');
    if (category === 'all') {
      card.style.display = 'block';
    } else if (cardCat === 'common' || cardCat === category) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

// 체크리스트 터치 토글 및 로컬스토리지 저장
function toggleCheck(label) {
  const checkbox = label.querySelector('input[type="checkbox"]');
  // label 자체 클릭 이벤트와의 중복 방지 처리
  setTimeout(() => {
    if (checkbox.checked) {
      label.classList.add('checked');
    } else {
      label.classList.remove('checked');
    }
  }, 10);
}
</script>
