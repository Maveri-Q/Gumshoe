import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="c656515c-db89-40d0-9b27-0888af2b023c",
    name="Verify Main Menu Persistence on Canvas Click",
    tc_id="TC-136",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes", "broken": "yes", "seen": "The main menu is open with file and application options visible."},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='a005e080-4b52-4046-9cff-9641181c0b11'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button in the top left header', instruction_id='1657e998-9e6d-4217-a6e1-6a6cba2f5ef1'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open with items shown'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).getAttribute(\'role\') === \'menu\' && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0 ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the open main menu contains menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='The answer, exactly yes or no, to "the main menu is open and shows its items" is stored as {{ready}}.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas; away from the open left menu and bottom controls', instruction_id='01d4ab2f-ed85-48fb-819b-3884abf33cf2'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas; away from the open left menu and bottom controls', "click", 960, 918)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting 2000 ms after clicking the empty bottom-middle canvas', instruction_id='771d1b46-1cdc-4b13-a861-b5d3b0a0ea2d'):
        await page.wait_for_timeout(2000)
    
    async with testmu.step('Reading whether the main menu is open'):
        set_var('broken', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).getAttribute('role') === 'menu' && !!(el(19).offsetWidth || el(19).offsetHeight || el(19).getClientRects().length) ? 'yes' : 'no');\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='The answer, exactly yes or no, to "the main menu is still open" is stored as {{broken}}.'))
    
    async with testmu.step('Describing the current visible page state'):
        set_var('seen', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).querySelector(\'[role="menuitem"]\') ? \'The main menu is open with file and application options visible.\' : \'The Excalidraw whiteboard is visible.\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='a short sentence describing the visible page state', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='One short sentence describing what is seen is stored as {{seen}}.'))


if __name__ == "__main__":
    testmu.run(test)