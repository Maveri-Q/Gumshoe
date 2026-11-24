import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="b3dcb588-369e-4c1f-9f32-faaaa5029076",
    name="Verify Main Menu Persistence After Canvas Click",
    tc_id="TC-138",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes", "broken": "yes", "seen": "The Excalidraw main menu is open over a blank drawing canvas."},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='7cb19eb1-c395-456b-b6c1-cf4f01baa614'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button in the top-left header toolbar', instruction_id='3158f491-9f20-459f-b71b-738dc90e731c'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open with items visible in its menu'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).getAttribute(\'role\') === \'menu\' && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0 ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the open main menu contains menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether the main menu is open and shows its items is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas area', instruction_id='afd0b067-31a1-4778-b3c4-c8bf532ab9f2'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas area', "click", 960, 864)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting 2 seconds after clicking the empty canvas area', instruction_id='3bf33d8f-f392-441c-98a8-5d9cc8cb355a'):
        await page.wait_for_timeout(2000)
    
    async with testmu.step('Whether the main menu is still open is stored exactly as yes or no as {{broken}}.', instruction_id='c937d1a8-ced6-407f-a9b8-72fc979a9a7c'):
        set_var('broken', await testmu.vision_query(page, "Whether the main menu is still open is stored exactly as yes or no as {{broken}}.", ""))
    
    async with testmu.step('One short sentence describing what is visible on the screen is stored as {{seen}}.', instruction_id='ec9c330c-c307-4d25-b436-039492e214ff'):
        set_var('seen', await testmu.vision_query(page, "One short sentence describing what is visible on the screen is stored as {{seen}}.", ""))


if __name__ == "__main__":
    testmu.run(test)