import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="75184d6b-8444-4b32-b07b-7bdb320aa788",
    name="Verify Main Menu Open State and Canvas Interaction",
    tc_id="TC-148",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='fa6ce884-1537-4974-a068-70b5afd845a8'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button (three lines) to open the menu', instruction_id='61928bed-46a3-40f1-a9a2-9d59d53b9978'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).querySelectorAll(\'[role="menuitem"]\').length > 0 && !!(el(19).offsetWidth || el(19).offsetHeight || el(19).getClientRects().length) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open and displays its menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='whether "the main menu is open and shows its items" is true right now is stored as {{ready}} as exactly yes or no'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; container=blank canvas', instruction_id='a40f9291-22ef-4b51-b704-ead7466649dc'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; container=blank canvas', "click", 960, 810)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting 2000 ms after clicking the empty canvas area', instruction_id='6bbdc58e-a918-4e47-8237-0477681a2bd8'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)