import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="f7fed3f7-12b7-4d74-a59d-b409a9b1c9c4",
    name="Verify Main Menu Open State and Canvas Interaction",
    tc_id="TC-157",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='fde50082-4aea-44f3-a404-36a97a732645'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button in the top-left header', instruction_id='ba568a31-239b-4e9e-b908-9d0bbcdaa3a3'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading the main menu open state and items'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(19).getClientRects().length > 0 && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is visible and contains menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether "the main menu is open and shows its items" is true right now is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; container=blank canvas', instruction_id='26eb1357-dc1f-48dd-81d5-4e2116c62276'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; container=blank canvas', "click", 960, 810)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting for 2 seconds', instruction_id='b2d65224-305c-43ba-8598-a622cdd66dfe'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)