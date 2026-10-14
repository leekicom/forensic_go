# -*- coding: utf-8 -*-
"""
디지털 포렌식 현장 압수 절차 안내 (Streamlit 웹앱)

실행:
    pip install streamlit
    streamlit run app.py

배포 (휴대폰/아이폰에서 접속하려면):
    1) GitHub 저장소에 app.py, requirements.txt 를 올린다.
    2) https://share.streamlit.io (Streamlit Community Cloud) 에서
       저장소를 연결해 배포하면 https://xxxx.streamlit.app 링크가 생긴다.
    3) 아이폰/안드로이드 어디서든 그 링크를 브라우저로 열면 바로 사용 가능.

이 프로그램은 "현장에서 무엇을/왜/어떤 순서로 보존해야 하는지"를 안내하는
절차 가이드입니다. 잠금해제·데이터추출 등 기술적 작업은 법적 권한을 가진
전문 인력이 공인 장비로 수행해야 합니다.
"""

import streamlit as st
import datetime
import json
import io
import zipfile

APP_TITLE = "현장 압수 절차 안내 (Digital Forensics Seizure Guide)"

# ---------------------------------------------------------------------------
# 절차 데이터 (tkinter 버전과 동일)
# ---------------------------------------------------------------------------

COMMON_PRE_STEPS = [
    {
        "title": "0. 현장 안전 및 권한 확인",
        "detail": (
            "- 압수수색영장 등 법적 권한 범위를 먼저 확인한다.\n"
            "- 현장 책임자(소지자/관리자)에게 신분과 목적을 고지한다.\n"
            "- 입회인(참관인) 확보 여부를 확인한다."
        ),
        "caution": "법적 권한 없이는 어떠한 기기도 조작/압수하지 않는다.",
    },
    {
        "title": "1. 현장 사진/영상 기록",
        "detail": (
            "- 기기의 위치, 화면 상태(켜짐/꺼짐), 주변 배선, 연결된 주변기기를 촬영한다.\n"
            "- 타임스탬프가 남도록 촬영하고, 전체 현장 → 기기 근접 순으로 기록한다."
        ),
        "caution": "사진 촬영 전에는 어떤 기기도 만지지 않는다.",
    },
]

PC_STEPS = COMMON_PRE_STEPS + [
    {
        "title": "2. 전원 상태 확인",
        "detail": (
            "- 모니터 화면과 본체 상태(LED, 팬 소음 등)로 전원 ON/OFF를 확인한다.\n"
            "- 화면이 켜져 있다면 현재 실행 중인 프로그램/화면을 그대로 촬영한다."
        ),
        "caution": "전원이 꺼져 있다면 절대 켜지 않는다. 켜져 있다면 임의로 끄지 않는다.",
    },
    {
        "title": "3. 네트워크 연결 차단 검토",
        "detail": (
            "- 원격 삭제/암호화/동기화를 막기 위해 랜케이블 분리, Wi-Fi 차단을 검토한다.\n"
            "- 휘발성 데이터(RAM) 수집이 필요한 경우, 기관 SOP에 따라 네트워크\n"
            "  차단 시점과 방법을 사전 결정한다."
        ),
        "caution": "네트워크 차단이 오히려 증거를 훼손할 수 있는 경우도 있으니 사전 교육된 절차를 따른다.",
    },
    {
        "title": "4. 휘발성 메모리(RAM) 수집 여부 판단",
        "detail": (
            "- 기기가 켜져 있고 암호화(BitLocker 등)가 의심되는 경우, RAM 이미징을\n"
            "  통한 복호화 키 확보를 기관 지침에 따라 검토한다.\n"
            "- RAM 수집은 공인된 도구와 절차로 전문 인력이 수행한다."
        ),
        "caution": "비전문 인력이 임의 프로그램을 설치/실행하면 증거가 훼손될 수 있다.",
    },
    {
        "title": "5. 전원 차단 및 케이블 라벨링",
        "detail": (
            "- 휘발성 수집이 끝났거나 불필요하다면, 전원 케이블을 직접 뽑아 안전하게\n"
            "  종료한다(정상 종료 대신 플러그 분리를 권장하는 기관 지침이 많음).\n"
            "- 모든 케이블에 라벨을 붙이고 연결 위치를 사진으로 남긴 뒤 분리한다."
        ),
        "caution": "노트북은 배터리도 함께 분리하거나 전원이 완전히 차단되었는지 확인한다.",
    },
    {
        "title": "6. 저장매체 식별 및 쓰기방지장치 준비",
        "detail": (
            "- HDD/SSD/M.2 등 저장매체 모델명, 용량, 일련번호를 기록한다.\n"
            "- 이미징 시 반드시 쓰기방지장치(Write Blocker)를 사용하여 원본이\n"
            "  변경되지 않도록 한다."
        ),
        "caution": "쓰기방지장치 없이 원본 저장매체를 PC에 직접 마운트하지 않는다.",
    },
    {
        "title": "7. 포렌식 이미징 및 해시값 기록",
        "detail": (
            "- 공인 포렌식 이미징 도구(FTK Imager, EnCase 등)로 비트 단위 이미지를 생성한다.\n"
            "- 이미징 전/후 SHA-256(또는 MD5) 해시값을 산출하여 원본과 사본의\n"
            "  무결성을 증명한다."
        ),
        "caution": "해시값이 다르면 반드시 원인을 기록하고 재시도한다.",
    },
    {
        "title": "8. 증거물 포장 및 봉인",
        "detail": (
            "- 정전기 방지 봉투(Anti-static bag)에 저장매체를 담는다.\n"
            "- 봉인 스티커에 서명/날짜를 기입하고 봉인 상태를 사진으로 남긴다."
        ),
        "caution": "충격/자기장에 노출되지 않도록 운반에 유의한다.",
    },
    {
        "title": "9. 증거물 목록 및 인수인계 기록 작성",
        "detail": (
            "- 압수물 목록(품명, 수량, 일련번호, 상태)을 작성한다.\n"
            "- Chain of Custody(증거보관연계) 문서에 담당자, 시각, 장소를 기록한다."
        ),
        "caution": "이후 모든 취급자는 인계 시점마다 서명을 남긴다.",
    },
]

IPHONE_STEPS = COMMON_PRE_STEPS + [
    {
        "title": "2. 전원 및 잠금 상태 확인",
        "detail": (
            "- 화면이 켜져 있는지, 잠금(Lock) 상태인지 확인하고 촬영한다.\n"
            "- 켜져 있다면 전원을 끄지 않는다(끄면 재부팅 후 암호화가 강화되어\n"
            "  이후 접근이 더 어려워질 수 있다)."
        ),
        "caution": "꺼져 있던 기기라면 임의로 전원을 켜지 않는다.",
    },
    {
        "title": "3. 원격 삭제/초기화 방지 (네트워크 차단)",
        "detail": (
            "- 'iPhone 찾기'를 통한 원격 삭제를 막기 위해 가능한 한 빨리\n"
            "  네트워크로부터 격리한다.\n"
            "- 방법: 페러데이백(Faraday bag)에 넣거나, 비행기 모드 전환,\n"
            "  또는 SIM 제거를 기관 SOP에 따라 선택한다."
        ),
        "caution": "화면 조작이 필요한 경우, 조작 전후 과정을 반드시 촬영/기록한다.",
    },
    {
        "title": "4. 배터리 방전 방지",
        "detail": (
            "- 기기 전원이 꺼지면 보호가 강화되어 접근이 어려워질 수 있으므로\n"
            "  방전되지 않도록 한다.\n"
            "- 페러데이백 전용 충전 케이블 또는 보조배터리를 사용한다."
        ),
        "caution": "충전 중에도 네트워크 격리 상태가 유지되는지 확인한다.",
    },
    {
        "title": "5. 기기 식별 정보 기록",
        "detail": (
            "- 모델명, iOS 버전, 일련번호/IMEI(화면/기기 라벨에서 확인 가능한\n"
            "  범위), 연결된 Apple ID(화면에 노출된 경우)를 기록한다."
        ),
        "caution": "잠금 해제를 시도하며 정보를 캐내려 하지 않는다. 화면에 보이는 정보만 기록한다.",
    },
    {
        "title": "6. 잠금 관련 상태 메모",
        "detail": (
            "- 잠금화면 메시지, Face ID/Touch ID 사용 여부 등 화면에 보이는\n"
            "  정보를 기록해 둔다(전문 추출팀 전달용 참고 정보)."
        ),
        "caution": "소지자의 동의나 법적 근거 없이 잠금 해제를 요구/시도하지 않는다.",
    },
    {
        "title": "7. 전문 추출팀 인계",
        "detail": (
            "- 법적 권한과 절차에 따라 공인 모바일 포렌식 장비를 보유한\n"
            "  전문 인력에게 인계한다."
        ),
        "caution": "비전문 인력이 임의 소프트웨어로 추출을 시도하면 증거능력이 부정될 수 있다.",
    },
    {
        "title": "8. 증거물 포장 및 봉인",
        "detail": "- 페러데이백째로 정전기 방지 봉투에 추가 포장, 봉인 스티커 서명/날짜 기입 및 촬영.",
        "caution": "운반 중 충격, 고온, 자기장 노출 주의.",
    },
    {
        "title": "9. 증거물 목록 및 인수인계 기록 작성",
        "detail": "- 압수물 목록과 Chain of Custody 문서를 작성한다.",
        "caution": "모든 접촉/이동 이력을 빠짐없이 기록한다.",
    },
]

ANDROID_STEPS = COMMON_PRE_STEPS + [
    {
        "title": "2. 전원 및 화면 상태 확인",
        "detail": (
            "- 화면 켜짐/꺼짐, 잠금 여부를 확인하고 촬영한다.\n"
            "- 켜져 있다면 전원을 끄지 않는다."
        ),
        "caution": "꺼져 있던 기기라면 임의로 전원을 켜지 않는다.",
    },
    {
        "title": "3. 네트워크 격리",
        "detail": (
            "- 원격 초기화(Find My Device 등) 방지를 위해 네트워크로부터 격리한다.\n"
            "- 방법: 페러데이백 사용, 비행기 모드, 또는 기관 SOP에 따른 방법."
        ),
        "caution": "화면 조작이 필요하면 과정을 반드시 촬영/기록한다.",
    },
    {
        "title": "4. 배터리 방전 방지",
        "detail": "- 전원이 꺼지지 않도록 페러데이백 전용 충전 케이블 또는 보조배터리를 연결한다.",
        "caution": "충전 중 네트워크 격리 유지 여부 확인.",
    },
    {
        "title": "5. 기기 식별 정보 기록",
        "detail": (
            "- 제조사/모델명, Android 버전, IMEI/시리얼, USB 디버깅 활성화\n"
            "  여부(화면상 확인 가능한 경우)를 기록한다."
        ),
        "caution": "잠금 해제를 시도하거나 코드를 추측하지 않는다.",
    },
    {
        "title": "6. 루팅/개발자 옵션 상태 메모",
        "detail": "- 가능한 범위에서 루팅 여부, 개발자 옵션 활성화 여부 등을 기록해 둔다.",
        "caution": "직접 설정을 변경하지 않는다. 변경이 필요하면 기록 후 전문팀과 협의.",
    },
    {
        "title": "7. 전문 추출팀 인계",
        "detail": "- 공인 모바일 포렌식 장비를 보유한 전문 인력에게 법적 절차에 따라 인계한다.",
        "caution": "비전문 인력의 임의 추출 시도는 증거능력을 저해할 수 있다.",
    },
    {
        "title": "8. 증거물 포장 및 봉인",
        "detail": "- 정전기 방지 봉투/페러데이백 포장 후 봉인 스티커 서명/날짜 기입.",
        "caution": "운반 중 충격, 고온 주의.",
    },
    {
        "title": "9. 증거물 목록 및 인수인계 기록 작성",
        "detail": "- 압수물 목록과 Chain of Custody 문서를 작성한다.",
        "caution": "모든 접촉/이동 이력을 빠짐없이 기록한다.",
    },
]

DEVICE_STEPS = {"PC": PC_STEPS, "iPhone": IPHONE_STEPS, "Android": ANDROID_STEPS}

# ---------------------------------------------------------------------------
# Streamlit 앱
# ---------------------------------------------------------------------------

st.set_page_config(page_title=APP_TITLE, page_icon="🔎", layout="centered")


def init_state():
    defaults = {
        "stage": "start",          # "start" | "guide"
        "device_type": None,
        "current_index": 0,
        "case_info": {},
        "records": {},             # {step_index: {"done": bool, "note": str, "photos": [UploadedFile,...]}}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def render_start():
    st.title(APP_TITLE)
    st.caption(
        "현장 보존 절차를 단계별로 안내합니다. 먼저 사건 정보를 입력한 뒤 "
        "압수 대상 기기 유형을 선택하세요."
    )

    with st.form("case_info_form"):
        case_number = st.text_input("사건번호")
        officer = st.text_input("담당자")
        location = st.text_input("현장 위치")
        seized_at = st.text_input(
            "압수 일시 (YYYY-MM-DD HH:MM)",
            value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
        device_type = st.radio("압수 대상 기기 유형", ["PC", "iPhone", "Android"], horizontal=True)
        submitted = st.form_submit_button("절차 안내 시작 ▶")

    if submitted:
        st.session_state.case_info = {
            "사건번호": case_number,
            "담당자": officer,
            "현장 위치": location,
            "압수 일시": seized_at,
        }
        st.session_state.device_type = device_type
        st.session_state.current_index = 0
        steps = DEVICE_STEPS[device_type]
        st.session_state.records = {
            i: {"done": False, "note": "", "photos": []} for i in range(len(steps))
        }
        st.session_state.stage = "guide"
        st.rerun()

    st.info(
        "※ 본 프로그램은 현장 보존 절차(사진기록, 전원상태, 네트워크 차단, 해시기록, "
        "Chain of Custody 등) 안내용입니다. 잠금해제·데이터추출 등 기술적 작업은 "
        "법적 권한을 가진 전문 인력이 공인 장비로 수행해야 합니다."
    )


def build_report_text():
    device_type = st.session_state.device_type
    steps = DEVICE_STEPS[device_type]
    records = st.session_state.records
    lines = []
    lines.append("=" * 70)
    lines.append("디지털 포렌식 현장 압수 절차 리포트 (Chain of Custody Log)")
    lines.append("=" * 70)
    lines.append(f"생성 시각: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"기기 유형: {device_type}")
    for k, v in st.session_state.case_info.items():
        lines.append(f"{k}: {v}")
    lines.append("-" * 70)
    for i, step in enumerate(steps):
        rec = records[i]
        status = "[완료]" if rec["done"] else "[미완료]"
        lines.append(f"\n{status} {step['title']}")
        lines.append(step["detail"])
        if step.get("caution"):
            lines.append(f"주의: {step['caution']}")
        if rec["note"]:
            lines.append(f"현장 메모: {rec['note']}")
        photos = rec.get("photos") or []
        if photos:
            names = ", ".join(p.name for p in photos)
            lines.append(f"첨부 사진 ({len(photos)}장): {names}")
    lines.append("\n" + "=" * 70)
    lines.append("서명란:")
    lines.append("담당자 서명: ______________________   일시: ______________________")
    lines.append("입회인 서명: ______________________   일시: ______________________")
    lines.append("=" * 70)
    return "\n".join(lines)


def render_guide():
    device_type = st.session_state.device_type
    steps = DEVICE_STEPS[device_type]
    idx = st.session_state.current_index
    step = steps[idx]
    rec = st.session_state.records[idx]

    top_l, top_r = st.columns([4, 1])
    with top_l:
        st.title(f"[{device_type}] 현장 압수 절차")
    with top_r:
        if st.button("처음으로"):
            st.session_state.stage = "start"
            st.rerun()

    st.progress((idx + 1) / len(steps), text=f"{idx + 1} / {len(steps)} 단계")

    st.subheader(step["title"])
    st.markdown(step["detail"].replace("\n", "  \n"))
    if step.get("caution"):
        st.warning(f"⚠ 주의: {step['caution']}")

    rec["done"] = st.checkbox("이 단계를 완료했습니다", value=rec["done"], key=f"done_{idx}")
    rec["note"] = st.text_area("현장 메모", value=rec["note"], key=f"note_{idx}", height=100)

    st.markdown("**📷 현장 사진**")
    uploaded_photos = st.file_uploader(
        "사진 추가 (여러 장 선택 가능, 이미 올린 사진은 목록에서 x로 삭제 가능)",
        type=["png", "jpg", "jpeg", "heic"],
        accept_multiple_files=True,
        key=f"photos_{idx}",
    )
    rec["photos"] = uploaded_photos or []

    if rec["photos"]:
        st.caption(f"이 단계에 첨부된 사진: {len(rec['photos'])}장")
        thumb_cols = st.columns(3)
        for p_idx, photo in enumerate(rec["photos"]):
            with thumb_cols[p_idx % 3]:
                st.image(photo, caption=photo.name, use_container_width=True)
    else:
        st.caption("아직 첨부된 사진이 없습니다.")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("◀ 이전 단계", disabled=(idx == 0)):
            st.session_state.current_index -= 1
            st.rerun()
    with col2:
        if idx < len(steps) - 1:
            if st.button("다음 단계 ▶"):
                st.session_state.current_index += 1
                st.rerun()
        else:
            st.success("마지막 단계입니다. 아래에서 리포트를 다운로드하세요.")
    with col3:
        pass

    st.divider()
    st.markdown("### 📄 리포트 다운로드")
    report_text = build_report_text()
    file_tag = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    total_photos = sum(len(st.session_state.records[i].get("photos") or []) for i in range(len(steps)))

    dcol1, dcol2, dcol3 = st.columns(3)
    with dcol1:
        st.download_button(
            "TXT 리포트 다운로드",
            data=report_text.encode("utf-8"),
            file_name=f"forensic_report_{device_type}_{file_tag}.txt",
            mime="text/plain",
        )
    with dcol2:
        backup = {
            "case_info": st.session_state.case_info,
            "device_type": device_type,
            "steps": [
                {
                    "title": steps[i]["title"],
                    "done": st.session_state.records[i]["done"],
                    "note": st.session_state.records[i]["note"],
                    "photos": [p.name for p in (st.session_state.records[i].get("photos") or [])],
                }
                for i in range(len(steps))
            ],
        }
        st.download_button(
            "JSON 백업 다운로드",
            data=json.dumps(backup, ensure_ascii=False, indent=2).encode("utf-8"),
            file_name=f"forensic_report_{device_type}_{file_tag}.json",
            mime="application/json",
        )
    with dcol3:
        if total_photos > 0:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for i in range(len(steps)):
                    photos = st.session_state.records[i].get("photos") or []
                    step_folder = f"{i:02d}_{steps[i]['title'][:20]}".replace("/", "-")
                    for photo in photos:
                        photo.seek(0)
                        zf.writestr(f"{step_folder}/{photo.name}", photo.read())
            st.download_button(
                f"사진 전체 ZIP ({total_photos}장)",
                data=zip_buffer.getvalue(),
                file_name=f"forensic_photos_{device_type}_{file_tag}.zip",
                mime="application/zip",
            )
        else:
            st.caption("첨부된 사진이 없습니다.")

    with st.expander("전체 단계 한눈에 보기 / 바로 이동"):
        for i, s in enumerate(steps):
            mark = "✅" if st.session_state.records[i]["done"] else "⬜"
            if st.button(f"{mark} {s['title']}", key=f"jump_{i}"):
                st.session_state.current_index = i
                st.rerun()


def main():
    init_state()
    if st.session_state.stage == "start":
        render_start()
    else:
        render_guide()


if __name__ == "__main__":
    main()