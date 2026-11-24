import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="be287110-189e-41c1-bd55-646ced1e0d13",
    name="Change Canvas Background Color via Hex Code",
    tc_id="TC-165",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='5a6fb196-922c-4c83-a916-486ff9ca8947'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the three-line menu button in the top-left header', instruction_id='5d18bb96-2fe6-47cc-9e05-d1235451eedf'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last right color square under the Canvas background preview', instruction_id='5ad9ea27-8b35-4cf8-931a-e6e0b9555bba'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Reading whether the colour picker is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {115: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(115).innerText.includes('Hex code') && !!el(115).querySelector('input')) ? 'yes' : 'no');\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether an open colour picker dialog contains a Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether a colour picker with a Hex code text box is open is stored as {{ready}} exactly as yes or no.'))
    
    async with testmu.step('Waiting for the next step to be queued', instruction_id='6af75518-713f-4446-b2cb-e4fbc45605ad'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='b27a1c82-6213-4300-9d8e-0026a5c58d20'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='f03d6313-8272-4720-9ab0-a8447e97a78f'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting for 2 seconds', instruction_id='13f069c8-9b08-4ce7-9d90-0d935e20e14d'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)