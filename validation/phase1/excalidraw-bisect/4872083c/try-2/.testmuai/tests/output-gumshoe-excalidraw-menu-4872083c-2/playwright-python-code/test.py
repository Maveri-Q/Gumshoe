import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="3e849b60-3eaf-4d42-807d-f1e6f086aeb5",
    name="Verify Main Menu Open State and Canvas Interaction",
    tc_id="TC-150",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes", "ready_2": "false"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='2227a0ee-2feb-4573-8022-e731ba2e2d35'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button', instruction_id='7b1e66e2-d9a6-4779-a1cb-633de44c5398'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open with items visible'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).getAttribute(\'role\') === \'menu\' && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0 ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the open main menu contains menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='whether "the main menu is open and shows its items" is stored exactly as yes or no as {{ready}}'))
    
    async with testmu.step('PRIMARY: empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-center; large blank canvas area', instruction_id='62b0a438-ed2b-48a8-9343-a8f52e780c1a'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-center; large blank canvas area', "click", 960, 918)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting for 2 seconds', instruction_id='686e6073-a568-48c4-8199-7e637279f2fb'):
        await page.wait_for_timeout(2000)
    
    async with testmu.step('Checking whether the main menu is open'):
        set_var('ready_2', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {18: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(18).getAttribute('aria-expanded') === 'true');\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:testid=[data-testid="main-menu-trigger"s]'], query='whether the main menu trigger is expanded to show its menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='whether the main menu is open and shows its items is saved as {{ready}}', reprobe=True))


if __name__ == "__main__":
    testmu.run(test)