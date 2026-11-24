import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="e0683228-8fa3-41e1-b603-675ffde1377a",
    name="Verify Main Menu Open State and Canvas Interaction",
    tc_id="TC-147",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='ec217205-9f4e-4c74-bfa2-d480a8905b2e'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button in the top-left corner', instruction_id='535ca084-d143-49f2-8f56-f1a914de2607'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).querySelectorAll(\'[role="menuitem"]\').length > 0 && !!(el(19).offsetWidth || el(19).offsetHeight || el(19).getClientRects().length) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open and shows its menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether "the main menu is open and shows its items" is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas area', instruction_id='4b72b75d-6688-4609-a6bf-69f75eefad41'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas area', "click", 960, 918)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting 2000 ms after clicking the canvas area', instruction_id='341f1c59-a68e-4ba1-837e-20e99b32f7cb'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)