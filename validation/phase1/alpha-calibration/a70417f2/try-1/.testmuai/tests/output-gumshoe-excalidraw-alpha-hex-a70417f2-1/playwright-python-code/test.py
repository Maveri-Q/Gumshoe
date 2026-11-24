import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="f6356149-6db7-42b5-b9bb-708d76fef21a",
    name="Change Canvas Background Color Using Hex Code",
    tc_id="TC-162",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "true"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='fc9f383c-6629-415e-89bb-a77ead780860'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button in the top-left corner', instruction_id='e64edd62-6353-4a9d-a0ad-0983ac142fa4'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last color square on the right in the canvas background palette', instruction_id='8121f03b-e1e2-4d45-b125-2e4927ffb80f'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Checking whether the colour picker is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {109: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (!!(el(109).querySelector(\'input[role="textbox"], input\') && /Hex code/i.test(el(109).innerText)));\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether the open colour picker dialog contains a Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='The answer exactly yes or no to whether "a colour picker with a Hex code text box is open" is stored as {{ready}}.'))
    
    async with testmu.step('Waiting for the queued plan steps to start', instruction_id='317c5830-f1c5-4b4c-9fe6-a744bb819589'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='af46e3c0-8ab3-46d3-b08b-732fd907e077'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='554f80a5-385a-4e19-98e1-b8642611c9e5'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting 2000 ms after pressing Tab', instruction_id='d8ca7eac-dcbf-4be2-9f05-97f6759ed0f7'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)