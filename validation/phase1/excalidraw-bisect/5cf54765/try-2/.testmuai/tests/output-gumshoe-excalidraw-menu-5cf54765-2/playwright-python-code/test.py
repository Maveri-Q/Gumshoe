import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="0eb642f3-9b57-46b2-a678-ab86f89274d2",
    name="Verify Main Menu Open State and Canvas Interaction",
    tc_id="TC-146",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes", "ready_2": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='5a925e79-8a2d-47bc-87be-e4ec3958c53e'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button in the top-left header', instruction_id='373f63e2-8e1b-495c-aaa4-fce37701c2c2'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(19).getBoundingClientRect().width > 0 && el(19).getBoundingClientRect().height > 0 && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open and shows menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='whether "the main menu is open and shows its items" is stored exactly as yes or no as {{ready}}'))
    
    async with testmu.step('Reading whether the main menu is open'):
        set_var('ready_2', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(19).getBoundingClientRect().width > 0 && el(19).getBoundingClientRect().height > 0 && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open and shows menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='whether the main menu is open and shows its items is saved as {{ready}}', reprobe=True))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle blank white canvas, above zoom controls and left of bottom-right help button', instruction_id='8f942f8e-a5f5-470f-9a00-7ba4a1b01ace'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle blank white canvas, above zoom controls and left of bottom-right help button', "click", 960, 810)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting for 2 seconds', instruction_id='71c47c12-4513-4dd2-b8a8-0bb0159d8b49'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)