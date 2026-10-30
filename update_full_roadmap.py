"""Generate complete M1 I-3 (TradingView Fidelity) Roadmap for Mindjet MindManager."""

import os
import sys
import shutil

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.com_bridge import MindManagerBridge

bridge = MindManagerBridge()
doc = bridge.get_active_doc()
print(f"Connected to MindManager doc: {doc.Name}", flush=True)

ct = doc.CentralTopic
ct.Text = "AI Trading Workbench: Итерация M1 I-3 (TradingView Fidelity)"
bridge.set_topic_notes(
    ct.Text,
    "Мастер-план и статус оркестрации итерации M1 I-3.\n"
    "Базовый коммит: bb63f37416702ff04d9ab1d0349dd49281f7c23c (origin/main, v0.2.0-i2)\n"
    "Рабочая ветка: feature/m1-i3-tradingview-fidelity (HEAD 391280e)\n"
    "Модель управления: Главный Orchestrator + изолированные субагенты Claude Code (Opus / Sonnet)\n"
    "Правило R-005: 1 активная задача в момент времени, переход строго по ACCEPTED зависимостям.\n"
    "Внешняя память: F:\\Мой диск\\Проекты AI\\001-AI Trading\\03_STAGES\\Stage_002_Trading_Workbench_M1\\M1_I3_IMPLEMENTATION"
)
bridge.set_style(ct.Text, shape="CAPSULE", fill_color="#0F2942", text_color="#FFFFFF", bold=True, font_size=13)

# Очистка старых веток
while ct.AllSubTopics.Count > 0:
    ct.AllSubTopics.Item(1).Delete()
print("Cleaned existing subtopics", flush=True)

# ==============================================================================
# 1. Фаза P0: Входные ворота и окружение
# ==============================================================================
p0 = bridge.add_subtopic(
    ct.Text,
    "Фаза P0: Стартовые ворота и окружение",
    notes="Подготовка среды, изоляция Docker, бэкап БД на диск F:, проверка REA MCP и Chrome CDP.",
    shape="ROUNDED_RECTANGLE",
    fill_color="#EBF8FF",
    text_color="#2B6CB0",
)
bridge.add_icon("Фаза P0: Стартовые ворота и окружение", "CHECK")

bridge.add_subtopic(
    "Фаза P0: Стартовые ворота и окружение",
    "PRE-000: Установка REA MCP для Claude Code",
    notes="Нативная интеграция MCP-сервера REA в сессию Claude Code для анализа верстки TradingView.",
    complete_percent=100,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_subtopic(
    "Фаза P0: Стартовые ворота и окружение",
    "TASK-001: Изоляция Docker, бэкап БД и baseline I-1/I-2",
    notes="Ветка от bb63f37; тестовый стек aitrading-i3test (порт 8180); бэкап pg_dump на F: (1:1 restore); baseline PASS. Gate GO (I3_BASELINE_AND_GATE.md).",
    complete_percent=100,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_subtopic(
    "Фаза P0: Стартовые ворота и окружение",
    "TASK-002: REA Runtime Proof + Chrome CDP (9222)",
    notes="Выделенный профиль Chrome (claude-rea-chrome), проверка CDP 127.0.0.1:9222, smoke TradingView, REA_RUNTIME_PROOF.md, DEV_REA_DELTA_LOG.md.",
    complete_percent=100,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_boundary("Фаза P0: Стартовые ворота и окружение", shape="ROUNDED_RECTANGLE", line_color="#3182CE", line_style="DASH")
print("P0 added", flush=True)

# ==============================================================================
# 2. Фаза P1: OBS-ядро, аудит и надёжность
# ==============================================================================
p1 = bridge.add_subtopic(
    ct.Text,
    "Фаза P1: OBS-ядро, аудит и наблюдаемость",
    notes="Сквозная трассировка OpenTelemetry, структурированные JSON-логи, аудит мутаций и soak-тестирование.",
    shape="ROUNDED_RECTANGLE",
    fill_color="#EDF2F7",
    text_color="#2D3748",
)
bridge.add_icon("Фаза P1: OBS-ядро, аудит и наблюдаемость", "CHECK")

bridge.add_subtopic(
    "Фаза P1: OBS-ядро, аудит и наблюдаемость",
    "TASK-003: OBS-ядро бэкенда (OTel SDK, JSON-логи)",
    notes="JSON-логирование, маскирование секретов, каталог OBS_EVENT_CATALOG.md, operation_id/traceparent, метрики.",
    complete_percent=100,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_subtopic(
    "Фаза P1: OBS-ядро, аудит и наблюдаемость",
    "TASK-004: Аудит (миграция 0005) и события безопасности",
    notes="Миграция 0005_audit_log (append-only триггер, fail-closed rollback при ошибке), аудит IDOR, эмуляция WS/Binance ошибок.",
    complete_percent=100,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_subtopic(
    "Фаза P1: OBS-ядро, аудит и наблюдаемость",
    "TASK-005: OBS на фронтенде, collector и soak-тест",
    notes="Фронтенд sdk-trace-web, collector в docker-compose.obs.yml, obs_report.py, soak-тест 70+ мин, OBS_BASE_VERIFICATION.md.",
    complete_percent=100,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_boundary("Фаза P1: OBS-ядро, аудит и наблюдаемость", shape="ROUNDED_RECTANGLE", line_color="#718096", line_style="DASH")
print("P1 added", flush=True)

# ==============================================================================
# 3. Фаза P2: 5-зонная оболочка и панели
# ==============================================================================
p2 = bridge.add_subtopic(
    ct.Text,
    "Фаза P2: 5-зонная оболочка и панели интерфейса",
    notes="Декомпозиция шелла Workbench на зоны, интеграция эталонных токенов Cold Gray, Topbar, Bottombar и правый док.",
    shape="ROUNDED_RECTANGLE",
    fill_color="#EBF8FF",
    text_color="#2B6CB0",
)
bridge.add_icon("Фаза P2: 5-зонная оболочка и панели интерфейса", "CHECK")

bridge.add_subtopic(
    "Фаза P2: 5-зонная оболочка и панели интерфейса",
    "TASK-006: Каркас 5-зонной оболочки UI",
    notes="Зоны: topbar, leftbar, right, bottom, floating. Popover, Menu, Modal, Tooltip (Esc, click-outside). 12 SVG иконок.",
    complete_percent=100,
    priority=2,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_subtopic(
    "Фаза P2: 5-зонная оболочка и панели интерфейса",
    "TASK-007: Topbar, нижняя панель и правый dock (45..346px)",
    notes="Верхний тулбар, диапазоны дат/таймзоны, правый dock с ресайзом KLineChart. Закрытие Issue #5 AC-01..04.",
    complete_percent=100,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_boundary("Фаза P2: 5-зонная оболочка и панели интерфейса", shape="ROUNDED_RECTANGLE", line_color="#3182CE", line_style="SOLID")
print("P2 added", flush=True)

# ==============================================================================
# 4. Фаза P3: Темы и стили свечей
# ==============================================================================
p3 = bridge.add_subtopic(
    ct.Text,
    "Фаза P3: Темы и стили отображения свечей",
    notes="Поддержка тёмной/светлой темы, режимы hollow/stroke свечей, палитра цветов.",
    shape="ROUNDED_RECTANGLE",
    fill_color="#FAF5FF",
    text_color="#6B46C1",
)
bridge.add_icon("Фаза P3: Темы и стили отображения свечей", "CHECK")

bridge.add_subtopic(
    "Фаза P3: Темы и стили отображения свечей",
    "TASK-008: Темы dark/light и стили свечей (setStyles)",
    notes="Backend ui_theme, style_json.candle; tokens.css dark/light; режимы candle_up_stroke, candle_solid, candle_stroke, area, ohlc; сохранение.",
    complete_percent=100,
    priority=2,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_boundary("Фаза P3: Темы и стили отображения свечей", shape="ROUNDED_RECTANGLE", line_color="#805AD5", line_style="DASH")
print("P3 added", flush=True)

# ==============================================================================
# 5. Фаза P4: Инструменты рисования и каноническая модель
# ==============================================================================
p4 = bridge.add_subtopic(
    ct.Text,
    "Фаза P4: Инструменты рисования и оверлеи (ЯДРО)",
    notes="Полный набор 13 инструментов рисования TradingView, каноническая модель, панель свойств и дерево объектов.",
    shape="ROUNDED_RECTANGLE",
    fill_color="#FEFCBF",
    text_color="#744210",
)
bridge.add_icon("Фаза P4: Инструменты рисования и оверлеи (ЯДРО)", "ROCKET")

bridge.add_subtopic(
    "Фаза P4: Инструменты рисования и оверлеи (ЯДРО)",
    "TASK-009: Серверная модель рисунков (миграция 0006)",
    notes="Миграция 0006_drawing_types, point_kind time_only / time_price, типизированные схемы до 8 КБ, адаптация semantics.ts / DrawingService.ts.",
    complete_percent=100,
    priority=1,
    shape="DATABASE",
)
bridge.add_icon("TASK-009: Серверная модель рисунков (миграция 0006)", "CHECK")

t10 = bridge.add_subtopic(
    "Фаза P4: Инструменты рисования и оверлеи (ЯДРО)",
    "TASK-010: Левая панель, избранное, 7 линейных инструментов [В РАБОТЕ]",
    notes="Левая панель, плавающее избранное (settings.favorites_bar), 7 инструментов (Vertical, Trend, Horiz Line, Horiz Ray, Extended, Rect, Parallel Channel). Issue #5 AC-10. Запас бандла >= 3 КБ, фикс e2e 11.",
    complete_percent=20,
    priority=1,
    shape="ROUNDED_RECTANGLE",
    fill_color="#FFFDF0",
    line_color="#D69E2E",
)
bridge.set_task("TASK-010: Левая панель, избранное, 7 линейных инструментов [В РАБОТЕ]", due_date="2026-10-31", resources=["Claude Code (Opus)"])
bridge.add_icon("TASK-010: Левая панель, избранное, 7 линейных инструментов [В РАБОТЕ]", "CLOCK")
bridge.add_callout("TASK-010: Левая панель, избранное, 7 линейных инструментов [В РАБОТЕ]", "ТЕКУЩИЙ ЭТАП КЛОДА! Активная задача в TASK_BOARD.md")

bridge.add_subtopic(
    "Фаза P4: Инструменты рисования и оверлеи (ЯДРО)",
    "TASK-011: Сложные инструменты: Path, стрелки, позиции, FRVP",
    notes="Path (полилиния N точек), Arrow Up/Down (1 точка), Long/Short Position (расчёт R:R), FRVP (Volume Profile: POC, VAH, VAL сопоставление с TV).",
    complete_percent=0,
    priority=2,
    shape="ROUNDED_RECTANGLE",
)
bridge.set_task("TASK-011: Сложные инструменты: Path, стрелки, позиции, FRVP", due_date="2026-11-03", resources=["Claude Code"])

bridge.add_subtopic(
    "Фаза P4: Инструменты рисования и оверлеи (ЯДРО)",
    "TASK-012: Панель свойств, настройки, Undo/Redo, Object Tree",
    notes="DrawingPropertiesBar, DrawingSettingsDialog, Lock/Hide/Delete, видимость по TF, Undo/Redo, Object Tree со слоями. Issue #10 P-1 (Auto/Log/%).",
    complete_percent=0,
    priority=2,
    shape="ROUNDED_RECTANGLE",
)
bridge.set_task("TASK-012: Панель свойств, настройки, Undo/Redo, Object Tree", due_date="2026-11-05", resources=["Claude Code"])

bridge.add_boundary("Фаза P4: Инструменты рисования и оверлеи (ЯДРО)", shape="ROUNDED_RECTANGLE", line_color="#D69E2E", line_style="SOLID")
print("P4 added", flush=True)

# ==============================================================================
# 6. Фаза P5: Индикаторы и подпанели
# ==============================================================================
p5 = bridge.add_subtopic(
    ct.Text,
    "Фаза P5: Каталог индикаторов и подпанели",
    notes="Каталог индикаторов KLineChart 10.1.0, модальное окно выбора, легенда, настройки параметров и drag-ресайз высот подпанелей.",
    shape="ROUNDED_RECTANGLE",
    fill_color="#F0FFF4",
    text_color="#22543D",
)

bridge.add_subtopic(
    "Фаза P5: Каталог индикаторов и подпанели",
    "TASK-013: Каталог индикаторов, легенда, подпанели (Issue #5 AC-05..09)",
    notes="Инвентаризация индикаторов, каталог 840x638, вынос ATR над свечами, SQZMOM в подвале, ресайз и сохранение высот панелей WorkspaceChart.indicators.",
    complete_percent=0,
    priority=2,
    shape="ROUNDED_RECTANGLE",
)
bridge.set_task("TASK-013: Каталог индикаторов, легенда, подпанели (Issue #5 AC-05..09)", due_date="2026-11-08", resources=["Claude Code"])
bridge.add_boundary("Фаза P5: Каталог индикаторов и подпанели", shape="ROUNDED_RECTANGLE", line_color="#38A169", line_style="DASH")
print("P5 added", flush=True)

# ==============================================================================
# 7. Фаза P6: Мульти-чарт сетка 1..16 окон
# ==============================================================================
p6 = bridge.add_subtopic(
    ct.Text,
    "Фаза P6: Мульти-чарт сетка (1..16 окон), Watchlist и Sync",
    notes="Раскладки на 1, 2, 3, 4, 6, 8, 9, 12, 16 окон, синхронизация курсоров, таймфреймов и символов, Watchlist.",
    shape="ROUNDED_RECTANGLE",
    fill_color="#EDF2F7",
    text_color="#2D3748",
)

bridge.add_subtopic(
    "Фаза P6: Мульти-чарт сетка (1..16 окон), Watchlist и Sync",
    "TASK-014: GridContainer (1..16 окон), Watchlist, Sync-меню, Maximize",
    notes="Раскладки 1..16 окон + 5 TF, Maximize/Restore окна без сброса стейта, Watchlist (settings.watchlist), Issue #10 P-5 (сохранение dock/часового пояса).",
    complete_percent=0,
    priority=2,
    shape="ROUNDED_RECTANGLE",
)
bridge.set_task("TASK-014: GridContainer (1..16 окон), Watchlist, Sync-меню, Maximize", due_date="2026-11-11", resources=["Claude Code"])
bridge.add_boundary("Фаза P6: Мульти-чарт сетка (1..16 окон), Watchlist и Sync", shape="ROUNDED_RECTANGLE", line_color="#4A5568", line_style="DASH")
print("P6 added", flush=True)

# ==============================================================================
# 8. Фаза P7: Приёмка, верификация и релиз
# ==============================================================================
p7 = bridge.add_subtopic(
    ct.Text,
    "Фаза P7: Комплексная приёмка, аудит и релиз",
    notes="Полный цикл сквозной верификации: безопасность, миграции, мультипользовательский режим, сравнение с TradingView и закрытие Issue #5, #6, #10.",
    shape="ROUNDED_RECTANGLE",
    fill_color="#FFF5F5",
    text_color="#742A2A",
)

bridge.add_subtopic(
    "Фаза P7: Комплексная приёмка, аудит и релиз",
    "TASK-015: Полная приёмка (миграция, 2 юзера, 5/16 окон, TV-сравнение)",
    notes="Прогон миграций на копии рабочей БД, 2 пользователя (IDOR API/WS), нагрузка 5/16 окон vs I-2, визуальное и пиксельное сравнение в 2 viewport. Закрытие AC-01..12.",
    complete_percent=0,
    priority=1,
    shape="DOCUMENT",
)
bridge.set_task("TASK-015: Полная приёмка (миграция, 2 юзера, 5/16 окон, TV-сравнение)", due_date="2026-11-14", resources=["Orchestrator", "Playwright", "Слава"])

bridge.add_subtopic(
    "Фаза P7: Комплексная приёмка, аудит и релиз",
    "TASK-016: Публикация, Heptabase, PR и RETURN_HANDOFF.md",
    notes="Итоговые отчёты, релизный манифест, архив артефактов, PR в upstream, синхронизация с базой Heptabase, финальный RETURN_HANDOFF.md.",
    complete_percent=0,
    priority=1,
    shape="DOCUMENT",
)
bridge.set_task("TASK-016: Публикация, Heptabase, PR и RETURN_HANDOFF.md", due_date="2026-11-16", resources=["Orchestrator", "Claude Code"])

bridge.add_boundary("Фаза P7: Комплексная приёмка, аудит и релиз", shape="ROUNDED_RECTANGLE", line_color="#E53E3E", line_style="SOLID")
print("P7 added", flush=True)

# ==============================================================================
# 9. Блок: Контроль решений (Change Control R-005)
# ==============================================================================
gov = bridge.add_subtopic(
    ct.Text,
    "Контроль решений и Owner-Issues (R-005)",
    notes="Ключевые контракты владельца проекта (Славы) и критерии приёмки архитектуры.",
    shape="ROUNDED_RECTANGLE",
    fill_color="#E2E8F0",
    text_color="#1A202C",
)

bridge.add_subtopic(
    "Контроль решений и Owner-Issues (R-005)",
    "Issue #5: Динамическая компоновка (AC-01..12)",
    notes="12 критериев динамической компоновки (AC-01..04 приняты в TASK-007, AC-10 в TASK-010, AC-05..09 в TASK-013, AC-11..12 в TASK-014/015).",
    complete_percent=33,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_subtopic(
    "Контроль решений и Owner-Issues (R-005)",
    "Issue #6: Правило R-005 (закрыто 29.10)",
    notes="Строгий регламент сдачи задач: любая модификация требований оформляется через отдельный Issue перед кодом.",
    complete_percent=100,
    priority=2,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_subtopic(
    "Контроль решений и Owner-Issues (R-005)",
    "Issue #10: Решения владельца 29.10 (P-1, P-5)",
    notes="P-1: Кнопки Auto/Log/% переносятся в контекстное меню шкалы цен (TASK-012). P-5: Сохранение ширины дока и часового пояса индивидуально для каждой раскладки (TASK-014).",
    complete_percent=100,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)
print("Gov added", flush=True)

# ==============================================================================
# 10. Связи со стрелками (Relationships)
# ==============================================================================
# Поток P4 (Инструменты рисования)
bridge.add_relationship(
    "TASK-009: Серверная модель рисунков (миграция 0006)",
    "TASK-010: Левая панель, избранное, 7 линейных инструментов [В РАБОТЕ]",
    label="Канонические типы и схемы",
    line_color="#D69E2E",
    line_style="SOLID",
)

bridge.add_relationship(
    "TASK-010: Левая панель, избранное, 7 линейных инструментов [В РАБОТЕ]",
    "TASK-011: Сложные инструменты: Path, стрелки, позиции, FRVP",
    label="Базовые оверлеи -> Сложные",
    line_color="#D69E2E",
    line_style="SOLID",
)

bridge.add_relationship(
    "TASK-011: Сложные инструменты: Path, стрелки, позиции, FRVP",
    "TASK-012: Панель свойств, настройки, Undo/Redo, Object Tree",
    label="13 инструментов -> Свойства и дерево",
    line_color="#D69E2E",
    line_style="SOLID",
)

# Переход от P4 к P5 и P6
bridge.add_relationship(
    "TASK-012: Панель свойств, настройки, Undo/Redo, Object Tree",
    "TASK-013: Каталог индикаторов, легенда, подпанели (Issue #5 AC-05..09)",
    label="Свойства и дерево -> Индикаторы",
    line_color="#38A169",
    line_style="SOLID",
)

bridge.add_relationship(
    "TASK-013: Каталог индикаторов, легенда, подпанели (Issue #5 AC-05..09)",
    "TASK-014: GridContainer (1..16 окон), Watchlist, Sync-меню, Maximize",
    label="Индикаторы -> Мультиокна 1..16",
    line_color="#3182CE",
    line_style="SOLID",
)

bridge.add_relationship(
    "TASK-014: GridContainer (1..16 окон), Watchlist, Sync-меню, Maximize",
    "TASK-015: Полная приёмка (миграция, 2 юзера, 5/16 окон, TV-сравнение)",
    label="Интеграция -> Приёмка AC-01..12",
    line_color="#E53E3E",
    line_style="SOLID",
)

# Связь Issue #10 c TASK-012 и TASK-014
bridge.add_relationship(
    "Issue #10: Решения владельца 29.10 (P-1, P-5)",
    "TASK-012: Панель свойств, настройки, Undo/Redo, Object Tree",
    label="P-1: Auto/Log/% в меню шкалы",
    line_color="#805AD5",
    line_style="DASH",
)

bridge.add_relationship(
    "Issue #10: Решения владельца 29.10 (P-1, P-5)",
    "TASK-014: GridContainer (1..16 окон), Watchlist, Sync-меню, Maximize",
    label="P-5: dock и часовой пояс по раскладкам",
    line_color="#805AD5",
    line_style="DASH",
)
print("Relationships added", flush=True)

# 11. Review Comment
bridge.add_comment(
    "TASK-010: Левая панель, избранное, 7 линейных инструментов [В РАБОТЕ]",
    "Внимание Orchestrator: пауза 29.10 из-за лимитов кредитов. Готов к возобновлению новым субагентом Opus с tasks/TASK-010-SPEC.md.",
    "Max AI (Navigator)",
)
print("Comment added", flush=True)

# 12. Сохранение и копирование
save_doc_path = os.path.expanduser(r"~\Documents\AI-Trading-I3-Fidelity-Roadmap.mmap")
doc.SaveAs(save_doc_path)
print(f"Map saved to: {save_doc_path}", flush=True)

ai_trading_path = r"D:\Dev\AI-Trading\AI-Trading-I3-Fidelity-Roadmap.mmap"
shutil.copy2(save_doc_path, ai_trading_path)
print(f"Map copied to project folder: {ai_trading_path}", flush=True)

os.startfile(ai_trading_path)
print(f"SUCCESS: Full M1 I-3 Roadmap (17 tasks, P0-P7) populated, saved and opened in GUI!", flush=True)
