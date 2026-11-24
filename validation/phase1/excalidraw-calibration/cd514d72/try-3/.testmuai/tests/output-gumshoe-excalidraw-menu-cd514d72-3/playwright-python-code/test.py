import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="12ab627e-37eb-4e13-8e4e-42444be3fa4f",
    name="Verify Main Menu Persistence After Canvas Click",
    tc_id="TC-140",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "true", "broken": "yes", "seen": "The Excalidraw main menu is open over an empty whiteboard."},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='9a52e98a-1607-4f29-ba8c-f917b41970bd'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button to open the menu', instruction_id='05a294c7-5b96-436f-86db-f29676e859f8'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Checking whether the main menu is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).getAttribute(\'role\') === \'menu\' && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0 && !!(el(19).offsetWidth || el(19).offsetHeight || el(19).getClientRects().length));\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open and shows menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='The answer to whether "the main menu is open and shows its items" is true right now is stored as {{ready}} exactly as yes or no.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; container=blank Excalidraw canvas', instruction_id='86480abe-ab04-4bcb-985f-72fbad7adb19'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; container=blank Excalidraw canvas', "click", 960, 864)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting 2000 ms after clicking the empty canvas area', instruction_id='5c4cd637-8629-4f18-8bff-c76efb826ff7'):
        await page.wait_for_timeout(2000)
    
    async with testmu.step('The answer to whether "the main menu is still open" is true right now is stored as {{broken}} exactly as yes or no.', instruction_id='3c8e9bb5-ee44-4836-86dd-d017e583155b'):
        set_var('broken', await testmu.vision_query(page, "The answer to whether \"the main menu is still open\" is true right now is stored as {{broken}} exactly as yes or no.", ""))
    
    async with testmu.step('One short sentence describing what you see is stored as {{seen}}.', instruction_id='1671ee35-70ff-4520-beea-e4bf198f9dd9'):
        set_var('seen', await testmu.vision_query(page, "One short sentence describing what you see is stored as {{seen}}.", ""))


if __name__ == "__main__":
    testmu.run(test)