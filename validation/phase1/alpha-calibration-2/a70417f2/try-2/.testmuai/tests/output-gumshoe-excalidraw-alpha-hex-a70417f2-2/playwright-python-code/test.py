import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="fe5244d9-2efc-47d8-b0fa-7813b09c3a65",
    name="Change Canvas Background Color via Hex Code",
    tc_id="TC-167",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='acfe1dd8-aeeb-4f21-a3ed-717c621b3a37'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button', instruction_id='9c97d29f-b553-4afb-860c-ac0a6b6b90c6'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last canvas background colour square after the divider', instruction_id='9a98d30b-6773-4c4a-81eb-19a90bd6af50'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Reading whether the colour picker with Hex code input is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {109: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(109).querySelector(\'input, [role="textbox"]\') && /hex code/i.test(el(109).innerText)) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether the open colour picker dialog contains a Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether a colour picker with a Hex code text box is open is stored as {{ready}} exactly as yes or no.'))
    
    async with testmu.step('Waiting for the queued plan to execute', instruction_id='8211a711-aac0-44e7-9431-001a7cde3a0f'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='560aaa94-e64b-45fe-9997-fbae438aac9a'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='c131c00c-1c2b-4170-935d-a748f5b0487e'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting 2000 ms after pressing Tab', instruction_id='57a446c9-769b-4a0f-b03c-f6ea02dd5f79'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)