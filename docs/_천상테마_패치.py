# -*- coding: utf-8 -*-
"""박사학위 콘솔 「천상」 테마 (2026-09-29) — /taste 스킬의 방향을 화면용으로 옮김.

스킬의 원칙을 UI 에 옮긴 것
  · 방향을 먼저 정한다  → 천사코어 × 클라우드 트랜스 중 「천상」: near-black 허공 + bone white 글자
  · 강조색은 하나        → 딱 하나의 따뜻한 빛(금 #FFB24D). 붉은색은 경고에만
  · 한 줄기 빛           → 화면 오른쪽 위에서 번지는 은은한 불씨 그러데이션, 눌린 메뉴와 떠 있는 패널에 금빛 번짐
  · 결이 하나            → 지도·표의 색 단계도 금 한 가지 색의 명암(ember → gold)
기존 밝은·어두운 테마는 건드리지 않고 세 번째 테마로 더한다. 상단 버튼이 밝게 → 어둡게 → 천상 순으로 돈다.
대비: 본문 17.1:1, 보조 글자 9.7:1 · 6.3:1, 금 글자 10.8:1, 금 바탕 위 글자 10.5:1, 경고 7.6:1 (모두 WCAG AA 이상).

  python docs/_천상테마_패치.py      (phd-console 폴더에서, 한 번만)
"""
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
s = open(P, encoding='utf-8').read()
assert 'data-theme="angel"' not in s, '이미 적용됨'


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (old[:70], c)
    s = s.replace(old, new)


# 1) 저장된 테마 읽기 ------------------------------------------------------
rep('document.documentElement.setAttribute("data-theme", t === "dark" ? "dark" : "light"); })();',
    'document.documentElement.setAttribute("data-theme", t === "dark" || t === "angel" ? t : "light"); })();')

# 2) 토큰과 결 ------------------------------------------------------------
rep('\n*{box-sizing:border-box}',
    '''
/* 천상 테마 — near-black 허공 · bone white · 하나의 따뜻한 빛(금). 붉은색은 경고에만 (docs/_천상테마_패치.py) */
:root[data-theme="angel"]{
  color-scheme:dark;
  --ground:#05060A; --surface:#0C0E16; --surface-2:#131624; --surface-3:#1C2032;
  --line:#242942; --line-soft:#161A2A; --line-strong:#3D4468;
  --ink:#F4F1EA; --ink-2:#B9B5C9; --ink-3:#9490AB;
  --accent:#FFB24D; --accent-ink:#FFCB80; --accent-soft:#2B1E0C; --accent-line:#8A5A1E; --on-accent:#1A0F00;
  --warn:#FF7A7A; --warn-soft:#2C1115; --warn-line:#7A2B33;
  --grid:#161A2A;
  --shadow:0 1px 2px rgba(0,0,0,.6), 0 14px 34px -22px rgba(0,0,0,1);
  --shadow-lift:0 0 0 1px rgba(255,178,77,.07), 0 24px 56px -28px rgba(255,150,40,.32);
}
:root[data-theme="angel"] body{background:radial-gradient(880px 460px at 82% -10%, rgba(255,150,40,.13), transparent 62%) no-repeat, var(--ground)}   /* fixed 는 스크롤마다 다시 그려 무겁다 — 맨 위에서만 번지게 */
:root[data-theme="angel"] .navb[aria-current="page"]{box-shadow:inset 0 0 0 1px var(--accent-line), 0 0 22px -8px rgba(255,178,77,.55)}
:root[data-theme="angel"] .corr td[data-q="4"], :root[data-theme="angel"] .corr td[data-q="5"]{color:#1A0F00}
:root[data-theme="angel"] .mapfig img{border-color:var(--accent-line); box-shadow:0 0 30px -12px rgba(255,178,77,.5)}

*{box-sizing:border-box}''')

# 3) 상단 버튼: 밝게 → 어둡게 → 천상 ------------------------------------------
old = s[s.index('function themeLabel(){'):s.index('themeLabel();\n\n/* ===================== 진행 현황')]
new = '''var THEMES = ["light", "dark", "angel"], THEME_NEXT = {light:"어둡게", dark:"천상", angel:"밝게"}, THEME_NOW = {light:"밝음", dark:"어둠", angel:"천상"};
function themeCur(){ var t = document.documentElement.getAttribute("data-theme"); return THEMES.indexOf(t) < 0 ? "light" : t; }
function themeLabel(){
  var cur = themeCur(), b = document.getElementById("themeTxt"), btn = document.querySelector("[data-theme-toggle]");
  if(b) b.textContent = THEME_NEXT[cur];
  if(btn) btn.setAttribute("aria-label", "화면 테마 바꾸기 — 지금 " + THEME_NOW[cur] + ", 다음 " + THEME_NEXT[cur]);
}
document.querySelector("[data-theme-toggle]").addEventListener("click", function(){
  var next = THEMES[(THEMES.indexOf(themeCur()) + 1) % THEMES.length];
  document.documentElement.setAttribute("data-theme", next);
  try{ localStorage.setItem("phd-console-theme", next); }catch(e){}
  themeLabel();
});
'''
s = s.replace(old, new, 1)

# 색 단계(--seq)는 금 한 가지 색의 명암. 운영체제 다크 모드용 「:root:not([data-theme="light"])」 규칙이 파일 뒤쪽에 있어
# (우선순위가 같으면 뒤가 이긴다) 위 토큰 블록에 두면 청록으로 덮인다 — 반드시 그 규칙보다 뒤에 둔다.
anchor = ':root[data-theme="dark"]{ --seq1:#153A35; --seq2:#1E5A52; --seq3:#2F8074; --seq4:#4FA99A; --seq5:#8ED3C7; --nodata:#1C2523 }\n'
rep(anchor, anchor + ':root[data-theme="angel"]{ --seq1:#2A1D0C; --seq2:#5A3C14; --seq3:#8A5A1C; --seq4:#DD9A38; --seq5:#FFC46B; --nodata:#131624; }\n')

open(P, 'w', encoding='utf-8').write(s)
print('적용 완료')
