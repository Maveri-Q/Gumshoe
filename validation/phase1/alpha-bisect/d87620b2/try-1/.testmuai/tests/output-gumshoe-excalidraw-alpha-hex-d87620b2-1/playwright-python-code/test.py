import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="65a7ecf2-0461-4f4b-9587-e9f14ffa7403",
    name="Change Canvas Background Color Using Hex Code",
    tc_id="TC-172",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='6c48aace-5755-407a-9e11-82f25d76d818'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button with three lines in the top-left corner', instruction_id='67de11dc-5fd0-4290-914d-0ccf715eda4d'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last Canvas background color square on the right', instruction_id='77cfb448-47ce-4acf-a094-166853af0a88'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Reading whether the colour picker is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {116: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(116).offsetParent !== null && el(116).getAttribute('value') !== null) ? 'yes' : 'no');\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:role=textbox[name="Canvas background"i]'], query='whether the open canvas background colour picker includes a visible Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether a colour picker with a Hex code text box is open is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('Waiting for the plan to be queued', instruction_id='3b41f65e-62f1-4bc5-bfee-ed98fe7ad437'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='c7b44cba-6326-4228-af62-350e39e9f654'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='7888800e-9b65-477f-a5ff-6f963db81caf'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting for 2 seconds after typing ff000080 and pressing Tab', instruction_id='35b77f29-ea2d-47b2-a64c-87b16ba05204'):
        await page.wait_for_timeout(2000)
    
    async with testmu.step('Waiting 2 seconds', instruction_id='734a1bd2-c5b8-4c02-a5bd-4e305decba04'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)