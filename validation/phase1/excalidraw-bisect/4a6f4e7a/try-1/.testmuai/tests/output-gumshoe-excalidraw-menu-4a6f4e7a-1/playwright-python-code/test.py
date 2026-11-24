import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="7d7e3bdb-2dfe-44c4-a735-5d015709184b",
    name="Verify Main Menu Open State and Canvas Interaction",
    tc_id="TC-153",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='502e0ee8-6ea9-4bac-9a5d-07bdb9332030'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button (three lines) in the top-left corner', instruction_id='658cca05-5213-4f59-805c-5278d5c32f2e'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open with its items'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(19).getAttribute(\'role\') === \'menu\' && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the open main menu contains menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether the main menu is open and shows its items is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; empty white canvas', instruction_id='0c5ee84a-3d97-4143-bc2a-b979ecdb8284'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; empty white canvas', "click", 960, 864)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting for 2 seconds', instruction_id='719649e6-6c9e-4472-b287-a79bb6c81159'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)