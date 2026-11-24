import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="5dc5f94b-c84c-44e7-9569-ac660a6c3288",
    name="Change Canvas Background Color via Hex Code",
    tc_id="TC-178",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "true"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='474536c5-c2b0-4366-8ace-d40fe79e3ff0'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button in the top-left corner', instruction_id='bbb15db9-9793-4bc2-aec2-d201565edb6d'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last color square on the right after the divider', instruction_id='356e6e08-17b0-4789-9b2a-0ba6cc8eab02'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Checking whether the colour picker is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {116: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (!!(el(116).querySelector(\'input[aria-label="Canvas background"]\') && /Hex code/.test(el(116).innerText)));\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether a colour picker dialog with a Hex code text box is open', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='exactly yes or no is stored as {{ready}} for whether "a colour picker with a Hex code text box is open" is true right now.'))
    
    async with testmu.step('Typing ff000080 in the Hex code text box', instruction_id='28ab3b78-20da-4c22-a244-6c54f4b2f092'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Pressing Tab in the Hex code field', instruction_id='c6abf267-45f1-40ca-8ad2-72c18796d539'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting 2 seconds', instruction_id='d4ac9682-b86b-41ff-b986-6e940361e1b1'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)