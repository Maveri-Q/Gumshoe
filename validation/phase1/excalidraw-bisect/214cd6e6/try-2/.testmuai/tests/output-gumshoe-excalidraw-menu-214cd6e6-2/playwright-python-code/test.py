import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="bfe3cdce-a2ca-4c8d-8d64-9df39f9f30cd",
    name="Verify Main Menu Open State and Canvas Interaction",
    tc_id="TC-156",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='8717f79c-b170-4055-b682-917e6673f7b4'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button to open the menu', instruction_id='454559aa-0957-4371-8896-20367dcea16d'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).getAttribute(\'role\') === \'menu\' && el(19).getClientRects().length > 0 && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0 ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open and shows menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Store exactly yes or no as {{ready}} for whether the main menu is open and shows its items.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; container=blank white drawing canvas', instruction_id='7a7ef853-fe23-4e3c-a1a4-2bbe44a8d37a'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; container=blank white drawing canvas', "click", 960, 810)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting 2000 ms', instruction_id='04213510-c465-40e0-881e-74bab08db565'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)