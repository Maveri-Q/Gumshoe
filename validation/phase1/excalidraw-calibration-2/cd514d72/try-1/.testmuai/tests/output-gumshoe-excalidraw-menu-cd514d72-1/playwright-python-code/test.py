import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="d80850e6-56ac-4336-889b-35eef7f92c37",
    name="Verify Main Menu Open State and Canvas Interaction",
    tc_id="TC-141",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "true"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='0077c545-9219-445c-a609-669e730b7990'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button in the top-left header', instruction_id='ea2fc372-d090-4617-a89e-ee1f776c69f8'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Checking whether the main menu is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(19).getAttribute(\'role\') === \'menu\' && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0));\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open and contains menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='The answer exactly yes or no to whether the main menu is open and shows its items is stored as {{ready}}.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button; role=canvas | HINTS: position=bottom-middle; empty white canvas area', instruction_id='9ff4602e-5294-40e4-909a-0aa640152d25'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button; role=canvas | HINTS: position=bottom-middle; empty white canvas area', "click", 960, 810)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting 2000 ms after clicking the empty canvas area', instruction_id='a538f4db-6da2-4e88-88dc-b9d1d6a43aee'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)