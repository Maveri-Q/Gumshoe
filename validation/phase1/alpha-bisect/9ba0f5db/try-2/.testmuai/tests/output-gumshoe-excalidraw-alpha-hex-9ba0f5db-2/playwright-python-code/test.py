import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="01c05f89-e61b-4e6f-901e-5e7388be6eb9",
    name="Set Canvas Background Color via Hex Code",
    tc_id="TC-169",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='fa5e44e7-3586-4e32-a3d4-093701b82e70'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button in the top-left corner', instruction_id='f8886db5-5526-4626-b67a-ae81c6b1850a'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last color square in the Canvas background row', instruction_id='b72d4886-1d34-4127-ab10-34ed90aae5d7'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Checking whether the colour picker is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {116: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(116).innerText.includes(\'Hex code\') && !!el(116).querySelector(\'input[role="textbox"], input, [role="textbox"]\')) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether an open colour picker dialog contains a Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether "a colour picker with a Hex code text box is open" is true right now is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('Waiting for the next queued step to start', instruction_id='4aad1c98-4a5c-48fc-9d78-4bdfc6e0700f'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='11ac802f-6060-4744-ba8e-e7e6ac218091'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='890870e7-1e75-4899-b0b4-8b96c2dcde90'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting for 2000 ms after tabbing out of the Hex code text box', instruction_id='e0a75cb9-de8f-48bf-964b-485f9eb20a0b'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)