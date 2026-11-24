import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="3ef9ecd1-2769-4113-b447-43291acb0ca3",
    name="Verify Main Menu Persistence After Canvas Click",
    tc_id="TC-137",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "true", "broken": "yes", "seen": "The main menu is open, showing options such as Open and Save to."},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='365805d7-0e48-4e81-a871-494f3ec1e6b1'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button in the top-left header area', instruction_id='948e5287-8f93-451a-8d31-992a3e7a9548'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Checking whether the main menu is open and shows its items'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).getAttribute(\'role\') === \'menu\' && Array.from(el(19).querySelectorAll(\'[role="menuitem"]\')).length > 0);\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open and shows menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='The answer, exactly yes or no, to "the main menu is open and shows its items" is stored as {{ready}}.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle of the blank white drawing canvas, well right of the open menu and above bottom controls', instruction_id='80809c04-cd6b-4b7b-8ffa-ddbfb1bfffda'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle of the blank white drawing canvas, well right of the open menu and above bottom controls', "click", 1248, 918)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting for 2000 ms after clicking the empty canvas area', instruction_id='3816534c-e57f-492c-82be-9fcfbfa24282'):
        await page.wait_for_timeout(2000)
    
    async with testmu.step('Reading whether the main menu is open'):
        set_var('broken', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).getAttribute('role') === 'menu' && !!(el(19).offsetWidth || el(19).offsetHeight || el(19).getClientRects().length) ? 'yes' : 'no');\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open in the application interface', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='The answer, exactly yes or no, to "the main menu is still open" is stored as {{broken}}.'))
    
    async with testmu.step('Describing the visible interface'):
        set_var('seen', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).getAttribute('role') === 'menu' && !!(el(19).offsetWidth || el(19).offsetHeight || el(19).getClientRects().length) ? 'The main menu is open, showing options such as Open and Save to.' : 'The main menu is closed.');\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='a short sentence describing the visible application interface', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='One short sentence describing what is visible is stored as {{seen}}.'))


if __name__ == "__main__":
    testmu.run(test)