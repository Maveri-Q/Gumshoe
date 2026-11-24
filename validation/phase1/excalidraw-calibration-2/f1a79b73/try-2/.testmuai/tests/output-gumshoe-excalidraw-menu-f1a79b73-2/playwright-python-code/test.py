import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="ab70b24c-36e3-4ea3-8543-91e23111cdf4",
    name="Verify Main Menu Open State and Canvas Interaction",
    tc_id="TC-144",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "true"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='5e6d723c-1537-4c1f-abc6-3e2d4a16f017'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button in the top-left header', instruction_id='424a4084-39c0-4a6c-aaf1-51bd1e57a84b'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Checking whether the main menu is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).matches(\':not([hidden])\') && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0);\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open and contains menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether "the main menu is open and shows its items" is true right now is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; empty white canvas area', instruction_id='6ccce8f0-ff6f-4ca2-a7bc-56e9dbe2896e'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; empty white canvas area', "click", 960, 864)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting for 2000 milliseconds', instruction_id='0d9ea1a6-8e71-45f0-8952-9edea97bd53f'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)