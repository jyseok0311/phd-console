# -*- coding: utf-8 -*-
"""박사학위 콘솔에 「피드백」 메뉴 추가 (2026-09-23).

지도교수 피드백의 반영 여부를 한 화면에 모은다. 원본 표는
박사학위논문/지도교수 면담/피드백_반영표.xlsx 이며 docs/feedback-tracker.xlsx 로 내려받게 한다.

  python docs/_피드백메뉴_패치.py      (phd-console 폴더에서, 한 번만)
"""
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
s = open(P, encoding='utf-8').read()
assert 'scFeedback' not in s, '이미 적용됨'

# ── 메뉴 버튼 ─────────────────────────────────────────────────────────
NAV = '<span>진행 현황</span><span class="cnt" id="cntRep"></span></button>'
assert NAV in s
s = s.replace(NAV, NAV + '\n    <button class="navb" data-go="feedback"><svg viewBox="0 0 24 24">'
              '<path d="M21 15a2 2 0 0 1-2 2H8l-4 4V5a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2z"/>'
              '<path d="m8.5 10 2.2 2.2L15.5 7.5"/></svg><span>피드백</span>'
              '<span class="cnt" id="cntFb"></span></button>', 1)

# ── 라우팅 · 배지 ─────────────────────────────────────────────────────
R = '  report:{title:"진행 현황", render:scReport}\n'
assert R in s
s = s.replace(R, '  report:{title:"진행 현황", render:scReport},\n'
                 '  feedback:{title:"피드백 반영", render:scFeedback}\n', 1)
M = '  var cp = document.getElementById("cntRep"); if(cp) cp.textContent = REPORT.ver;\n'
assert M in s
s = s.replace(M, M + '  var cf = document.getElementById("cntFb"); if(cf) cf.textContent = '
                     'FEEDBACK.items.filter(function(x){ return x[6] === "완료"; }).length + "/" + FEEDBACK.items.length;\n', 1)

# ── CSS ───────────────────────────────────────────────────────────────
C = '.dlrow .fname{font-family:var(--f-mono); font-size:11.5px; color:var(--ink-3)}\n'
assert C in s
s = s.replace(C, C +
    'ul.fbl{margin:0; padding-left:15px}\n'
    'ul.fbl li{margin:2px 0; line-height:1.5}\n'
    'table.fbt td{vertical-align:top}\n'
    'table.fbt td.k{white-space:normal; min-width:120px}\n'
    '.fbd{display:block; font-weight:400; font-size:11px; color:var(--ink-3); font-family:var(--f-mono); margin-top:2px}\n'
    'table.dt td.mono{font-family:var(--f-mono)}\n', 1)

# ── 데이터 · 화면 ─────────────────────────────────────────────────────
JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_피드백메뉴.js'), encoding='utf-8').read()
B = '/* ===================== 부팅 ===================== */'
assert B in s
s = s.replace(B, JS + '\n' + B, 1)

open(P, 'w', encoding='utf-8').write(s)
print('적용 완료')
