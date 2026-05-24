# Copied from tools-schooldata (github.com/akarpo/tools-schooldata) on 2026-05-24.
# Canonical version lives in that repo.
# Requires: playwright>=1.40  (pip install playwright && playwright install chromium)
"""
mischooldata.py — a reusable scraper for CEPI / MI School Data dashboards
(mischooldata.org).

Why this exists
---------------
MI School Data report pages look simple but are layered:

  * an Umbraco CMS shell page, on top of
  * cascading dropdowns rendered by the *bootstrap-multiselect* jQuery plugin
    (each real <select> is hidden; the visible widget is a <button> + <ul>), on
    top of
  * one or more checkbox groups, which feed
  * a "view-report" button that renders the actual report into an iframe named
    `results-frame`, pointed at legacy.mischooldata.org.

That layering defeats naive scraping:
  - setting a hidden <select>'s value does NOT fire the page's "settings
    complete" tracker (it listens to the plugin's onChange);
  - the legacy report URL can't be fetched directly (login wall) — it must be
    reached through the embed;
  - the view-report button is often not "visible" to Playwright's click;
  - the data lives in the iframe's DOM, not the outer page.

The recipe that works (encapsulated below):
  1. open the "Location and Report Settings" panel
  2. for each dropdown, drive bootstrap-multiselect via its jQuery API:
        $('#id').multiselect('select', value, true)   # 3rd arg fires onChange
        $('#id').trigger('change')                    # fires the AJAX cascade
  3. set any checkbox group(s) by clicking the inputs
  4. fire the report with  $('button.view-report-button').trigger('click')
     (jQuery trigger — NOT a native .click(), NOT Playwright's click())
  5. read tables (or click toggles like "Snapshot"/"Trend") inside the
     `results-frame` iframe

Requirements: playwright  (pip install playwright && playwright install chromium)

This module is report-agnostic. See examples/ for concrete usage against the
"Schools of Choice and Other Non-Resident Enrollments" report.
"""
from playwright.sync_api import sync_playwright


class MiSchoolDataReport:
    """Drives a single MI School Data report page.

    Usage:
        with MiSchoolDataReport(URL) as r:
            r.select("isd", "106")
            r.select("district", "1608")
            ...
            r.set_checkbox_group(["ChoiceInsideISD", "ChoiceOutsideISD"])
            r.fire_report()
            r.click_in_results("Trend")          # optional view toggle
            tables = r.results_tables()
    """

    def __init__(self, report_url, headless=True, viewport=(1600, 1100),
                 step_pause_ms=3000, report_pause_ms=11000):
        self.report_url = report_url
        self.headless = headless
        self.viewport = viewport
        self.step_pause_ms = step_pause_ms      # wait after each cascade step
        self.report_pause_ms = report_pause_ms  # wait after firing the report
        self._pw = None
        self._browser = None
        self.page = None

    # -- lifecycle -----------------------------------------------------------
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *exc):
        self.close()

    def open(self):
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(headless=self.headless)
        ctx = self._browser.new_context(
            viewport={"width": self.viewport[0], "height": self.viewport[1]})
        self.page = ctx.new_page()
        self.page.goto(self.report_url, wait_until="domcontentloaded", timeout=60000)
        self.page.wait_for_timeout(5000)
        # open the "Location and Report Settings" panel if present
        btn = self.page.query_selector("button.location-settings-button")
        if btn:
            btn.click()
            self.page.wait_for_timeout(1500)
        return self

    def close(self):
        if self._browser:
            self._browser.close()
        if self._pw:
            self._pw.stop()
        self._browser = self._pw = self.page = None

    # -- controls ------------------------------------------------------------
    def options(self, select_id):
        """Return [(value, label), ...] for a (possibly hidden) <select>."""
        return self.page.eval_on_selector_all(
            f'#{select_id} option',
            "els => els.map(o => [o.value, (o.textContent||'').trim()])")

    def select(self, select_id, value, timeout=25000):
        """Select `value` on a bootstrap-multiselect <select> by id.

        Sends BOTH the plugin's onChange (so the settings-tracker updates) and
        the native change event (so the dependent dropdowns cascade)."""
        self.page.wait_for_selector(f'#{select_id} option[value="{value}"]',
                                    timeout=timeout, state="attached")
        self.page.evaluate(
            """([id, val]) => {
                const $e = window.jQuery('#' + id);
                $e.multiselect('select', val, true);  // true => fire onChange
                $e.trigger('change');                 // => run the AJAX cascade
            }""",
            [select_id, value])
        self.page.wait_for_timeout(self.step_pause_ms)

    def select_no_cascade(self, select_id, value, timeout=25000):
        """Select `value` without firing the native change event.

        Use this for late-stage dropdowns (e.g. reportCategories) where the
        AJAX cascade would reset earlier selections (e.g. subjects).  The
        multiselect onChange still fires so the settings tracker enables the
        View Report button."""
        self.page.wait_for_selector(f'#{select_id} option[value="{value}"]',
                                    timeout=timeout, state="attached")
        self.page.evaluate(
            """([id, val]) => {
                const $e = window.jQuery('#' + id);
                $e.multiselect('select', val, true);
            }""",
            [select_id, value])
        self.page.wait_for_timeout(self.step_pause_ms)

    def set_checkbox_group(self, wanted_values,
                           value_regex=r"."):
        """Tick exactly `wanted_values` in a checkbox group, untick the rest.

        Targets <input type=checkbox> elements that are NOT inside a
        bootstrap-multiselect container and whose `value` matches `value_regex`.
        Pass a tighter `value_regex` if a page has multiple checkbox groups."""
        self.page.evaluate(
            """([wanted, rx]) => {
                const re = new RegExp(rx);
                const boxes = [...document.querySelectorAll('input[type=checkbox]')]
                    .filter(e => !e.closest('.multiselect-container') && re.test(e.value));
                for (const b of boxes) {
                    const want = wanted.includes(b.value);
                    if (b.checked !== want) b.click();
                }
            }""",
            [list(wanted_values), value_regex])
        self.page.wait_for_timeout(self.step_pause_ms)

    def view_button_state(self):
        """Return (class, text) of the view-report button — useful to confirm
        it left the disabled 'Settings Require Changes' state."""
        vb = self.page.locator("button.view-report-button")
        return vb.get_attribute("class"), vb.inner_text()

    def fire_report(self):
        """Click the view-report button via jQuery (its handler is jQuery-bound;
        a native click or Playwright click won't trigger it)."""
        self.page.evaluate("() => window.jQuery('button.view-report-button').trigger('click')")
        self.page.wait_for_timeout(self.report_pause_ms)

    # -- results iframe ------------------------------------------------------
    def _results_frame(self):
        fr = next((f for f in self.page.frames if f.name == "results-frame"), None)
        if fr is None:
            raise RuntimeError("results-frame iframe not found — was fire_report() called?")
        return fr

    def click_in_results(self, text, wait_ms=9000):
        """Click an element inside the results iframe whose text/value equals
        `text` (e.g. the 'Snapshot' / 'Trend' view toggles). Returns True/False."""
        rf = self._results_frame()
        clicked = rf.evaluate(
            """(text) => {
                const els = [...document.querySelectorAll('a,button,label,span,input')];
                const t = els.find(e => ((e.innerText||e.value||'').trim()) === text);
                if (t) { t.click(); return true; }
                return false;
            }""", text)
        if clicked:
            self.page.wait_for_timeout(wait_ms)
        return clicked

    def results_tables(self, min_rows=1):
        """Return every <table> inside the results iframe as a list of
        row-lists (each row a list of cell strings)."""
        rf = self._results_frame()
        return rf.evaluate(
            """(minRows) => [...document.querySelectorAll('table')]
                .map(t => [...t.querySelectorAll('tr')]
                    .map(tr => [...tr.querySelectorAll('th,td')]
                        .map(c => c.innerText.trim())))
                .filter(t => t.length >= minRows)""",
            min_rows)

    def results_text(self):
        """Raw innerText of the results iframe body (handy for debugging)."""
        rf = self._results_frame()
        return rf.evaluate("() => document.body ? document.body.innerText : ''")
