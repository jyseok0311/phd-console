/* ===================== 피드백 반영 ===================== */
/* 지도교수 피드백과 반영 여부. 원본은 박사학위논문/지도교수 면담/피드백_반영표.xlsx — 그 표를 고치면 이 상수도 맞춘다. */
var FEEDBACK = {
  updated: "2026. 9. 23.",
  file: "docs/feedback-tracker.xlsx",
  name: "피드백_반영표.xlsx",
  /* [피드백, 제기일, 반영한 것[], 아직 안 한 것[], 상태] */
  sum: [
    ["투입·산출변수 최대 확보", "9. 17.",
      ["투입 8 × 산출 10, 환경 55개로 확대", "모두 넣으면 효율=1 대학이 73.5% — 판별력이 사라짐을 검증 (7~10절)"],
      ["주 분석을 기본 3 × 4로 둘지 결정"], "결정 대기"],
    ["윈도우 분석 (EMS)", "9. 22.",
      ["3년 창·5년 창 계산 (두 결과 상관 0.978)", "EMS 입력 파일 준비 (11절)"],
      ["EMS 로 직접 돌려 결과 대조", "창 너비 확정"], "진행 중"],
    ["① 교육재정 비용변수 대폭 보강", "9. 23.",
      ["총교육비를 회계별 네 갈래로 분해 — 1,827행 합계 일치", "산학협력단 지출 ≈ 교외연구비(상관 0.969) 확인, 처리 방식 네 가지 비교 (13절)"],
      ["인건비·운영비 등 세부 비목 보강 — 국공립 원자료 재파싱 필요", "6절 확정안·7절 투입변수 표는 아직 총교육비"], "일부 반영"],
    ["② SFA 와 DEA", "9. 23.",
      ["SFA 추정 코드 작성·모의자료 검증, 16개 사양 추정", "DEA 와 순위상관 0.53, 비용 하나로 맞추면 0.68~0.72 — 41개 경우 전수 검토 (14·15절)"],
      ["SFA 를 주 모형으로 올릴지 결정", "패널 SFA(Greene 2005) · 투입가격 포함 비용함수 미추정"], "일부 반영"],
    ["③ 관련 이론 정리", "9. 23.",
      ["근거 이론 7개 → 11개 (T8~T11 비용·SFA 이론)", "문헌 20편 추가, 근거 이론 구성 v1.1 (3·4절)", "진행보고 문헌 집계·부록 257편으로 갱신 (16·17절)"],
      ["T8~T11 대표 문헌 원문 13편 미확보"], "반영"]
  ],
  /* [번호, 제기일, 피드백 요지, 대응 방향, 반영 위치, 커밋, 상태, 비고] — 피드백_반영표.xlsx 와 같은 순서 */
  items: [
    [1, "09-17", "투입·산출변수 최대 확보", "투입 8 × 산출 10, 환경 55개로 확대, 판별력 검증", "진행보고 7~10절 · 변수구성_최대안 v1.0", "8f92396", "검토 요청", "주 분석 3 × 4 제안 — 확인 요청 둘째"],
    [2, "09-22", "윈도우 분석 검토", "3년 창 8개·5년 창 6개 CCR·BCC, EMS 입력 파일", "진행보고 11절 · EMS입력_윈도우분석.xlsx", "fbbefc9", "진행 중", "EMS 대조, 창 너비 확정(여덟째)"],
    [3, "09-23", "① 비용변수 — 회계별 분해", "총교육비 → 본회계·산학협력단·도서구입비·기계기구매입비 + 발전기금", "진행보고 13절 · build_cost_vars.py", "3490086", "완료", "국공립 97% · 사립 98% 채움"],
    [4, "09-23", "① 비용변수 — 이중 계상", "산학협력단 지출 ≈ 교외연구비, M0~M3 비교", "진행보고 13절 · 이중계상_처리방식_비교.xlsx", "53981eb", "검토 요청", "본회계 투입 채택 — 확인 요청 열째"],
    [5, "09-23", "① 비용변수 — 세출 비목", "국공립 세출 비목 재파싱(라벨 오염, 분류 3회 변경)", "—", "", "미착수", "현재는 회계 단위 분해까지"],
    [6, "09-23", "① 비용변수 — 확정 모형 반영", "6절 확정안·7절 투입변수 표 교체", "—", "", "보류", "열째 결정 후 연구계획서 변수표와 함께"],
    [7, "09-23", "② SFA 와 DEA 비교", "SFA 16개 사양, DEA 와 순위상관, BC95 결정요인", "진행보고 14~15절 · 분석모형_전수검토 v1.0", "d53650d", "완료", "41개 경우 종합"],
    [8, "09-23", "② SFA — 주 모형 여부", "교차 검증 / 주 모형 결정 요청", "진행보고 18절", "", "검토 요청", "확인 요청 열한째"],
    [9, "09-23", "② SFA — 패널 · 투입가격", "Greene(2005) TRE/TFE, 투입가격 비용함수", "—", "", "미착수", "SFA 가 주 모형이 되면 착수"],
    [10, "09-23", "③ 관련 이론 정리", "근거 이론 11개, 비용 이론·SFA 문헌 20편", "진행보고 3~4절 · 근거이론_구성 v1.1", "92edc16", "완료", ""],
    [11, "09-23", "③ 이론 — 원문 확보", "T8~T11 대표 문헌 13편", "—", "", "미착수", "0 / 13 — 구독 DB 는 직접 내려받기"],
    [12, "09-23", "③ 이론 — 문헌 집계 갱신", "16·17절 집계와 부록에 20편 추가 (237 → 257편), 19절 교차참조 수정", "진행보고 16·17절 · 부록 1·2", "", "완료", "16절 표 A·D 수치·묶음 수 오류도 바로잡음"]
  ],
  /* 교수님 결정이 필요한 것 [사안, 제안, 확인 요청 번호] */
  ask: [
    ["변수 개수", "기본 3 × 4 를 주 분석으로, 최대안은 민감도로", "둘째"],
    ["비용 투입의 교체", "총교육비 대신 본회계 — 이중 계상 제거", "열째"],
    ["SFA 의 위상", "교차 검증으로 둘지 주 모형으로 올릴지", "열한째"]
  ],
  /* 결정과 무관하게 할 수 있는 것 [할 일, 관련 피드백] */
  todo: [
    ["국공립 세출 비목 재파싱", "피드백 ①"],
    ["T8~T11 대표 문헌 원문 13편 확보", "피드백 ③"],
    ["EMS 윈도우 분석 결과 대조 (직접 실행)", "윈도우 분석"]
  ]
};

function fbPill(st){
  var c = (st === "완료" || st === "반영") ? "ok" : (st === "미착수" || st === "보류") ? "" : "part";
  return '<span class="pill ' + c + '">' + esc(st) + '</span>';
}

function scFeedback(){
  var F = FEEDBACK, cnt = {};
  F.items.forEach(function(x){ cnt[x[6]] = (cnt[x[6]] || 0) + 1; });
  var n = F.items.length, done = cnt["완료"] || 0;
  var ul = function(a){ return '<ul class="fbl">' + a.map(function(t){ return '<li>' + esc(t) + '</li>'; }).join("") + '</ul>'; };
  var h = "";

  h += '<section class="stats">' +
    tile("피드백", F.sum.length + "건", "지도교수 · " + F.updated + " 기준", "accv") +
    tile("세부 항목", done + "/" + n, "완료 " + done + " · 검토 요청 " + (cnt["검토 요청"]||0) + " · 진행 중 " + (cnt["진행 중"]||0), "", done / n * 100) +
    tile("교수님 결정", F.ask.length + "건", "결정되어야 다음 단계로", "accv") +
    tile("남은 내 작업", F.todo.length + "건", "결정과 무관하게 할 수 있는 것", "") +
    '</section>';

  /* 피드백별 반영 현황 */
  h += '<section class="panel lift"><div class="panel-hd"><h2>피드백별 반영 현황</h2>' +
    '<p class="hint">③ 이론 정리만 끝까지 반영 · 나머지는 일부 반영이거나 결정 대기</p></div>' +
    '<div class="panel-bd"><div class="tablewrap"><table class="dt fbt"><thead>' +
    '<tr><th>피드백</th><th>반영한 것</th><th>아직 안 한 것</th><th>상태</th></tr></thead><tbody>';
  F.sum.forEach(function(x){
    h += '<tr><td class="k">' + esc(x[0]) + '<span class="fbd">' + esc(x[1]) + '</span></td>' +
      '<td>' + ul(x[2]) + '</td><td class="dim">' + ul(x[3]) + '</td><td>' + fbPill(x[4]) + '</td></tr>';
  });
  h += '</tbody></table></div></div></section>';

  h += '<div class="dgrid">';
  h += '<section class="panel"><div class="panel-hd"><h2>교수님 결정이 필요한 것</h2>' +
    '<p class="hint">진행보고 18절 확인 요청</p></div><div class="panel-bd">' +
    '<div class="tablewrap"><table class="dt"><thead><tr><th>사안</th><th>제안</th><th>요청</th></tr></thead><tbody>';
  F.ask.forEach(function(a){
    h += '<tr><td class="k">' + esc(a[0]) + '</td><td class="dim">' + esc(a[1]) + '</td><td><span class="pill part">' + esc(a[2]) + '</span></td></tr>';
  });
  h += '</tbody></table></div></div></section>';
  h += '<section class="panel"><div class="panel-hd"><h2>남은 내 작업</h2>' +
    '<p class="hint">교수님 결정과 무관하게 할 수 있는 것</p></div><div class="panel-bd">' +
    '<div class="tablewrap"><table class="dt"><thead><tr><th>할 일</th><th>관련</th></tr></thead><tbody>';
  F.todo.forEach(function(t){
    h += '<tr><td>' + esc(t[0]) + '</td><td class="dim">' + esc(t[1]) + '</td></tr>';
  });
  h += '</tbody></table></div></div></section>';
  h += '</div>';

  /* 세부 반영표 */
  h += '<section class="panel"><div class="panel-hd"><h2>세부 반영표</h2>' +
    '<p class="hint">' + n + '줄 · 심사 단계의 수정 대조표로 이어 씁니다</p></div><div class="panel-bd">' +
    '<div class="dlrow" style="margin-bottom:12px"><a class="abtn" href="' + F.file + '" download="' + F.name + '">' +
    '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" ' +
    'stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="m7 11 5 5 5-5"/><path d="M4 20h16"/></svg>' +
    '반영표 내려받기</a><span class="fname">' + esc(F.name) + ' · 엑셀</span></div>' +
    '<div class="tablewrap"><table class="dt"><thead><tr><th class="n">#</th><th>제기일</th><th>피드백 요지</th>' +
    '<th>대응 방향</th><th>반영 위치</th><th>커밋</th><th>상태</th><th>비고</th></tr></thead><tbody>';
  F.items.forEach(function(x){
    h += '<tr><td class="n">' + x[0] + '</td><td class="dim">' + esc(x[1]) + '</td><td class="k">' + esc(x[2]) + '</td>' +
      '<td class="dim">' + esc(x[3]) + '</td><td class="dim">' + esc(x[4]) + '</td>' +
      '<td class="dim mono">' + esc(x[5]) + '</td><td>' + fbPill(x[6]) + '</td><td class="dim">' + esc(x[7]) + '</td></tr>';
  });
  h += '</tbody></table></div></div></section>';
  return h;
}
