import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="7b29cafd-7244-4492-9907-b8f8066f1ef9",
    name="Change Canvas Background Color Using Hex Code",
    tc_id="TC-179",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='e1d1a34c-4b68-4538-9641-dde84a1832a0'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button', instruction_id='1f844ddd-88b7-42cb-a925-450f8bedfe3e'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last canvas background color square on the right', instruction_id='6e248060-a780-4644-b263-b0745f2d1603'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Reading whether the color picker is open with a Hex code field'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {116: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(116).querySelector(\'input, [role="textbox"]\') && /Hex code/i.test(el(116).innerText)) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether the open color picker dialog contains a Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether a colour picker with a Hex code text box is open is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('Waiting for the canvas background text to appear', instruction_id='1c9503f2-938a-446b-8938-434fbcab2628'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='eb08ba82-bac2-4fca-8d32-cf1e31533fbe'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='6a4c4471-8cc1-42ac-98f1-91fcd230e001'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting 2 seconds after pressing Tab', instruction_id='737e00ea-f90a-4918-b53a-98610f17edb5'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)