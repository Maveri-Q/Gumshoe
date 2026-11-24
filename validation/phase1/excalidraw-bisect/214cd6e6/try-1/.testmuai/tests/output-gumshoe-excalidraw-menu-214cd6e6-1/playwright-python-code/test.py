import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="576a14b8-885a-408e-a5c1-adaab3aea6f1",
    name="Verify Menu Open State and Perform Canvas Click",
    tc_id="TC-155",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='b062a183-0e57-4e4e-8ed5-49fbe39e5fb3'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button in the top-left toolbar', instruction_id='f22f8ae6-8383-41d5-ab9d-c476d4b070d8'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(19).getAttribute(\'aria-hidden\') !== \'true\' && !!el(19).querySelector(\'[role="menuitem"]\')) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open and shows its items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='the value of whether "the main menu is open and shows its items" is true is stored exactly as yes or no as {{ready}}'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas below the welcome content', instruction_id='9e06cea0-27dd-4f6a-a960-f428ab2da7e1'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas below the welcome content', "click", 960, 810)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting for 2 seconds', instruction_id='d83da8a7-7dcb-4a9a-9045-afd4d3959cb4'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)