import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="d282cc06-264b-41ca-96e4-284e893f63e4",
    name="Change Canvas Background Color Using Hex Code",
    tc_id="TC-168",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='c87ddd72-68fa-467e-a62b-18cf1a76e9fa'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button in the top-left corner', instruction_id='3f2cf3b8-72a2-496e-9e9d-d68016e571ab'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last color square on the right in the canvas background', instruction_id='206c243b-ef2d-4523-a3c8-8cb31067df76'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Checking whether the colour picker is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {116: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(116).innerText.includes(\'Hex code\') && !!el(116).querySelector(\'input, textarea, [role="textbox"]\')) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether an open colour picker dialog contains a Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='exactly yes or no is stored as {{ready}} for whether a colour picker with a Hex code text box is open right now'))
    
    async with testmu.step('Waiting for the next step to start', instruction_id='88ee11c0-c05d-4f37-8a32-6b860cd1e91b'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='a8e7b0af-41e0-4207-b6fd-e9f4d4b96dfb'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='f9df537a-7874-4977-b617-ed17d7687ce1'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting for 2 seconds', instruction_id='6db929ed-51c9-4508-bbee-22848196b9e9'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)