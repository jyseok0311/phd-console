# -*- coding: utf-8 -*-
"""박사학위 콘솔 점검·개선 (2026-09-29) — 접근성·성능·내비게이션.

  1) 이름 없던 입력창에 aria-label — 문헌(항목마다 메모·읽기 상태·인용 장절·숨기기, 필터 6개), 목차(진행 상태·쪽수·메모),
     마일스톤 체크, 데이터(지표·연도·학교 검색). 문헌·목차는 항목 이름을 넣어 낭독기가 어느 항목인지 알 수 있게 한다.
  2) 문헌 목록에 content-visibility:auto — 화면 밖 항목은 그리기를 미룬다(노드 1.5만 개, 렌더 0.43초).
  3) 화면을 바꾸면 브라우저 탭 제목도 「화면 이름 · 박사학위 콘솔」로.
  4) 「본문으로 건너뛰기」 링크(키보드 사용자). 해시 라우터와 충돌하지 않게 # 링크가 아니라 클릭 처리.

  python docs/_점검개선_패치.py      (phd-console 폴더에서, 한 번만)
"""
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
s = open(P, encoding='utf-8').read()
assert 'skiplink' not in s, '이미 적용됨'


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (old[:70], c)
    s = s.replace(old, new)


T = '\' + esc(r.title || "") + \''          # 문헌 제목을 aria-label 에 넣는 조각

# 1) aria-label ---------------------------------------------------------
rep('<textarea data-rmemo="\' + r.id + \'" maxlength="1500"',
    '<textarea data-rmemo="\' + r.id + \'" aria-label="메모 — %s" maxlength="1500"' % T)
rep('<select data-rst="\' + r.id + \'">', '<select data-rst="\' + r.id + \'" aria-label="읽기 상태 — %s">' % T)
rep('<select data-rcite="\' + r.id + \'">', '<select data-rcite="\' + r.id + \'" aria-label="인용 장절 — %s">' % T)
rep('<button class="del" data-rdel="\' + r.id + \'">', '<button class="del" data-rdel="\' + r.id + \'" aria-label="목록에서 숨기기 — %s">' % T)
rep('id="refQ" placeholder=', 'id="refQ" aria-label="문헌 검색" placeholder=')
for k, lab in (('area', '영역'), ('grp', '묶음'), ('tag', '주제'), ('st', '읽기 상태'), ('sort', '정렬')):
    rep('<select data-rsel="%s">' % k, '<select data-rsel="%s" aria-label="%s 필터">' % (k, lab))
rep('<select data-toc-st="\' + x.id + \'" class="st-\' + st + \'">',
    '<select data-toc-st="\' + x.id + \'" aria-label="진행 상태 — \' + x.id + \' \' + esc(x.t) + \'" class="st-\' + st + \'">')
rep('data-toc-pg="\' + x.id + \'" value=', 'data-toc-pg="\' + x.id + \'" aria-label="현재 쪽수 — \' + x.id + \' \' + esc(x.t) + \'" value=')
rep('data-toc-note="\' + x.id + \'" maxlength=', 'data-toc-note="\' + x.id + \'" aria-label="메모 — \' + x.id + \' \' + esc(x.t) + \'" maxlength=')
rep('<input class="ck mchk" type="checkbox" data-mk="\' + M.k + \'"',
    '<input class="ck mchk" type="checkbox" data-mk="\' + M.k + \'" aria-label="\' + esc(M.label || M.k) + \' 완료"')
rep('<select data-dsel="ind">', '<select data-dsel="ind" aria-label="지표">')
rep('<select data-dsel="year">', '<select data-dsel="year" aria-label="연도">')
rep('id="schoolIn" placeholder=', 'id="schoolIn" aria-label="학교명 검색" placeholder=')

# 2) 문헌 목록 그리기 미루기 ------------------------------------------------
rep('@media (max-width:640px){ .ref{grid-template-columns:1fr} }',
    '.ref{content-visibility:auto; contain-intrinsic-size:auto 150px}   /* 화면 밖 항목은 그리기를 미룬다 */\n'
    '@media (max-width:640px){ .ref{grid-template-columns:1fr} }')

# 3) 탭 제목 --------------------------------------------------------------
rep('document.getElementById("scTitle").textContent = SCREENS[name].title;',
    'document.getElementById("scTitle").textContent = SCREENS[name].title;\n'
    '  document.title = SCREENS[name].title + " · 박사학위 콘솔";')

# 4) 본문으로 건너뛰기 -----------------------------------------------------
rep('<body>\n\n<div class="app">', '<body>\n<a class="skiplink" href="#/" id="skipLink">본문으로 건너뛰기</a>\n\n<div class="app">')
rep('<main id="screen"></main>', '<main id="screen" tabindex="-1"></main>')
rep('.srlive{position:absolute;',
    '.skiplink{position:absolute; left:8px; top:-48px; z-index:50; background:var(--accent); color:var(--on-accent); padding:9px 14px;\n'
    '  border-radius:var(--r-s); font-size:13px; font-weight:600; text-decoration:none}\n'
    '.skiplink:focus{top:8px}\n'
    'main:focus{outline:none}\n'
    '.srlive{position:absolute;')
rep('/* ===================== 부팅 ===================== */\nload();',
    'document.getElementById("skipLink").addEventListener("click", function(e){ e.preventDefault(); document.getElementById("screen").focus(); });\n\n'
    '/* ===================== 부팅 ===================== */\nload();')

open(P, 'w', encoding='utf-8').write(s)
print('적용 완료')
