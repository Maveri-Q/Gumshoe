import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="4247c132-4e6d-4c40-91dd-81419acc4200",
    name="Verify Main Menu Open State and Canvas Interaction",
    tc_id="TC-142",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "true"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='aaaf8fa8-6ca7-4c42-aff0-7acd98cac3b1'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button (three lines) at the top left', instruction_id='682ce907-8d85-49c1-a30d-6088dfd02ec3'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Checking whether the main menu is open and contains items'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(19).matches(\':not([hidden])\') && el(19).querySelectorAll(\'[role="menuitem"]\').length > 0);\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the open main menu contains menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether "the main menu is open and shows its items" is true right now is stored as {{ready}} exactly as yes or no.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas below the Excalidraw welcome content', instruction_id='2b0c570e-2f66-4364-b0d0-3b79c6e2e164'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; blank white canvas below the Excalidraw welcome content', "click", 960, 810)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting for 2000 milliseconds after clicking the empty canvas', instruction_id='c2d19614-3e16-4fac-b0cd-b25d363bd4f9'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)