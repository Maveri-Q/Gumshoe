import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="9305a1ee-d33f-44a5-b9ad-f8e92f08c35b",
    name="Verify Main Menu Open State and Canvas Interaction",
    tc_id="TC-149",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='3773726e-6ff5-4832-8611-6a8bef21d5dc'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button to open the menu', instruction_id='756475ee-dfb4-41f7-8e52-4ffa6c9c6ab0'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open and shows its items'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(19).getAttribute(\'aria-hidden\') !== \'true\' && !!(el(19).offsetWidth || el(19).offsetHeight || el(19).getClientRects().length) && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the open main menu contains visible menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether "the main menu is open and shows its items" is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas well above bottom controls and right-side Help button', instruction_id='b0f4f84a-3664-4cb8-99fa-beca08ea2608'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas well above bottom controls and right-side Help button', "click", 960, 864)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting 2 seconds', instruction_id='ba3c536b-05f3-4f0f-bacc-87972714373a'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)