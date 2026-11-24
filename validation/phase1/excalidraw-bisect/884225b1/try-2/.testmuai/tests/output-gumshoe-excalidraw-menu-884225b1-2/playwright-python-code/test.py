import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="c43d36cc-01a8-4470-8b8c-e5f2d75b04f6",
    name="Verify Main Menu Open State and Canvas Interaction",
    tc_id="TC-152",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='f93a59b0-c470-4a48-bd60-0f675c605415'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button in the top-left header', instruction_id='335231e9-dee2-408e-86d3-1abeb293de23'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(19).matches(\':not([hidden])\') && el(19).getAttribute(\'aria-hidden\') !== \'true\' && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open and displays menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether the main menu is open and shows its items is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; container=blank drawing canvas; away from the open left menu and bottom controls', instruction_id='22a47831-6831-4efe-b49c-e2cac21b0416'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; container=blank drawing canvas; away from the open left menu and bottom controls', "click", 960, 918)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting 2000 ms after clicking the canvas', instruction_id='5a84000d-4909-4d5b-94a4-cfadd1089469'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)