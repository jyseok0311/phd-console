# -*- coding: utf-8 -*-
"""박사학위 콘솔 「지도」 메뉴 — 공간 의존성 예비 검정(2026-09-29).

박사학위논문 저장소의 결과물을 읽어 콘솔에 넣는다. 다시 실행하면 자료 블록만 새로 고친다(메뉴·화면은 한 번만 넣음).
  원본  박사학위논문/최종 결과물/데이터/예비분석_공간의존성.xlsx   (spatial_prelim.py)
        박사학위논문/최종 결과물/지도/지도1_평균효율성.png · 지도2_LISA군집.png · 대학점.csv   (spatial_map_qgis.py)
  복사  docs/maps/

  python docs/_지도메뉴_패치.py      (phd-console 폴더에서)
"""
import os, re, json, shutil
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.join(HERE, '..', 'index.html')
THESIS = r'C:\Users\User\Desktop\박사학위논문\최종 결과물'
XL = os.path.join(THESIS, '데이터', '예비분석_공간의존성.xlsx')
MAPS = os.path.join(HERE, 'maps')
os.makedirs(MAPS, exist_ok=True)
FILES = [(os.path.join(THESIS, '지도', '지도1_평균효율성.png'), 'map-efficiency.png'),
         (os.path.join(THESIS, '지도', '지도2_LISA군집.png'), 'map-lisa.png'),
         (os.path.join(THESIS, '지도', '대학점.csv'), 'points.csv'),
         (XL, 'spatial-prelim.xlsx')]
for a, b in FILES:
    shutil.copyfile(a, os.path.join(MAPS, b))
kb = lambda f: '%dKB' % round(os.path.getsize(os.path.join(MAPS, f)) / 1024)

# ── 자료 ─────────────────────────────────────────────────────────────
S = pd.read_excel(XL, sheet_name='요약').set_index('항목')['값']
MS = pd.read_excel(XL, sheet_name='Moran_요약')
B = pd.read_excel(XL, sheet_name='거점거리_구간')
LI = pd.read_excel(XL, sheet_name='LISA_거점거리')
W = {'band30': '반경 30km', 'band50': '반경 50km', 'knn6': '최근접 6개'}
moran = [[W.get(r['가중행렬'], r['가중행렬']), r['변수'], round(r['평균I'], 3), round(r['최소I'], 3), round(r['최대I'], 3),
          int(r['유의연도']), int(r['연도수'])] for _, r in MS.iterrows()]
sig = LI[LI['군집'] != '유의하지 않음'].sort_values(['군집', 'CCR'])
DATA = {
    'updated': '2026. 9. 29.',
    'n': int(LI.shape[0]),
    'global': S["대학별 평균 CCR Moran's I (최근접 6개)"],
    'tests': [int(MS['유의연도'].sum()), int(MS['연도수'].sum())],
    'range': [round(float(MS['최소I'].min()), 2), round(float(MS['최대I'].max()), 2)],
    'lisa': S['LISA 군집(p < 0.05)'],
    'hub': S['거점국립대 거리–평균 CCR 순위상관(비거점)'],
    'hub2': S['같은 상관(비수도권 비거점)'],
    'pos': S['위치의 정밀도'],
    'moran': moran,
    'bins': [[str(r['거리 구간']), int(r['대학수']), round(r['평균CCR'], 3), round(r['평균BCC'], 3)] for _, r in B.iterrows()],
    'sig': [[r['학교명'], r['지역'], r['군집'], round(r['CCR'], 3), round(r['p'], 3)] for _, r in sig.iterrows()],
    'maps': [['지도 1 · 대학별 평균 효율성', 'docs/maps/map-efficiency.png', '박사학위논문_지도1_평균효율성.png', kb('map-efficiency.png'),
              'DEA(투입 3 × 산출 4) CCR 의 2015~2024년 대학별 평균을 다섯 구간 색으로'],
             ['지도 2 · LISA 국지 군집', 'docs/maps/map-lisa.png', '박사학위논문_지도2_LISA군집.png', kb('map-lisa.png'),
              '최근접 6개 이웃 기준, 순열 999회로 유의(p < 0.05)한 대학만 색으로']],
    'files': [['검정 결과 (엑셀)', 'docs/maps/spatial-prelim.xlsx', '예비분석_공간의존성.xlsx', kb('spatial-prelim.xlsx')],
              ['지도 점 자료 (CSV)', 'docs/maps/points.csv', '대학점.csv', kb('points.csv')]],
}

BLOCK = r'''/* ===================== 지도 (docs/_지도메뉴_패치.py 가 생성) ===================== */
var MAPDATA = __MAPDATA__;

function mapShow(i){
  var M = MAPDATA.maps[i], img = document.getElementById("mapImg");
  if(!img) return;
  img.src = M[1]; img.alt = M[0];
  document.getElementById("mapCap").textContent = M[4];
  var a = document.getElementById("mapDl"); a.href = M[1]; a.setAttribute("download", M[2]);
  document.getElementById("mapDlName").textContent = M[2] + " · " + M[3];
  Array.prototype.forEach.call(document.querySelectorAll(".mapsw .abtn"), function(b, k){ b.setAttribute("aria-pressed", k === i ? "true" : "false"); });
}

function scMap(){
  var D = MAPDATA, h = "";
  h += '<section class="stats">' +
    tile("대학", D.n + "교", "2015~2024 효율성이 있는 대학 · 실제 캠퍼스 좌표", "") +
    tile("Moran\'s I", D.global.split(" ")[0], "대학별 평균 CCR · " + D.global.replace(/^\S+\s*/, ""), "accv") +
    tile("연도별 검정", D.tests[0] + "/" + D.tests[1], "유의(p < 0.05) — 우연 수준 약 " + Math.round(D.tests[1] * 0.05) + "개", "") +
    tile("LISA 군집", D.lisa.replace(/[^0-9 ]/g, "").trim().split(/\s+/).reduce(function(a, b){ return a + (+b || 0); }, 0) + "교", D.lisa, "") +
    tile("거점국립대 거리", D.hub.split(" ")[0], "평균 CCR 과 순위상관 " + D.hub.replace(/^\S+\s*/, ""), "") +
    '</section>';

  h += '<section class="panel lift"><div class="panel-hd"><h2>공간 의존성 지도</h2>' +
    '<p class="hint">QGIS 3.40 · 교육지원청 경계 위 대학별 효율성 · 거점국립대 9개교 ★</p></div><div class="panel-bd">' +
    '<div class="mapsw">' + D.maps.map(function(m, i){
      return '<button class="abtn" type="button" aria-pressed="' + (i === 0) + '" onclick="mapShow(' + i + ')">' + esc(m[0]) + '</button>'; }).join("") + '</div>' +
    '<p class="mapcap" id="mapCap">' + esc(D.maps[0][4]) + '</p>' +
    '<figure class="mapfig"><img id="mapImg" src="' + D.maps[0][1] + '" alt="' + esc(D.maps[0][0]) + '" loading="lazy"></figure>' +
    '<div class="dlrow"><a class="abtn primary" id="mapDl" href="' + D.maps[0][1] + '" download="' + D.maps[0][2] + '">' +
    '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' +
    '<path d="M12 3v12"/><path d="m7 11 5 5 5-5"/><path d="M4 20h16"/></svg>지도 내려받기</a>' +
    '<span class="fname" id="mapDlName">' + esc(D.maps[0][2]) + ' · ' + D.maps[0][3] + '</span></div>' +
    '<p class="hint mapnote">※ ' + esc(D.pos) + '. 지도 자료 © OpenStreetMap 기여자, Wikidata.</p>' +
    '</div></section>';

  h += '<div class="dgrid">';
  h += '<section class="panel"><div class="panel-hd"><h2>공간 자기상관 (Moran\'s I)</h2>' +
    '<p class="hint">2015~2024 연도별 · 순열 999회 · 범위 ' + D.range[0] + ' ~ ' + D.range[1] + '</p></div><div class="panel-bd">' +
    '<div class="tablewrap"><table class="dt"><thead><tr><th>이웃 기준</th><th>변수</th><th class="n">평균 I</th><th class="n">최소 ~ 최대</th><th class="n">유의 연도</th></tr></thead><tbody>';
  D.moran.forEach(function(r){
    h += '<tr><td class="k">' + esc(r[0]) + '</td><td class="dim">' + esc(r[1]) + '</td><td class="n">' + r[2].toFixed(3) + '</td>' +
      '<td class="n">' + r[3].toFixed(3) + ' ~ ' + r[4].toFixed(3) + '</td><td class="n">' + r[5] + '/' + r[6] + '</td></tr>';
  });
  h += '</tbody></table></div></div></section>';

  h += '<section class="panel"><div class="panel-hd"><h2>거점국립대까지의 거리</h2>' +
    '<p class="hint">가장 가까운 거점국립대 · 거점 제외 ' + D.bins.reduce(function(a, b){ return a + b[1]; }, 0) + '교</p></div><div class="panel-bd">' +
    '<div class="tablewrap"><table class="dt"><thead><tr><th>거리</th><th class="n">대학</th><th class="n">평균 CCR</th><th class="n">평균 BCC</th></tr></thead><tbody>';
  D.bins.forEach(function(b){
    h += '<tr><td class="k">' + esc(b[0]) + '</td><td class="n">' + b[1] + '</td><td class="n">' + b[2].toFixed(3) + '</td><td class="n">' + b[3].toFixed(3) + '</td></tr>';
  });
  h += '</tbody></table></div><p class="hint" style="margin-top:10px">순위상관: 전체 ' + esc(D.hub) + ' · 비수도권 ' + esc(D.hub2) + '</p></div></section>';
  h += '</div>';

  h += '<div class="dgrid">';
  h += '<section class="panel"><div class="panel-hd"><h2>LISA 유의 대학</h2><p class="hint">' + esc(D.lisa) + '</p></div><div class="panel-bd">' +
    '<div class="tablewrap"><table class="dt"><thead><tr><th>대학</th><th>지역</th><th>군집</th><th class="n">평균 CCR</th><th class="n">p</th></tr></thead><tbody>';
  D.sig.forEach(function(r){
    h += '<tr><td class="k">' + esc(r[0]) + '</td><td class="dim">' + esc(r[1]) + '</td><td><span class="pill' +
      (r[2].charAt(0) === "고" ? " part" : "") + '">' + esc(r[2]) + '</span></td><td class="n">' + r[3].toFixed(3) + '</td><td class="n">' + r[4].toFixed(3) + '</td></tr>';
  });
  h += '</tbody></table></div></div></section>';

  h += '<section class="panel"><div class="panel-hd"><h2>읽는 법과 쓸 곳</h2><p class="hint">' + esc(D.updated) + ' 예비 검정</p></div><div class="panel-bd"><ul class="fbl">' +
    '<li><b>결론</b> — 가까운 대학끼리 효율성이 닮지 않는다. 시도 평균을 빼도 같고, 거점국립대와의 거리도 효율성과 무관하다.</li>' +
    '<li><b>논문에서</b> — 효율성 격차가 개별 대학에서 온다는 예비분석(71.8%)을 실제 거리로 재확인. 연구문제 3 재설정(확인 요청 아홉째)의 근거.</li>' +
    '<li><b>방법론</b> — Simar–Wilson 2단계의 관측치 독립 가정을 지지한다. 공간회귀(SAR·SDM)는 본 분석보다 제4장 강건성 한 문단으로.</li>' +
    '<li><b>위치</b> — 캠퍼스 실제 좌표(OpenStreetMap 184교 · Wikidata 6교, EPSG:5186). 교육지원청 중심점으로 계산했을 때와 결론이 같다.</li>' +
    '</ul><div style="display:flex;flex-direction:column;gap:10px;margin-top:14px">' +
    D.files.map(function(f){ return '<div class="dlrow"><a class="abtn" href="' + f[1] + '" download="' + f[2] + '">' + esc(f[0]) + ' 내려받기</a><span class="fname">' + esc(f[2]) + ' · ' + f[3] + '</span></div>'; }).join("") +
    '</div></div></section>';
  h += '</div>';
  return h;
}
/* ===================== 지도 끝 ===================== */'''.replace('__MAPDATA__', json.dumps(DATA, ensure_ascii=False))

s = open(IDX, encoding='utf-8').read()
START, END = '/* ===================== 지도 (docs/_지도메뉴_패치.py 가 생성) ===================== */', '/* ===================== 지도 끝 ===================== */'
if START in s:                                                     # 자료만 새로 고침
    a = s.index(START); b = s.index(END) + len(END)
    s = s[:a] + BLOCK + s[b:]
    print('자료 갱신')
else:
    NAV = '<span>피드백</span><span class="cnt" id="cntFb"></span></button>'
    assert NAV in s
    s = s.replace(NAV, NAV + '\n    <button class="navb" data-go="map"><svg viewBox="0 0 24 24">'
                  '<path d="M9 4 3 6.5v13.5l6-2.5 6 2.5 6-2.5V4l-6 2.5z"/><path d="M9 4v13.5M15 6.5V20"/></svg>'
                  '<span>지도</span><span class="cnt" id="cntMap"></span></button>', 1)
    R = '  feedback:{title:"피드백 반영", render:scFeedback}\n'
    assert R in s
    s = s.replace(R, '  feedback:{title:"피드백 반영", render:scFeedback},\n  map:{title:"공간 분석 지도", render:scMap}\n', 1)
    M = '  var cf = document.getElementById("cntFb");'
    assert M in s
    s = s.replace(M, '  var cm = document.getElementById("cntMap"); if(cm) cm.textContent = MAPDATA.maps.length + "장";\n' + M, 1)
    C = '.dlrow .fname{font-family:var(--f-mono); font-size:11.5px; color:var(--ink-3)}\n'
    assert C in s
    s = s.replace(C, C +
        '.mapsw{display:flex; gap:8px; flex-wrap:wrap}\n'
        '.mapsw .abtn[aria-pressed="true"]{background:var(--accent-soft); border-color:var(--accent-line); color:var(--accent-ink); font-weight:600}\n'
        '.mapcap{margin:10px 0 0; font-size:var(--t-xs); color:var(--ink-3)}\n'
        '.mapfig{margin:12px 0 14px; display:flex; justify-content:center}\n'
        '.mapfig img{width:100%; max-width:720px; height:auto; background:#fff; border:1px solid var(--line); border-radius:var(--r-s)}\n'
        '.mapnote{margin-top:10px}\n', 1)
    B0 = '/* ===================== 부팅 ===================== */'
    assert B0 in s
    s = s.replace(B0, BLOCK + '\n\n' + B0, 1)
    print('메뉴 추가')
open(IDX, 'w', encoding='utf-8').write(s)
