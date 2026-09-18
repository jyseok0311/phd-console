# -*- coding: utf-8 -*-
"""phd-console 에 「진행 현황」 메뉴를 붙인다.

지도교수 확인용 진행보고서(v1.6)를 내려받을 수 있게 하고, 목차·확인 요청·판본
이력을 한 화면에 보여 준다. 보고서 파일은 docs/ 에 ASCII 이름으로 두고,
내려받을 때의 이름만 download 속성으로 한글로 돌려준다.
"""
import io, re, sys, os

P = r'C:\Users\User\Desktop\phd-console\index.html'
h = io.open(P, encoding='utf-8').read()
orig = h
log = []


def once(old, new, what):
    global h
    if new.split('\n')[0][:40] in h and what.startswith('중복'):
        return
    n = h.count(old)
    if n != 1:
        sys.exit('앵커 %d개 (1개여야 함): %s' % (n, what))
    h = h.replace(old, new, 1)
    log.append(what)


# 1) a.abtn 스타일 (내려받기 링크용)
once('.actions{display:flex; gap:8px; flex-wrap:wrap; align-items:center}',
     'a.abtn{display:inline-flex; align-items:center; gap:7px; text-decoration:none; color:inherit}\n'
     'a.abtn.primary{color:var(--on-accent)}\n'
     '.dlrow{display:flex; gap:14px; align-items:center; flex-wrap:wrap}\n'
     '.dlrow .fname{font-family:var(--f-mono); font-size:11.5px; color:var(--ink-3)}\n'
     '.actions{display:flex; gap:8px; flex-wrap:wrap; align-items:center}',
     'CSS: 내려받기 링크·줄 스타일')

# 2) 좌측 메뉴 버튼
once('<span>문헌</span><span class="cnt" id="cntRefs"></span></button>',
     '<span>문헌</span><span class="cnt" id="cntRefs"></span></button>\n'
     '    <button class="navb" data-go="report"><svg viewBox="0 0 24 24">'
     '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/>'
     '<path d="M14 3v5h5"/><path d="M12 12v5"/><path d="m9.5 14.5 2.5-2.5 2.5 2.5"/></svg>'
     '<span>진행 현황</span><span class="cnt" id="cntRep"></span></button>',
     '메뉴: 진행 현황 버튼')

# 3) 라우트 등록
once('  refs: {title:"문헌", render:scRefs}',
     '  refs: {title:"문헌", render:scRefs},\n'
     '  report:{title:"진행 현황", render:scReport}',
     '라우트: report')

# 4) 메뉴 뱃지
once('  var cr = document.getElementById("cntRefs"); if(cr) cr.textContent = allRefs().length ? allRefs().length + "편" : "";',
     '  var cr = document.getElementById("cntRefs"); if(cr) cr.textContent = allRefs().length ? allRefs().length + "편" : "";\n'
     '  var cp = document.getElementById("cntRep"); if(cp) cp.textContent = REPORT.ver;',
     '뱃지: 판본 표시')

# 5) 데이터와 화면
SCREEN = r'''
/* ===================== 진행 현황 ===================== */
/* 지도교수 확인용 진행보고서의 메타데이터. 보고서를 새로 내면 이 상수만 고친다. */
var REPORT = {
  ver: "v1.6",
  date: "2026. 9. 18.",
  file: "docs/progress-report-v1.6.hwpx",
  name: "박사학위논문_진행보고_석재영_v1.6.hwpx",
  size: "80KB",
  adviser: "박경돈 교수님",
  pages: 16,
  toc: [
    ["Ⅰ. 보고 목적",      [[1,"보고 목적과 현재 단계",1]]],
    ["Ⅱ. 분석자료",       [[2,"분석자료 구축 현황",1]]],
    ["Ⅲ. 근거 이론",      [[3,"근거 이론 (7개)",2],[4,"이론별 대표 문헌",3],[5,"검토 후 채택하지 않은 이론",3]]],
    ["Ⅳ. 분석모형과 변수", [[6,"분석모형 확정안",4],[7,"투입변수 (8개)",4],[8,"산출변수 (10개)",5],
                            [9,"환경변수: 2단계 결정요인 (55개)",5],[10,"변수 확대의 검증 결과",7]]],
    ["Ⅴ. 문헌연구",       [[11,"문헌연구 현황",8],[12,"구분별 집계",8]]],
    ["Ⅵ. 확인과 일정",    [[13,"확인 요청 사항",9],[14,"향후 일정",10]]],
    ["부록",              [[15,"국내문헌 (90편)",11],[16,"국외문헌 (147편)",16]]]
  ],
  asks: [
    ["분석기간", 1, "2025년은 취업률 미공시로 완전 관측치 0건. 2015~2024년 10개년으로 줄일지, 2025년을 취업자 수 제외 모형으로 따로 낼지."],
    ["변수 개수", 1, "최대(투입 8 × 산출 10)로 돌리면 효율성 1인 대학이 73~78%. 기본 3 × 4 를 주 분석으로, 최대안은 민감도 근거표로."],
    ["산출변수의 0값", 0, "기술이전 597건·특허 478건·SCI 189건이 0. 결측만 빼면 1,731개, 양수만 쓰면 1,114개."],
    ["재정 변수의 표본", 1, "재정알리미 6개 변수는 사립대만 공시. 2단계에 넣으면 국공립 287개가 전량 빠진다."],
    ["환경변수 축약", 0, "55개를 다 넣을 수 없다. 구분별 대표 변수로 8~12개까지 추리고 나머지는 강건성 검정."],
    ["정부재정지원금", 0, "총교육비와 중복 계상되어 투입에서 빼고 2단계 결정요인으로. 자원의존이론이 근거."],
    ["분교 처리", 0, "건국 글로컬·고려 세종·동국 WISE·연세 미래·한양 ERICA 5개는 별도 DMU."]
  ],
  hist: [
    ["v1.6","2026. 9. 18.","이론명 띄어쓰기 4곳"],
    ["v1.5","2026. 9. 18.","표지·목차를 학위논문 격식으로, 쪽번호 기입"],
    ["v1.3","2026. 9. 18.","각주 복원 · 「쓸 자리」 열 복원"],
    ["v1.1","2026. 9. 17.","자료·이론·변수·문헌 통합본 (16절)"],
    ["v1.0","2026. 9. 16.","최초 보고 — 확인 요청 5건"]
  ]
};

function scReport(){
  var R = REPORT, urgent = R.asks.filter(function(a){ return a[1]; }).length;
  var h = "";

  h += '<section class="stats">' +
    tile("판본", R.ver, R.date + " · 지도교수 확인용", "accv") +
    tile("분량", "16절", "본문 14 · 부록 2 · 표 16개", "") +
    tile("쪽", R.pages + "", "표지 · 목차 별도", "") +
    tile("확인 요청", R.asks.length + "건", "그중 " + urgent + "건은 DEA 실행 전 결정", "accv") +
    tile("받는 분", R.adviser.replace(" 교수님",""), "교수님", "") +
    '</section>';

  h += '<section class="panel lift"><div class="panel-hd"><h2>보고서 내려받기</h2>' +
    '<p class="hint">한글(HWPX) — 한컴오피스 한글에서 열립니다</p></div><div class="panel-bd">' +
    '<div class="dlrow"><a class="abtn primary" href="' + R.file + '" download="' + R.name + '">' +
    '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" ' +
    'stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="m7 11 5 5 5-5"/>' +
    '<path d="M4 20h16"/></svg>' + R.ver + ' 내려받기</a>' +
    '<span class="fname">' + esc(R.name) + ' · ' + R.size + '</span></div></div></section>';

  h += '<div class="dgrid">';

  /* 목차 */
  h += '<section class="panel"><div class="panel-hd"><h2>목차</h2><p class="hint">절 ' +
    '16개 · 쪽번호는 보고서 기준</p></div><div class="panel-bd">' +
    '<div class="tablewrap"><table class="dt"><thead><tr><th>구분</th><th>절</th><th class="n">쪽</th></tr></thead><tbody>';
  R.toc.forEach(function(g){
    g[1].forEach(function(s, i){
      h += '<tr><td class="k">' + (i === 0 ? esc(g[0]) : "") + '</td>' +
        '<td>' + s[0] + '. ' + esc(s[1]) + '</td><td class="n">' + s[2] + '</td></tr>';
    });
  });
  h += '</tbody></table></div></div></section>';

  /* 판본 이력 */
  h += '<section class="panel"><div class="panel-hd"><h2>판본 이력</h2>' +
    '<p class="hint">내려받기는 최신판만 제공합니다</p></div><div class="panel-bd">' +
    '<div class="tablewrap"><table class="dt"><thead><tr><th>판본</th><th>날짜</th><th>바뀐 점</th></tr></thead><tbody>';
  R.hist.forEach(function(v, i){
    h += '<tr><td class="k">' + esc(v[0]) + (i === 0 ? ' ' + pill("확보") : "") + '</td>' +
      '<td class="dim">' + esc(v[1]) + '</td><td class="dim">' + esc(v[2]) + '</td></tr>';
  });
  h += '</tbody></table></div></div></section>';
  h += '</div>';

  /* 확인 요청 */
  h += '<section class="panel lift"><div class="panel-hd"><h2>확인 요청 사항</h2>' +
    '<p class="hint">' + R.asks.length + '건 · 표시된 ' + urgent + '건은 DEA 실행 전에 결정이 필요합니다</p></div>' +
    '<div class="panel-bd"><div class="tablewrap"><table class="dt"><thead>' +
    '<tr><th class="n">#</th><th>사안</th><th>요지</th><th>시급</th></tr></thead><tbody>';
  R.asks.forEach(function(a, i){
    h += '<tr><td class="n">' + (i + 1) + '</td><td class="k">' + esc(a[0]) + '</td>' +
      '<td class="dim">' + esc(a[2]) + '</td><td>' +
      (a[1] ? '<span class="pill part">실행 전</span>' : '<span class="dim">확인만</span>') + '</td></tr>';
  });
  h += '</tbody></table></div></div></section>';
  return h;
}
'''

once('/* ===================== 부팅 ===================== */',
     SCREEN.strip() + '\n\n/* ===================== 부팅 ===================== */',
     '화면: scReport + REPORT 상수')

io.open(P, 'w', encoding='utf-8').write(h)
print('index.html %d → %d 자' % (len(orig), len(h)))
for x in log:
    print('  ·', x)
