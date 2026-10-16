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
import io
import os
import zipfile

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, PageBreak, HRFlowable,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

# ---------------------------------------------------------------------------
# 한글 폰트 탐색 및 등록
# Windows에는 기본적으로 맑은 고딕(malgun.ttf)이 들어있어 별도 폰트 파일
# 없이도 동작한다. 리눅스(Streamlit Community Cloud 등)에 배포하는 경우에는
# packages.txt 에 `fonts-nanum` 을 추가하거나, app.py와 같은 폴더에
# fonts/NanumGothic.ttf 를 넣어두면 자동으로 사용된다.
# ---------------------------------------------------------------------------

_KOREAN_FONT_CANDIDATES = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "NanumGothic.ttf"),
    r"C:\Windows\Fonts\malgun.ttf",
    r"C:\Windows\Fonts\malgunbd.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
]

KOREAN_FONT_NAME = "KoreanFont"


def get_korean_font_path():
    for path in _KOREAN_FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def ensure_korean_font_registered():
    """한글 폰트를 reportlab에 등록한다. 못 찾으면 None을 반환한다."""
    if KOREAN_FONT_NAME in pdfmetrics.getRegisteredFontNames():
        return KOREAN_FONT_NAME
    font_path = get_korean_font_path()
    if not font_path:
        return None
    try:
        pdfmetrics.registerFont(TTFont(KOREAN_FONT_NAME, font_path))
        return KOREAN_FONT_NAME
    except Exception:
        return None

APP_TITLE = "현장 압수 절차 포렌식 매뉴얼 (Digital Forensics Seizure Guide)"

# ---------------------------------------------------------------------------
# 절차 데이터
# ---------------------------------------------------------------------------

DEVICE_SELECT_STEP = {
    "title": "압수 대상 기기 유형 선택",
    "type": "device_select",
    "detail": (
        "현장에서 확보한 기기의 유형을 선택한다. 선택한 유형에 따라 이후\n"
        "단계의 세부 절차(전원/네트워크 보존 방법, 식별 항목, 추출 방식 등)가\n"
        "달라진다."
    ),
    "caution": "여러 기기를 동시에 압수하는 경우, 기기마다 이 프로그램을 별도로 실행하여 각각 기록한다.",
}

COMMON_PRE_STEPS = [
    {
        "title": "현장 안전 및 권한 확인",
        "detail": (
            "- 압수수색영장 등 법적 권한 범위를 먼저 확인한다.\n"
            "- 현장 책임자(소지자/관리자)에게 신분과 목적을 고지한다.\n"
            "- 입회인(참관인) 확보 여부를 확인한다."
        ),
        "caution": "법적 권한 없이는 어떠한 기기도 조작/압수하지 않는다.",
    },
    {
        "title": "현장 사진/영상 기록",
        "detail": (
            "- 기기의 위치, 화면 상태(켜짐/꺼짐), 주변 배선, 연결된 주변기기를 촬영한다.\n"
            "- 타임스탬프가 남도록 촬영하고, 전체 현장 → 기기 근접 순으로 기록한다."
        ),
        "caution": "사진 촬영 전에는 어떤 기기도 만지지 않는다.",
    },
]

PC_STEPS = COMMON_PRE_STEPS + [
    {
        "title": "전원 상태 확인 및 네트워크 차단 검토",
        "detail": (
            "[전원 상태]\n"
            "- 모니터 화면과 본체 상태(LED, 팬 소음 등)로 전원 ON/OFF를 확인한다.\n"
            "- 화면이 켜져 있다면 현재 실행 중인 프로그램/화면을 그대로 촬영한다.\n\n"
            "[네트워크 차단 검토]\n"
            "- 원격 삭제/암호화/동기화를 막기 위해 랜케이블 분리, Wi-Fi 차단을\n"
            "  검토한다.\n"
            "- 휘발성 데이터(RAM) 수집이 필요한 경우, 네트워크 차단 시점과 방법을\n"
            "  미리 정한다."
        ),
        "caution": (
            "전원이 꺼져 있다면 절대 켜지 않는다. 켜져 있다면 임의로 끄지 않는다. "
            "네트워크 차단이 오히려 증거를 훼손할 수 있는 경우도 있으니 사전 "
            "교육된 절차를 따른다."
        ),
    },
    {
        "title": "휘발성 메모리(RAM) 수집 판단 및 저장매체 식별",
        "detail": (
            "- 기기가 켜져 있고 암호화(BitLocker 등)가 의심되는 경우, RAM 이미징을\n"
            "  통한 복호화 키 확보가 필요한지 판단한다.\n"
            "- HDD/SSD/M.2 등 저장매체 모델명, 용량, 일련번호를 식별·기록한다."
        ),
        "caution": "비전문 인력이 임의 프로그램을 설치/실행하면 증거가 훼손될 수 있다.",
        "role_override": {
            "수사관": {
                "detail": (
                    "- 기기가 켜져 있고 암호화가 의심되는 경우, RAM 수집이 필요한지는\n"
                    "  동행한 포렌식 분석관과 협의하여 판단한다.\n"
                    "- 저장매체(HDD/SSD/M.2 등) 식별도 분석관과 함께 확인한다.\n"
                    "- 수사관 단독으로 RAM 수집 도구를 설치/실행하지 않는다."
                ),
            },
            "포렌식분석관": {
                "detail": (
                    "- 기기가 켜져 있고 암호화(BitLocker 등)가 의심되는 경우, RAM\n"
                    "  이미징을 통한 복호화 키 확보 필요 여부를 직접 판단한다.\n"
                    "- RAM 수집이 필요하면 보유 장비로 직접 수행한다.\n"
                    "- 저장매체 모델명, 용량, 일련번호를 식별·기록한다."
                ),
            },
        },
    },
    {
        "title": "전원 차단, 케이블 라벨링 및 쓰기방지장치 준비",
        "detail": (
            "- 휘발성 데이터, 암호화 상태, 시스템 안정성 및 기관 SOP를 고려해 종료 방법을\n"
            "  결정한다. 전원 차단은 데이터 손실·변경을 유발할 수 있으므로 임의로 수행하지 않는다.\n"
            "- 모든 케이블에 라벨을 붙이고 연결 위치를 사진으로 남긴 뒤 분리한다.\n"
            "- 이미징 시 반드시 쓰기방지장치(Write Blocker)를 사용하여 원본이\n"
            "  변경되지 않도록 준비한다."
        ),
        "caution": "노트북 배터리 분리 등 물리적 조작은 기기 구조와 보존 목표에 따라 승인된 절차로 수행한다. 쓰기방지장치 없이 원본 저장매체를 분석용 PC에 직접 연결하지 않는다.",
    },
    {
        "title": "현장 이미지 추출 여부 결정",
        "type": "decision",
        "options": ["현장 즉시 이미지 추출", "압수 후 실험실 이송", "보류 (책임자 추가 판단 필요)"],
        "detail": (
            "현장에서 바로 저장매체를 이미징할지, PC 또는 저장매체를 압수해\n"
            "실험실로 옮긴 뒤 처리할지를 아래 기준으로 판단해 선택한다. 동행한\n"
            "포렌식 분석관과 협의하여 결정한다.\n\n"
            "판단 기준:\n"
            "- 시간 민감성: 암호화 재잠금, 시스템 자동 종료 위험이 임박했는가\n"
            "- 현장 장비: 공인 이미징 장비와 전문 인력이 현장에 있는가\n"
            "- 공간/환경: 전력, 작업 테이블 등 여건이 되는가\n"
            "- 법적 권한 범위: 영장/동의 범위가 현장 이미징까지 포함하는가\n"
            "- 증거 복잡성: 대용량 저장소, RAID 구성 등으로 실험실 정밀 분석이\n"
            "  필요한 상황인가"
        ),
        "caution": "결정 권한은 현장 책임자(또는 기관 SOP가 지정한 담당자)에게 있다. 애매하면 '보류'를 선택하고 책임자 지시를 받는다.",
        "branch_info": {
            "현장 즉시 이미지 추출": (
                "→ 전력, 공간 등 현장 작업 여건을 지원하며 공인 장비로 이미징한다.\n"
                "   작업 시작/종료 시각, 사용 장비명, 담당자를 기록한다. 추출된\n"
                "   사본의 압수·보관·교부 여부와 범위는 영장 문언, 혐의사실 관련성, 선별 절차\n"
                "   및 적용 법령·판례에 따라 책임자가 판단한다. 해시값·교부 내역을 기록한다."
            ),
            "압수 후 실험실 이송": (
                "→ PC 또는 저장매체를 봉인하여 실험실로 이송한다. 이송 책임자와\n"
                "   시각을 기록한다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "→ 책임자 지시가 있을 때까지 현재 보존 상태를 유지한다. 판단이\n"
                "   내려지면 이 선택을 다시 바꾸고 사유를 메모에 남긴다."
            ),
        },
    },
    {
        "title": "포렌식 이미징 및 해시값 기록",
        "detail": (
            "- 공인 포렌식 이미징 도구로 비트 단위 이미지를 생성한다.\n"
            "- 기관 SOP에 따라 SHA-256 해시값을 산출·기록한다. 필요한 경우 보조 해시를\n"
            "  추가하되, 해시 일치만으로 수집 절차 전체의 적법성이 증명되는 것은 아니다."
        ),
        "caution": "해시값이 다르면 반드시 원인을 기록하고 재시도한다.",
        "tool_select": True,
        "role_override": {
            "수사관": {
                "detail": (
                    "- 포렌식 이미징은 동행한 포렌식 분석관이 보유 장비로 직접\n"
                    "  수행한다. 수사관은 해시값과 사용 장비명을 전달받아 기록한다."
                ),
            },
            "포렌식분석관": {
                "detail": (
                    "- 보유 장비 중 이 매체에 적합한 도구를 선택하여 비트 단위\n"
                    "  이미지를 생성한다.\n"
                    "- 기관 SOP에 따라 SHA-256 해시값을 산출·기록한다. 필요한 경우 보조 해시를\n"
                    "  추가하며, 해시 일치와 절차 적법성은 구분해 판단한다."
                ),
            },
        },
        "variants": {
            "현장 즉시 이미지 추출": (
                "[현장 추출 선택됨] 작업 종료 후 해시값, 추출 범위, 파일 목록, 교부·보관 여부를\n"
                "기록하고 필요한 서류를 교부한다. 사본의 법적 지위는 일률적으로 단정하지 말고\n"
                "영장 범위와 관련성 선별 결과에 따라 책임자가 확인한다."
            ),
            "압수 후 실험실 이송": (
                "[실험실 이송 선택됨] 현장에서는 이미징하지 않고 '이송 전 봉인'까지만\n"
                "진행한다. 실험실 도착 후 공인 인력이 이미징을 수행한다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "[보류 선택됨] 책임자 지시가 내려온 뒤 진행한다."
            ),
        },
    },
    {
        "title": "증거물 포장 및 봉인",
        "detail": (
            "- 정전기 방지 봉투(Anti-static bag)에 저장매체를 담는다.\n"
            "- 봉인 스티커에 서명/날짜를 기입하고 봉인 상태를 사진으로 남긴다."
        ),
        "caution": "충격/자기장에 노출되지 않도록 운반에 유의한다.",
        "variants": {
            "현장 즉시 이미지 추출": (
                "[현장 추출] 원본 및 추출 사본 각각의 보관·교부·압수 여부를 책임자가 확정한다.\n"
                "해시값, 선별 범위, 교부확인 및 처리 근거를 기록하고, 압수 대상은 적법한\n"
                "절차에 따라 포장·봉인한다."
            ),
            "압수 후 실험실 이송": (
                "[실험실 이송] 원본(PC 또는 저장매체)을 포장·봉인한다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "[보류] 결정 전까지는 보존 상태만 유지하고, 최종 포장은 경로가\n"
                "확정된 뒤 진행한다."
            ),
        },
    },
    {
        "title": "증거물 목록 및 인수인계 기록 작성",
        "detail": (
            "- 압수물 목록(품명, 수량, 일련번호, 상태)을 작성한다.\n"
            "- Chain of Custody(증거보관연계) 문서에 담당자, 시각, 장소를 기록한다."
        ),
        "caution": "이후 모든 취급자는 인계 시점마다 서명을 남긴다.",
        "variants": {
            "현장 즉시 이미지 추출": (
                "[현장 추출] 실제 압수한 물건·전자정보를 구분해 목록화한다. 추출 사본의\n"
                "해시값, 선별 범위, 교부·보관 내역과 처리 근거를 별도 서식에도 기록하고\n"
                "압수목록과 상호 참조되도록 사건기록에 첨부한다."
            ),
            "압수 후 실험실 이송": (
                "[실험실 이송] 목록에 이송 경로(출발지→도착지), 이송 담당자,\n"
                "이송 수단을 함께 기재한다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "[보류] 최종 경로가 정해지면 이 목록에 사후 기재하고, 보류 기간\n"
                "동안의 보관 책임자를 명시해 둔다."
            ),
        },
    },
]

IPHONE_STEPS = COMMON_PRE_STEPS + [
    {
        "title": "전원 상태 확인 및 네트워크·배터리 보존",
        "detail": (
            "[전원/잠금 상태]\n"
            "- 화면이 켜져 있는지, 잠금(Lock) 상태인지 확인하고 촬영한다.\n"
            "- 켜져 있다면 전원을 끄지 않는다(끄면 재부팅 후 암호화가 강화되어\n"
            "  이후 접근이 더 어려워질 수 있다).\n\n"
            "[네트워크 격리]\n"
            "- 'iPhone 찾기'를 통한 원격 삭제를 막기 위해 가능한 한 빨리\n"
            "  네트워크로부터 격리한다.\n"
            "- 방법: 페러데이백(Faraday bag)에 넣거나, 비행기 모드 전환,\n"
            "  또는 SIM 제거를 기관 SOP에 따라 선택한다.\n\n"
            "[배터리 방전 방지]\n"
            "- 페러데이백 전용 충전 케이블 또는 보조배터리를 사용한다."
        ),
        "caution": (
            "꺼져 있던 기기라면 임의로 전원을 켜지 않는다. 화면 조작이 필요한 "
            "경우 조작 전후 과정을 반드시 촬영/기록한다. 충전 중에도 네트워크 "
            "격리 상태가 유지되는지 확인한다."
        ),
    },
    {
        "title": "기기 식별 및 보안상태 확인 (포렌식 분석관과 공동 진행)",
        "detail": (
            "이 단계는 전문적인 기술 판단이 포함되어 있어 현장 수사관 단독으로\n"
            "진행하기 어렵다. 압수 현장에 동행한 포렌식 분석관과 함께 아래 항목을\n"
            "협의하여 확인·기록한다.\n\n"
            "- 모델명, iOS 버전, 일련번호/IMEI(화면/기기 라벨에서 확인 가능한 범위)\n"
            "- Face ID / Touch ID 사용 여부\n"
            "- 화면에 노출된 Apple ID / iCloud 계정 정보"
        ),
        "caution": (
            "잠금 해제를 시도하며 정보를 캐내려 하지 않는다. 화면에 보이는 정보만 "
            "기록하며, 판단이 어려운 항목은 동행한 포렌식 분석관의 의견에 따른다."
        ),
        "role_override": {
            "포렌식분석관": {
                "detail": (
                    "- 모델명, iOS 버전, 일련번호/IMEI(화면/기기 라벨에서 확인 가능한\n"
                    "  범위), Face ID/Touch ID 사용 여부, 화면에 노출된 Apple ID/\n"
                    "  iCloud 계정 정보를 직접 확인·기록한다."
                ),
            },
        },
    },
    {
        "title": "현장 이미지 추출 여부 결정",
        "type": "decision",
        "options": ["현장 즉시 이미지 추출", "압수 후 실험실 이송", "보류 (책임자 추가 판단 필요)"],
        "detail": (
            "현장에서 바로 이미지를 뜰지, 기기를 압수해 실험실로 옮긴 뒤 처리할지를\n"
            "아래 기준으로 판단해 선택한다. 동행한 포렌식 분석관과 협의하여\n"
            "결정한다.\n\n"
            "판단 기준:\n"
            "- 시간 민감성: 배터리 소진, 자동 재잠금, 원격 삭제 위험이 임박했는가\n"
            "- 현장 장비: 공인 추출 장비와 전문 인력이 현장에 있는가\n"
            "- 공간/환경: 전력, 차폐(페러데이백/차폐룸), 작업 테이블 등 여건이 되는가\n"
            "- 법적 권한 범위: 영장/동의 범위가 현장 추출까지 포함하는가\n"
            "- 증거 복잡성: 다수 기기·대용량 저장소 등으로 실험실 정밀 분석이\n"
            "  필요한 상황인가"
        ),
        "caution": "결정 권한은 현장 책임자(또는 기관 SOP가 지정한 담당자)에게 있다. 애매하면 '보류'를 선택하고 책임자 지시를 받는다.",
        "branch_info": {
            "현장 즉시 이미지 추출": (
                "→ 전력, 공간, 네트워크 차폐 환경을 지원하며 공인 장비로 작업한다.\n"
                "   추출 시작/종료 시각, 사용 장비명, 담당자를 기록한다. 추출된\n"
                "   사본의 압수·보관·교부 여부와 범위는 영장 문언, 혐의사실 관련성 및 선별 절차에\n"
                "   따라 책임자가 판단한다. 해시값과 처리 내역을 기록한다."
            ),
            "압수 후 실험실 이송": (
                "→ 기기를 봉인하여 실험실로 이송한다. 이송 중에도 네트워크 격리와\n"
                "   배터리 방전 방지가 유지되는지 확인하고, 이송 책임자와 시각을\n"
                "   기록한다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "→ 책임자 지시가 있을 때까지 현재 보존 상태(격리/충전)를 유지한다.\n"
                "   판단이 내려지면 이 선택을 다시 바꾸고 사유를 메모에 남긴다."
            ),
        },
    },
    {
        "title": "잠금해제/복호화 - 전문 추출팀 인계 체크리스트",
        "detail": (
            "실제 잠금해제·복호화 작업은 공인 장비(Cellebrite UFED, GrayKey 등)와\n"
            "자격을 갖춘 전문 추출팀만 수행한다. 현장 담당자는 아래 정보를\n"
            "빠짐없이 기록해 전문팀에 인계한다.\n\n"
            "- 기기 모델명 / iOS 버전\n"
            "- Face ID / Touch ID 사용 여부\n"
            "- 마지막 잠금 해제로부터 경과 시간(가능한 범위에서 추정)\n"
            "- 배터리 잔량(%)\n"
            "- USB 제한 모드 활성 가능성(장시간 미사용 여부로 추정)\n"
            "- 화면에 노출된 Apple ID / iCloud 계정 정보\n"
            "- SIM 카드 장착 여부 및 통신사\n"
            "- 페러데이백/증거백 봉인 상태"
        ),
        "caution": "현장 담당자는 잠금 해제 코드를 추측하거나, 소지자에게 암호 제공을 강요하지 않는다. 암호 제공 요구는 법적 근거(영장 범위, 소지자 동의 등)가 있는 경우에만 지정된 절차로 진행한다.",
        "variants": {
            "현장 즉시 이미지 추출": (
                "[현장 추출 선택됨] 위 체크리스트는 현장에 도착할 전문 추출팀에게\n"
                "그 자리에서 바로 구두+서면으로 전달한다. 전문팀 도착 예정 시각을\n"
                "메모에 기록해 둔다."
            ),
            "압수 후 실험실 이송": (
                "[실험실 이송 선택됨] 위 체크리스트는 기기와 함께 이송 서류에\n"
                "동봉하여 실험실 인수자에게 전달한다. 체크리스트 작성 후에는\n"
                "기기에 더 이상 어떠한 조작도 가하지 않는다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "[보류 선택됨] 체크리스트는 책임자 판단을 돕기 위해 미리 작성해\n"
                "두되, 전문팀 인계나 이송은 책임자 지시가 내려온 뒤 진행한다."
            ),
        },
        "role_override": {
            "포렌식분석관": {
                "caution": "본인이 직접 공인 장비로 진행할 항목이므로, 위 정보를 스스로 확인·기록한 뒤 보유 장비로 작업을 시작한다.",
            },
        },
    },
    {
        "title": "전문 추출팀 인계",
        "detail": (
            "- 법적 권한과 절차에 따라 공인 모바일 포렌식 장비를 보유한\n"
            "  전문 인력에게 인계한다.\n"
            "- 위 체크리스트와 앞선 '현장 이미지 추출 여부 결정' 단계에서 선택한 처리 방식을\n"
            "  함께 전달한다."
        ),
        "caution": "비전문 인력이 임의 소프트웨어로 추출을 시도하면 증거능력이 부정될 수 있다.",
        "tool_select": True,
        "variants": {
            "현장 즉시 이미지 추출": (
                "[현장 추출] 전문 추출팀이 현장에서 작업을 완료할 때까지 입회\n"
                "하거나 대기 담당자를 지정한다. 작업 종료 후 산출된 해시값\n"
                "(SHA-256)을 전문팀으로부터 받아, 그 자리에서 피의자(소지자)에게\n"
                "고지·교부 등 필요한 조치를 기록한다. 추출 사본의 압수·보관·교부 여부는\n"
                "영장 범위와 관련성 선별 결과에 따라 책임자가 확인하며, 원본 처리도 별도 기록한다."
            ),
            "압수 후 실험실 이송": (
                "[실험실 이송] 현장에서는 인계가 아닌 '이송 전 봉인'까지만 진행\n"
                "한다. 실험실 도착 후 공인 인력이 봉인을 개봉하며 작업을\n"
                "시작하고, 개봉 시각과 담당자를 별도로 기록한다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "[보류] 아직 인계 대상이 정해지지 않았으므로 이 단계는 보류한다.\n"
                "책임자의 결정이 내려오면 앞선 결정 단계로 돌아가 선택을 변경한 뒤 다시\n"
                "진행한다."
            ),
        },
        "role_override": {
            "수사관": {
                "title_display": "전문 추출팀 인계",
            },
            "포렌식분석관": {
                "detail": (
                    "- 본인이 보유 장비 중 이 사건에 적합한 도구를 선택해 직접\n"
                    "  추출을 수행한다. 별도의 인계 절차는 없으며, 작업 시작/종료\n"
                    "  시각과 산출된 해시값을 스스로 기록한다."
                ),
                "caution": "본인이 직접 작업하더라도 모든 조작 과정은 기록하고, 해시값 검증 없이 결과를 확정하지 않는다.",
            },
        },
    },
    {
        "title": "증거물 포장 및 봉인",
        "detail": "- 페러데이백째로 정전기 방지 봉투에 추가 포장, 봉인 스티커 서명/날짜 기입 및 촬영.",
        "caution": "운반 중 충격, 고온, 자기장 노출 주의.",
        "variants": {
            "현장 즉시 이미지 추출": (
                "[현장 추출] 원본과 추출 사본 각각의 압수·보관·교부 여부를 책임자가 확정한다.\n"
                "해시값, 선별 범위, 처리 근거와 교부 내역을 기록하고 해당하는 증거물은\n"
                "적법한 절차에 따라 포장·봉인한다."
            ),
            "압수 후 실험실 이송": (
                "[실험실 이송] 원본만 포장/봉인하며, 추출은 실험실에서 진행되므로\n"
                "이 시점에는 사본이 없다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "[보류] 결정 전까지는 보존 상태(격리/충전)만 유지하고, 최종 포장은\n"
                "경로가 확정된 뒤 진행한다."
            ),
        },
    },
    {
        "title": "증거물 목록 및 인수인계 기록 작성",
        "detail": "- 압수물 목록과 Chain of Custody 문서를 작성한다.",
        "caution": "모든 접촉/이동 이력을 빠짐없이 기록한다.",
        "variants": {
            "현장 즉시 이미지 추출": (
                "[현장 추출] 실제 압수한 물건·전자정보를 구분해 목록화한다. 추출 사본의\n"
                "해시값, 선별 범위, 교부·보관 내역과 처리 근거도 별도 서식에 기록하고\n"
                "압수목록과 상호 참조되도록 사건기록에 첨부한다."
            ),
            "압수 후 실험실 이송": (
                "[실험실 이송] 목록에 이송 경로(출발지→도착지), 이송 담당자,\n"
                "이송 수단을 함께 기재한다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "[보류] 최종 경로가 정해지면 이 목록에 사후 기재하고, 보류 기간\n"
                "동안의 보관 책임자를 명시해 둔다."
            ),
        },
    },
]

ANDROID_STEPS = COMMON_PRE_STEPS + [
    {
        "title": "전원 상태 확인 및 네트워크·배터리 보존",
        "detail": (
            "[전원/화면 상태]\n"
            "- 화면 켜짐/꺼짐, 잠금 여부를 확인하고 촬영한다.\n"
            "- 켜져 있다면 전원을 끄지 않는다.\n\n"
            "[네트워크 격리]\n"
            "- 원격 초기화(Find My Device 등) 방지를 위해 네트워크로부터 격리한다.\n"
            "- 방법: 페러데이백 사용, 비행기 모드, 또는 기관 SOP에 따른 방법.\n\n"
            "[배터리 방전 방지]\n"
            "- 전원이 꺼지지 않도록 페러데이백 전용 충전 케이블 또는 보조배터리를\n"
            "  연결한다."
        ),
        "caution": (
            "꺼져 있던 기기라면 임의로 전원을 켜지 않는다. 화면 조작이 필요하면 "
            "과정을 반드시 촬영/기록한다. 충전 중에도 네트워크 격리 상태가 "
            "유지되는지 확인한다."
        ),
    },
    {
        "title": "기기 식별 및 보안상태 확인 (포렌식 분석관과 공동 진행)",
        "detail": (
            "이 단계는 전문적인 기술 판단이 포함되어 있어 현장 수사관 단독으로\n"
            "진행하기 어렵다. 압수 현장에 동행한 포렌식 분석관과 함께 아래 항목을\n"
            "협의하여 확인·기록한다.\n\n"
            "- 제조사/모델명, Android 버전, IMEI/시리얼\n"
            "- USB 디버깅 활성화 여부(화면상 확인 가능한 경우)\n"
            "- 루팅 여부(추정), 개발자 옵션 활성화 여부"
        ),
        "caution": (
            "잠금 해제를 시도하거나 코드를 추측하지 않는다. 직접 설정을 변경하지 "
            "않으며, 판단이 어려운 항목은 동행한 포렌식 분석관의 의견에 따른다."
        ),
        "role_override": {
            "포렌식분석관": {
                "detail": (
                    "- 제조사/모델명, Android 버전, IMEI/시리얼, USB 디버깅 활성화\n"
                    "  여부, 루팅 여부(추정), 개발자 옵션 활성화 여부를 직접\n"
                    "  확인·기록한다."
                ),
            },
        },
    },
    {
        "title": "현장 이미지 추출 여부 결정",
        "type": "decision",
        "options": ["현장 즉시 이미지 추출", "압수 후 실험실 이송", "보류 (책임자 추가 판단 필요)"],
        "detail": (
            "현장에서 전문 추출팀이 바로 이미지를 뜰지, 기기를 압수해 실험실로\n"
            "옮긴 뒤 처리할지를 아래 기준으로 판단해 선택한다. 동행한 포렌식\n"
            "분석관과 협의하여 결정한다.\n\n"
            "판단 기준:\n"
            "- 시간 민감성: 배터리 소진, 자동 재잠금, 원격 초기화 위험이 임박했는가\n"
            "- 현장 장비: 공인 추출 장비(Cellebrite, XRY 등)와 전문 인력이 현장에 있는가\n"
            "- 공간/환경: 전력, 차폐(페러데이백/차폐룸), 작업 테이블 등 여건이 되는가\n"
            "- 법적 권한 범위: 영장/동의 범위가 현장 추출까지 포함하는가\n"
            "- 증거 복잡성: 다수 기기·대용량 저장소 등으로 실험실 정밀 분석이\n"
            "  필요한 상황인가"
        ),
        "caution": "결정 권한은 현장 책임자(또는 기관 SOP가 지정한 담당자)에게 있다. 애매하면 '보류'를 선택하고 책임자 지시를 받는다.",
        "branch_info": {
            "현장 즉시 이미지 추출": (
                "→ 전문 추출팀이 현장에서 공인 장비로 작업할 수 있도록 전력, 공간,\n"
                "   네트워크 차폐 환경을 지원한다. 추출 시작/종료 시각, 사용 장비명,\n"
                "   담당자를 기록한다. 사본의 압수·보관·교부 여부와 범위는 영장 문언,\n"
                "   혐의사실 관련성 및 선별 절차에 따라 책임자가 판단하고 처리 내역을 기록한다."
            ),
            "압수 후 실험실 이송": (
                "→ 기기를 봉인하여 실험실로 이송한다. 이송 중에도 네트워크 격리와\n"
                "   배터리 방전 방지가 유지되는지 확인하고, 이송 책임자와 시각을\n"
                "   기록한다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "→ 책임자 지시가 있을 때까지 현재 보존 상태(격리/충전)를 유지한다.\n"
                "   판단이 내려지면 이 선택을 다시 바꾸고 사유를 메모에 남긴다."
            ),
        },
    },
    {
        "title": "잠금해제/복호화 - 전문 추출팀 인계 체크리스트",
        "detail": (
            "실제 잠금해제·복호화 작업은 공인 장비(Cellebrite, MSAB XRY 등)와\n"
            "자격을 갖춘 전문 추출팀만 수행한다. 현장 담당자는 아래 정보를\n"
            "빠짐없이 기록해 전문팀에 인계한다.\n\n"
            "- 제조사/모델명 / Android 버전 / 보안 패치 수준\n"
            "- 지문/얼굴 인식 등 생체인증 사용 여부\n"
            "- 마지막 잠금 해제로부터 경과 시간(가능한 범위에서 추정)\n"
            "- 배터리 잔량(%)\n"
            "- USB 디버깅 활성화 여부(화면상 확인 가능한 경우)\n"
            "- 루팅 여부(추정)\n"
            "- 화면에 노출된 구글 계정 정보\n"
            "- SIM 카드 장착 여부 및 통신사\n"
            "- 페러데이백/증거백 봉인 상태"
        ),
        "caution": "현장 담당자는 잠금 해제 코드를 추측하거나, 소지자에게 암호 제공을 강요하지 않는다. 암호 제공 요구는 법적 근거(영장 범위, 소지자 동의 등)가 있는 경우에만 지정된 절차로 진행한다.",
        "variants": {
            "현장 즉시 이미지 추출": (
                "[현장 추출 선택됨] 위 체크리스트는 현장에 도착할 전문 추출팀에게\n"
                "그 자리에서 바로 구두+서면으로 전달한다. 전문팀 도착 예정 시각을\n"
                "메모에 기록해 둔다."
            ),
            "압수 후 실험실 이송": (
                "[실험실 이송 선택됨] 위 체크리스트는 기기와 함께 이송 서류에\n"
                "동봉하여 실험실 인수자에게 전달한다. 체크리스트 작성 후에는\n"
                "기기에 더 이상 어떠한 조작도 가하지 않는다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "[보류 선택됨] 체크리스트는 책임자 판단을 돕기 위해 미리 작성해\n"
                "두되, 전문팀 인계나 이송은 책임자 지시가 내려온 뒤 진행한다."
            ),
        },
        "role_override": {
            "포렌식분석관": {
                "caution": "본인이 직접 공인 장비로 진행할 항목이므로, 위 정보를 스스로 확인·기록한 뒤 보유 장비로 작업을 시작한다.",
            },
        },
    },
    {
        "title": "전문 추출팀 인계",
        "detail": (
            "- 공인 모바일 포렌식 장비를 보유한 전문 인력에게 법적 절차에 따라\n"
            "  인계한다.\n"
            "- 위 체크리스트와 앞선 '현장 이미지 추출 여부 결정' 단계에서 선택한 처리 방식을\n"
            "  함께 전달한다."
        ),
        "caution": "비전문 인력의 임의 추출 시도는 증거능력을 저해할 수 있다.",
        "tool_select": True,
        "role_override": {
            "포렌식분석관": {
                "detail": (
                    "- 본인이 보유 장비 중 이 사건에 적합한 도구를 선택해 직접\n"
                    "  추출을 수행한다. 별도의 인계 절차는 없으며, 작업 시작/종료\n"
                    "  시각과 산출된 해시값을 스스로 기록한다."
                ),
                "caution": "본인이 직접 작업하더라도 모든 조작 과정은 기록하고, 해시값 검증 없이 결과를 확정하지 않는다.",
            },
        },
        "variants": {
            "현장 즉시 이미지 추출": (
                "[현장 추출] 전문 추출팀이 현장에서 작업을 완료할 때까지 입회\n"
                "하거나 대기 담당자를 지정한다. 작업 종료 후 산출된 해시값\n"
                "(SHA-256)을 전문팀으로부터 받아, 그 자리에서 피의자(소지자)에게\n"
                "고지·교부 등 필요한 조치를 기록한다. 추출 사본의 압수·보관·교부 여부는\n"
                "영장 범위와 관련성 선별 결과에 따라 책임자가 확인하며, 원본 처리도 별도 기록한다."
            ),
            "압수 후 실험실 이송": (
                "[실험실 이송] 현장에서는 인계가 아닌 '이송 전 봉인'까지만 진행\n"
                "한다. 실험실 도착 후 공인 인력이 봉인을 개봉하며 작업을\n"
                "시작하고, 개봉 시각과 담당자를 별도로 기록한다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "[보류] 아직 인계 대상이 정해지지 않았으므로 이 단계는 보류한다.\n"
                "책임자의 결정이 내려오면 앞선 결정 단계로 돌아가 선택을 변경한 뒤 다시\n"
                "진행한다."
            ),
        },
    },
    {
        "title": "증거물 포장 및 봉인",
        "detail": "- 정전기 방지 봉투/페러데이백 포장 후 봉인 스티커 서명/날짜 기입.",
        "caution": "운반 중 충격, 고온 주의.",
        "variants": {
            "현장 즉시 이미지 추출": (
                "[현장 추출] 원본과 추출 사본 각각의 압수·보관·교부 여부를 책임자가 확정한다.\n"
                "해시값, 선별 범위, 처리 근거와 교부 내역을 기록하고 해당하는 증거물은\n"
                "적법한 절차에 따라 포장·봉인한다."
            ),
            "압수 후 실험실 이송": (
                "[실험실 이송] 원본만 포장/봉인하며, 추출은 실험실에서 진행되므로\n"
                "이 시점에는 사본이 없다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "[보류] 결정 전까지는 보존 상태(격리/충전)만 유지하고, 최종 포장은\n"
                "경로가 확정된 뒤 진행한다."
            ),
        },
    },
    {
        "title": "증거물 목록 및 인수인계 기록 작성",
        "detail": "- 압수물 목록과 Chain of Custody 문서를 작성한다.",
        "caution": "모든 접촉/이동 이력을 빠짐없이 기록한다.",
        "variants": {
            "현장 즉시 이미지 추출": (
                "[현장 추출] 실제 압수한 물건·전자정보를 구분해 목록화한다. 추출 사본의\n"
                "해시값, 선별 범위, 교부·보관 내역과 처리 근거도 별도 서식에 기록하고\n"
                "압수목록과 상호 참조되도록 사건기록에 첨부한다."
            ),
            "압수 후 실험실 이송": (
                "[실험실 이송] 목록에 이송 경로(출발지→도착지), 이송 담당자,\n"
                "이송 수단을 함께 기재한다."
            ),
            "보류 (책임자 추가 판단 필요)": (
                "[보류] 최종 경로가 정해지면 이 목록에 사후 기재하고, 보류 기간\n"
                "동안의 보관 책임자를 명시해 둔다."
            ),
        },
    },
]

DEVICE_STEPS = {"PC": PC_STEPS, "iPhone": IPHONE_STEPS, "Android": ANDROID_STEPS}


def get_full_steps(device_type):
    """현장 안전·권한 확인 후 기기 유형을 선택하고, 사진 기록과 기기별 절차를 이어서 반환한다.

    기기 유형을 아직 선택하지 않은 경우에는 사전 확인과 유형 선택까지만 표시한다.
    """
    safety_step = COMMON_PRE_STEPS[0]
    photo_step = COMMON_PRE_STEPS[1]
    steps = [safety_step, DEVICE_SELECT_STEP]
    if device_type:
        # 공통 사전단계 중 안전·권한 확인은 이미 첫 단계에 배치했으므로,
        # 기기별 목록에서는 사진 기록 이후의 기기별 단계만 덧붙인다.
        device_specific_steps = DEVICE_STEPS[device_type][len(COMMON_PRE_STEPS):]
        steps.extend([photo_step])
        steps.extend(device_specific_steps)
    return steps

# ---------------------------------------------------------------------------
# 현장 수행 주체 및 보유 포렌식 도구
# ---------------------------------------------------------------------------

ROLE_OPTIONS = ["수사관", "포렌식분석관"]

TOOLS_BY_DEVICE = {
    "PC": ["디지털 콜렉터", "DFT", "AXIOM"],
    "iPhone": ["MD-NEXT", "인사이트 UFED (Cellebrite)", "AXIOM"],
    "Android": ["MD-NEXT", "인사이트 UFED (Cellebrite)", "AXIOM"],
}


def get_role_text(step, role):
    """역할(수사관/포렌식분석관)에 따라 조정된 (detail, caution)을 반환한다.
    role_override에 해당 role의 값이 있으면 그 값으로 덮어쓰고, 없으면 기본값을 쓴다."""
    detail = step.get("detail", "")
    caution = step.get("caution", "")
    override = (step.get("role_override") or {}).get(role)
    if override:
        detail = override.get("detail", detail)
        caution = override.get("caution", caution)
    return detail, caution


def get_selected_decision(steps, records):
    """이 기기 유형의 단계들 중 'decision' 타입 단계에서 선택된 값을 반환한다.
    (decision 단계는 기기당 하나뿐이라고 가정)"""
    for i, s in enumerate(steps):
        if s.get("type") == "decision":
            val = records.get(i, {}).get("decision")
            if val:
                return val
    return None


def get_decision_step_index(steps):
    for i, s in enumerate(steps):
        if s.get("type") == "decision":
            return i
    return None


def get_effective_last_index(steps, records, role):
    """수사관은 4단계까지 진행하고, 이후의 기술적 절차는 포렌식분석관이 수행한다."""
    if role == "수사관":
        return min(3, len(steps) - 1)
    return len(steps) - 1


def get_skipped_step_indices(steps, records, role):
    """포렌식분석관이 현장 즉시 이미지 추출을 선택하면 포장·봉인 단계를 생략한다."""
    if role != "포렌식분석관":
        return set()
    if get_selected_decision(steps, records) != "현장 즉시 이미지 추출":
        return set()
    return {
        i for i, step in enumerate(steps)
        if step.get("title") == "증거물 포장 및 봉인"
    }


def get_visible_step_indices(steps, records, role):
    """생략 대상만 제외한 전체 단계 인덱스. 역할별 진행/다운로드 제한은 호출부에서 적용한다."""
    skipped = get_skipped_step_indices(steps, records, role)
    return [i for i in range(len(steps)) if i not in skipped]

# ---------------------------------------------------------------------------
# Streamlit 앱
# ---------------------------------------------------------------------------

st.set_page_config(page_title=APP_TITLE, page_icon="🔎", layout="centered")


def init_state():
    defaults = {
        "stage": "start",          # "start" | "guide"
        "device_type": None,
        "role": None,              # "수사관" | "포렌식분석관"
        "current_index": 0,
        "case_info": {},
        "records": {},             # {step_index: {"done": bool, "note": str, "photos": [...], "decision": str, "tool": str}}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def render_start():
    st.title("현장 압수 절차")

    with st.form("case_info_form"):
        case_number = st.text_input("사건번호")
        officer = st.text_input("담당 수사관 (성명/소속)")
        suspect = st.text_input("피의자(소지자) 성명")
        location = st.text_input("현장 위치")
        seized_at = st.text_input(
            "압수 일시 (YYYY-MM-DD HH:MM)",
            value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
        role = st.radio(
            "현장 수행 주체",
            ROLE_OPTIONS,
            horizontal=True,
            help="수사관: 현장 보존·협의 중심 절차. 포렌식분석관: 본인이 직접 기술 항목과 추출 작업을 수행하는 절차.",
        )
        submitted = st.form_submit_button("절차 안내 시작 ▶")

    if submitted:
        st.session_state.case_info = {
            "사건번호": case_number,
            "담당 수사관": officer,
            "피의자(소지자) 성명": suspect,
            "현장 위치": location,
            "압수 일시": seized_at,
        }
        st.session_state.device_type = None  # 현장 안전·권한 확인 후 기기 유형 선택
        st.session_state.role = role
        st.session_state.current_index = 0
        st.session_state.records = {}
        st.session_state.stage = "guide"
        st.rerun()

    st.info(
        "※ 본 프로그램은 현장 보존 절차(사진기록, 전원상태, 네트워크 차단, 해시기록, "
        "Chain of Custody 등) 안내용입니다. 잠금해제·데이터추출 등 기술적 작업은 "
        "법적 권한을 가진 전문 인력이 공인 장비로 수행해야 합니다."
    )


def _pdf_styles(font_name):
    styles = getSampleStyleSheet()
    base = font_name or "Helvetica"
    return {
        "title": ParagraphStyle(
            "KTitle", parent=styles["Title"], fontName=base, fontSize=18, leading=22,
        ),
        "meta": ParagraphStyle(
            "KMeta", parent=styles["Normal"], fontName=base, fontSize=10, leading=14,
        ),
        "step_title": ParagraphStyle(
            "KStepTitle", parent=styles["Heading2"], fontName=base, fontSize=13, leading=17,
            spaceBefore=14, spaceAfter=4, textColor=colors.HexColor("#1a1a1a"),
        ),
        "body": ParagraphStyle(
            "KBody", parent=styles["Normal"], fontName=base, fontSize=10, leading=15,
        ),
        "caution": ParagraphStyle(
            "KCaution", parent=styles["Normal"], fontName=base, fontSize=10, leading=14,
            textColor=colors.HexColor("#b00020"),
        ),
        "decision": ParagraphStyle(
            "KDecision", parent=styles["Normal"], fontName=base, fontSize=10, leading=14,
            textColor=colors.HexColor("#0b6b2c"),
        ),
        "note": ParagraphStyle(
            "KNote", parent=styles["Normal"], fontName=base, fontSize=10, leading=14,
            textColor=colors.HexColor("#333333"), backColor=colors.HexColor("#f5f5f5"),
        ),
        "caption": ParagraphStyle(
            "KCaption", parent=styles["Normal"], fontName=base, fontSize=8, leading=11,
            textColor=colors.HexColor("#666666"),
        ),
    }


def _esc(text):
    """reportlab Paragraph는 간단한 HTML 서브셋을 쓰므로 특수문자를 이스케이프한다."""
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_pdf_bytes():
    device_type = st.session_state.device_type
    role = st.session_state.role
    steps = get_full_steps(device_type)
    records = st.session_state.records
    # 수사관용 PDF에는 1~4단계만 포함한다. 포렌식분석관이 현장 즉시 이미징을
    # 선택한 경우에는 증거물 포장·봉인 단계를 제외한다.
    report_last_index = get_effective_last_index(steps, records, role)
    report_indices = [i for i in get_visible_step_indices(steps, records, role) if i <= report_last_index]
    report_steps = [(i, steps[i]) for i in report_indices]

    font_name = ensure_korean_font_registered()
    styles = _pdf_styles(font_name)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=18 * mm, bottomMargin=18 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
    )

    story = []

    if not font_name:
        story.append(Paragraph(
            "WARNING: Korean font not found on this system. Text below may not render "
            "correctly. Place a .ttf font (e.g. NanumGothic.ttf) under a 'fonts' folder "
            "next to app.py, or deploy on Windows where Malgun Gothic is built in.",
            styles["caution"],
        ))
        story.append(Spacer(1, 8))

    story.append(Paragraph("디지털 포렌식 현장 압수 절차 리포트", styles["title"]))
    story.append(Paragraph("(Chain of Custody Log)", styles["meta"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        _esc("주의: 본 문서는 현장 기록 보조 자료이며 법률 자문이나 기관 SOP를 대체하지 않습니다. 영장 범위, 관련성 선별, 참여권 및 압수목록 교부 등 절차 준수 여부는 사건별로 확인해야 합니다. 전자정보·복제본의 압수/보관/교부 여부는 일률적으로 단정하지 말고 법적 근거와 책임자 판단을 기록하십시오."),
        styles["note"]
    ))
    story.append(Spacer(1, 10))

    meta_rows = [
        ["생성 시각", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ["기기 유형", device_type],
        ["현장 수행 주체", role or "-"],
    ]
    for k, v in st.session_state.case_info.items():
        meta_rows.append([k, v or "-"])

    meta_table = Table(meta_rows, colWidths=[40 * mm, 120 * mm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), font_name or "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eeeeee")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#999999")))

    selected_decision = get_selected_decision(steps, records)
    default_rec = {"done": False, "note": "", "photos": [], "decision": None, "tool": None}

    for display_index, (record_index, step) in enumerate(report_steps):
        rec = records.get(record_index, default_rec)
        status = "[완료]" if rec["done"] else "[미완료]"
        story.append(Paragraph(f"{status} {display_index + 1}. {_esc(step['title'])}", styles["step_title"]))

        if step.get("type") == "device_select":
            story.append(Paragraph(_esc(step["detail"]).replace("\n", "<br/>"), styles["body"]))
            story.append(Spacer(1, 3))
            story.append(Paragraph(f"▶ 선택된 기기 유형: {_esc(device_type or '-')}", styles["decision"]))
            story.append(Spacer(1, 4))
            story.append(HRFlowable(width="100%", color=colors.HexColor("#dddddd")))
            continue

        detail_text, caution_text = get_role_text(step, role)
        story.append(Paragraph(_esc(detail_text).replace("\n", "<br/>"), styles["body"]))

        if step.get("tool_select") and rec.get("tool"):
            story.append(Spacer(1, 3))
            story.append(Paragraph(f"🔧 사용 장비: {_esc(rec['tool'])}", styles["decision"]))

        if step.get("variants") and selected_decision:
            variant_text = step["variants"].get(selected_decision)
            if variant_text:
                story.append(Spacer(1, 3))
                story.append(Paragraph(_esc(variant_text).replace("\n", "<br/>"), styles["decision"]))

        if caution_text:
            story.append(Spacer(1, 3))
            story.append(Paragraph(f"⚠ 주의: {_esc(caution_text)}", styles["caution"]))

        if step.get("type") == "decision" and rec.get("decision"):
            story.append(Spacer(1, 3))
            story.append(Paragraph(f"▶ 선택된 결정: {_esc(rec['decision'])}", styles["decision"]))
            branch_text = step.get("branch_info", {}).get(rec["decision"])
            if branch_text:
                story.append(Paragraph(_esc(branch_text).replace("\n", "<br/>"), styles["decision"]))

        if rec["note"]:
            story.append(Spacer(1, 4))
            story.append(Paragraph(f"현장 메모: {_esc(rec['note'])}", styles["note"]))

        photos = rec.get("photos") or []
        if photos:
            story.append(Spacer(1, 6))
            max_width = 150 * mm
            for photo in photos:
                try:
                    photo.seek(0)
                    raw = photo.read()
                    pil_img = PILImage.open(io.BytesIO(raw))
                    pil_img.load()
                    w, h = pil_img.size
                    scale = min(max_width / w, 1.0)
                    draw_w, draw_h = w * scale, h * scale
                    # 세로 너무 길면 최대 높이로 제한
                    max_height = 120 * mm
                    if draw_h > max_height:
                        ratio = max_height / draw_h
                        draw_w, draw_h = draw_w * ratio, draw_h * ratio
                    img_buffer = io.BytesIO()
                    pil_img.convert("RGB").save(img_buffer, format="JPEG", quality=85)
                    img_buffer.seek(0)
                    story.append(RLImage(img_buffer, width=draw_w, height=draw_h))
                    story.append(Paragraph(_esc(photo.name), styles["caption"]))
                    story.append(Spacer(1, 4))
                except Exception:
                    story.append(Paragraph(
                        f"(사진 첨부 실패 - 파일 형식 미지원: {_esc(photo.name)})",
                        styles["caption"],
                    ))

        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", color=colors.HexColor("#dddddd")))

    story.append(Spacer(1, 16))
    story.append(Paragraph("서명란", styles["step_title"]))
    story.append(Spacer(1, 10))
    sign_table = Table(
        [["담당 수사관 서명:", "", "일시:", ""],
         ["입회인 서명:", "", "일시:", ""]],
        colWidths=[30 * mm, 50 * mm, 15 * mm, 45 * mm],
    )
    sign_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), font_name or "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("LINEBELOW", (1, 0), (1, -1), 0.7, colors.black),
        ("LINEBELOW", (3, 0), (3, -1), 0.7, colors.black),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(sign_table)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def get_record(idx):
    """전역 단계 인덱스에 대한 기록을 반환한다. 없으면 기본값으로 만든다.
    (1단계에서 기기 유형을 고르기 전에는 기기별 단계가 아직 존재하지 않으므로
    필요한 시점에 그때그때 생성한다.)"""
    if idx not in st.session_state.records:
        st.session_state.records[idx] = {
            "done": False, "note": "", "photos": [], "decision": None, "tool": None,
        }
    return st.session_state.records[idx]


def render_guide():
    role = st.session_state.role
    device_type = st.session_state.device_type
    steps = get_full_steps(device_type)
    idx = st.session_state.current_index
    idx = min(idx, len(steps) - 1)  # 기기 유형이 아직 없을 때 범위를 벗어나지 않도록
    visible_indices = get_visible_step_indices(steps, st.session_state.records, role)
    if idx not in visible_indices:
        later = [i for i in visible_indices if i > idx]
        idx = later[0] if later else visible_indices[-1]
    st.session_state.current_index = idx
    visible_position = visible_indices.index(idx)
    step = steps[idx]
    rec = get_record(idx)

    header = f"[{device_type} · {role}]" if device_type else f"[{role}]"
    top_l, top_r = st.columns([4, 1])
    with top_l:
        st.title("현장 압수 절차")
        st.caption(header)
    with top_r:
        if st.button("처음으로"):
            st.session_state.stage = "start"
            st.rerun()

    st.progress((visible_position + 1) / len(visible_indices), text=f"{visible_position + 1} / {len(visible_indices)} 단계")

    st.subheader(f"{visible_position + 1}. {step['title']}")

    if step.get("type") == "device_select":
        st.markdown(step["detail"].replace("\n", "  \n"))
        if step.get("caution"):
            st.warning(f"⚠ 주의: {step['caution']}")
        options = ["PC", "iPhone", "Android"]
        current = device_type
        default_index = options.index(current) if current in options else None
        choice = st.radio("기기 유형", options, index=default_index, horizontal=True, key="device_select_radio")
        if choice != st.session_state.device_type:
            st.session_state.device_type = choice
            # 기기 유형 변경 시 안전·권한 확인과 유형 선택 기록만 유지한다.
            # 사진 기록 및 기기별 단계 기록은 새 기기에 맞게 초기화한다.
            keep = {0, 1}
            st.session_state.records = {k: v for k, v in st.session_state.records.items() if k in keep}
            st.rerun()
        device_type = st.session_state.device_type
    else:
        detail_text, caution_text = get_role_text(step, role)
        st.markdown(detail_text.replace("\n", "  \n"))
        if caution_text:
            st.warning(f"⚠ 주의: {caution_text}")

        if step.get("tool_select") and role == "포렌식분석관":
            tool_options = TOOLS_BY_DEVICE.get(device_type, [])
            current_tool = rec.get("tool")
            tool_index = tool_options.index(current_tool) if current_tool in tool_options else None
            chosen_tool = st.selectbox(
                "사용 장비 선택 (보유 포렌식 도구)",
                tool_options,
                index=tool_index,
                key=f"tool_{idx}",
                placeholder="도구를 선택하세요",
            )
            rec["tool"] = chosen_tool

        if step.get("variants"):
            selected_decision = get_selected_decision(steps, st.session_state.records)
            if selected_decision:
                variant_text = step["variants"].get(selected_decision)
                if variant_text:
                    st.info(variant_text.replace("\n", "  \n"))
            else:
                st.caption("ℹ️ 앞선 '현장 이미지 추출 여부 결정' 단계에서 선택하면 이 단계 안내가 그에 맞게 표시됩니다.")

        if step.get("type") == "decision":
            options = step["options"]
            current = rec.get("decision")
            default_index = options.index(current) if current in options else None
            choice = st.radio(
                "현장 결정",
                options,
                index=default_index,
                key=f"decision_{idx}",
            )
            rec["decision"] = choice
            if choice:
                branch_text = step.get("branch_info", {}).get(choice)
                if branch_text:
                    st.success(branch_text.replace("\n", "  \n"))
                if role == "수사관" and choice == "현장 즉시 이미지 추출":
                    st.warning(
                        "🧑‍💼 현장 즉시 이미지 추출이 선택되었습니다. 수사관의 역할은 "
                        "여기서 끝나며, 이후 추출 작업은 포렌식 담당자가 전담합니다. "
                        "수사관은 아래에서 지금까지의 리포트를 다운로드할 수 있습니다."
                    )

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
                    st.image(photo, caption=photo.name, width="stretch")
        else:
            st.caption("아직 첨부된 사진이 없습니다.")

    # 모든 단계 내용(특히 결정 라디오 처리)이 끝난 뒤에 계산해야 이번 렌더링에서
    # 방금 선택한 결정값이 바로 반영된다.
    visible_indices = get_visible_step_indices(steps, st.session_state.records, role)
    visible_position = visible_indices.index(idx)
    effective_last = get_effective_last_index(steps, st.session_state.records, role)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("◀ 이전 단계", disabled=(visible_position == 0)):
            st.session_state.current_index = visible_indices[visible_position - 1]
            st.rerun()
    with col2:
        can_advance = visible_position < len(visible_indices) - 1 and idx < effective_last
        device_missing = step.get("type") == "device_select" and not device_type
        if can_advance:
            if st.button("다음 단계 ▶", disabled=device_missing):
                st.session_state.current_index = visible_indices[visible_position + 1]
                st.rerun()
            if device_missing:
                st.caption("기기 유형을 선택하면 다음 단계로 진행할 수 있습니다.")
        elif role == "수사관" and idx == effective_last and idx < len(steps) - 1:
            st.success("수사관 절차는 4단계까지입니다. 이후 기술적 절차는 포렌식분석관이 이어서 수행합니다. 아래에서 리포트를 다운로드하세요.")
        else:
            st.success("마지막 단계입니다. 아래에서 리포트를 다운로드하세요.")
    with col3:
        pass

    if device_type:
        st.divider()
        st.markdown("### 📄 리포트 다운로드")
        file_tag = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # 다운로드 가능한 사진도 PDF와 같은 단계 범위로 제한한다.
        export_last_index = get_effective_last_index(steps, st.session_state.records, role)
        export_indices = [i for i in get_visible_step_indices(steps, st.session_state.records, role) if i <= export_last_index]
        export_steps = [(i, steps[i]) for i in export_indices]
        total_photos = sum(
            len(st.session_state.records.get(i, {}).get("photos") or [])
            for i, _step in export_steps
        )

        if not get_korean_font_path():
            st.warning(
                "한글 폰트를 찾지 못했습니다. Windows에서는 보통 자동으로 잡히지만, "
                "다른 OS에서는 app.py와 같은 폴더에 fonts/NanumGothic.ttf 를 넣어주세요. "
                "폰트가 없어도 PDF는 생성되지만 한글이 깨져 보일 수 있습니다."
            )

        dcol1, dcol2 = st.columns(2)
        with dcol1:
            pdf_bytes = build_pdf_bytes()
            st.download_button(
                "PDF 리포트 다운로드",
                data=pdf_bytes,
                file_name=f"forensic_report_{device_type}_{file_tag}.pdf",
                mime="application/pdf",
            )
        with dcol2:
            if total_photos > 0:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                    for display_index, (record_index, export_step) in enumerate(export_steps):
                        photos = st.session_state.records.get(record_index, {}).get("photos") or []
                        step_folder = f"{display_index + 1:02d}_{export_step['title'][:20]}".replace("/", "-")
                        for photo in photos:
                            photo.seek(0)
                            zf.writestr(f"{step_folder}/{photo.name}", photo.read())
                st.download_button(
                    f"{'1~4단계' if role == '수사관' else '전체 단계'} 사진 ZIP ({total_photos}장)",
                    data=zip_buffer.getvalue(),
                    file_name=f"forensic_photos_{device_type}_{file_tag}.zip",
                    mime="application/zip",
                )
            else:
                st.caption("첨부된 사진이 없습니다.")

        with st.expander("전체 단계 한눈에 보기 / 바로 이동"):
            for display_index, i in enumerate(get_visible_step_indices(steps, st.session_state.records, role)):
                s = steps[i]
                mark = "✅" if st.session_state.records.get(i, {}).get("done") else "⬜"
                locked = i > effective_last
                label = f"{mark} {display_index + 1}. {s['title']}" + (" 🔒" if locked else "")
                if st.button(label, key=f"jump_{i}", disabled=locked):
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