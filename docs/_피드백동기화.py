# -*- coding: utf-8 -*-
"""피드백 반영표(엑셀) → 콘솔 「피드백」 화면 동기화 (2026-09-29).

원본은 박사학위논문/지도교수 면담/피드백_반영표.xlsx 하나다. 이 스크립트가
  - 엑셀을 docs/feedback-tracker.xlsx 로 복사하고(내려받기용),
  - index.html 의 FEEDBACK.items(세부 반영표)를 엑셀의 「피드백 반영표」 시트 내용으로 다시 쓴다.
엑셀을 고친 뒤 이것만 실행하면 콘솔의 세부 표·상태 집계·「완료 n/m」 배지가 함께 맞춰진다.
피드백별 요약(sum)·결정 요청(ask)·남은 작업(todo)은 글이 길어 index.html 에서 직접 고친다.

  python docs/_피드백동기화.py      (phd-console 폴더에서)
"""
import os, re, json, shutil
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.join(HERE, '..', 'index.html')
XL = r'C:\Users\User\Desktop\박사학위논문\지도교수 면담\피드백_반영표.xlsx'
shutil.copyfile(XL, os.path.join(HERE, 'feedback-tracker.xlsx'))

ws = openpyxl.load_workbook(XL)['피드백 반영표']
STATUS = {'미착수', '진행 중', '검토 요청', '완료', '보류'}
items = []
for r in ws.iter_rows(min_row=4, values_only=True):
    if not r[3]:                                                  # 피드백 요지가 없으면 빈 줄
        continue
    assert r[8] in STATUS, ('상태가 목록에 없음', r[3], r[8])
    items.append([len(items) + 1, str(r[1])[5:], r[3], r[5] or '', r[6] or '—', r[7] or '', r[8], r[10] or ''])

body = ',\n'.join('    ' + json.dumps(x, ensure_ascii=False) for x in items).replace('", "', '", "')
s = open(IDX, encoding='utf-8').read()
pat = re.compile(r'(  items: \[\n).*?(\n  \],\n  /\* 교수님 결정이 필요한 것)', re.S)
assert len(pat.findall(s)) == 1
s = pat.sub(lambda m: m.group(1) + body + m.group(2), s, count=1)
open(IDX, 'w', encoding='utf-8').write(s)
done = sum(x[6] == '완료' for x in items)
print('반영표 %d줄 · 완료 %d · 상태 %s' % (len(items), done, {k: sum(x[6] == k for x in items) for k in STATUS}))
