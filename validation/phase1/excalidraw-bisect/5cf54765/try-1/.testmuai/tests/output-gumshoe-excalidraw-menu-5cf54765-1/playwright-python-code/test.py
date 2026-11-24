import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="0c97d8fa-2066-4db7-95c7-674c98d38868",
    name="Verify Main Menu Open State and Interaction",
    tc_id="TC-145",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='25def86d-7002-4848-a9f5-88b54efcc5db'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button in the top-left corner', instruction_id='2faf9efe-2746-4be1-826b-c3322e561ef8'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open and shows items'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).querySelectorAll(\'[role="menuitem"]\').length > 0 ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the open main menu contains menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='The answer to “the main menu is open and shows its items” is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('PRIMARY: an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas', instruction_id='4eda0fac-02f9-4c8f-ab9f-8767a629ef42'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas', "click", 960, 810)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting 2000 ms after clicking the empty canvas', instruction_id='711c76ae-acd5-4930-b7de-261913f7a694'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)