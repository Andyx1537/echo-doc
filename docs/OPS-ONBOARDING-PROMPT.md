# 建档旁白快照消费

状态：现行 · 2026-09-17
依据：`SPEC-private-pet-onboarding-questionnaire` §6.5/§6.6；`CURRENT-DELIVERY-STATUS` B03
执行：`docs/handoff/onboarding-snapshot-prompt.md`

## 概述

- 生成锚点冻四类快照。旁白只吃**码**，不吃 JSON、自由文本、资源 id。
- 四行：`subject` 已选主体类型/种；`assets` 已选素材 mediaType；`answers` 问卷码；`facts` 仅 `allowedUses` 含 `private_generation` 的 `dimension:value`。
- 模板版本 `private-onboarding-v2`，写进锚点 `promptTemplateVersion`。
- 漫画/视频、把快照整段塞进模型、编造心理标签，都不做。

## 消费表

| 行 | 来源 | 写入 | 不写 |
|---|---|---|---|
| subject | subjectSnapshot | 已选 `modelType/species` | subjectId、框、置信度 |
| assets | assetSnapshot | 已选 `mediaType` | resourceId、质量原因 |
| answers | answerSnapshot | `answerCodes` | questionId、freeText |
| facts | factSnapshot | 允许私域生成的 `dimension:value` | 未授权用途、已替代事实 |

## 红线

- 禁止把自由文本或内部评审 JSON 送进旁白。
- 事实没有 `private_generation` 就不进 prompt。
- 不像时先对锚点四快照和模板版本，不先怪模型。
