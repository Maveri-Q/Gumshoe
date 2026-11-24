import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="fec12e27-54f9-4553-835b-d4d762ce1106",
    name="Verify Main Menu Persistence After Canvas Click",
    tc_id="TC-139",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes", "broken": "yes", "seen": "The Excalidraw main menu is open over a blank drawing canvas."},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='b45685fe-947d-4702-a8b2-15c44290e66c'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button in the top-left header', instruction_id='8d410863-e25a-4d1a-b19e-322d310765e4'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).getAttribute(\'role\') === \'menu\' && el(19).getAttribute(\'aria-hidden\') !== \'true\' && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0 ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open and contains menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='The answer to "the main menu is open and shows its items" is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white drawing canvas', instruction_id='0d2c153b-3bf7-4538-9044-322eafbe70ad'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white drawing canvas', "click", 960, 918)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting for 2000 ms after clicking the empty canvas', instruction_id='334df8a8-6ba0-473e-a154-9b2545da7ee8'):
        await page.wait_for_timeout(2000)
    
    async with testmu.step('The answer to "the main menu is still open" is stored exactly as yes or no as {{broken}}.', instruction_id='936162e3-85fc-49e0-8f55-bcca75de1bb8'):
        set_var('broken', await testmu.vision_query(page, "The answer to \"the main menu is still open\" is stored exactly as yes or no as {{broken}}.", ""))
    
    async with testmu.step('One short sentence describing what is visible is stored as {{seen}}.', instruction_id='5821b005-e668-45b6-83c7-2596a2d0f6a7'):
        set_var('seen', await testmu.vision_query(page, "One short sentence describing what is visible is stored as {{seen}}.", ""))


if __name__ == "__main__":
    testmu.run(test)