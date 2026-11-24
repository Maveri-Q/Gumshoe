import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="8f78b6f6-e351-466c-afd2-976a6a5e4d4e",
    name="Verify Main Menu Open State and Test Canvas Interaction",
    tc_id="TC-158",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4300/', instruction_id='966bdbae-5318-4a7f-9aa2-2a8603707952'):
        await page.goto("http://127.0.0.1:4300/")
    
    async with testmu.step('Clicking the main menu button in the top-left corner', instruction_id='c30661a2-304c-4116-8d5c-edeaa90bb0f7'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Reading whether the main menu is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {19: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((()=>{const m=el(19);const s=getComputedStyle(m);return s.display!=="none"&&s.visibility!=="hidden"&&m.getClientRects().length>0&&m.querySelectorAll(\'[role="menuitem"]\').length>0?"yes":"no"})());\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:testid=[data-testid="dropdown-menu"s]'], query='whether the main menu is open and contains menu items', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether "the main menu is open and shows its items" is true right now is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; empty white canvas area', instruction_id='4169b7e9-80c1-4615-a57c-a3950af5c4fa'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Click once on an empty part of the canvas, near the bottom middle of the page, away from the menu and from any button | HINTS: position=bottom-middle; empty white canvas area', "click", 960, 899)
        await page.mouse.click(coords['x'], coords['y'])
        
    
    async with testmu.step('Waiting 2000 ms after clicking the empty bottom-middle canvas area', instruction_id='3c38abea-e91f-42d6-8544-952f52c94ae0'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)