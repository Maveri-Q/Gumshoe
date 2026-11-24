import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="7bf0a335-ce20-4f36-b3c7-ecb49ac05ccb",
    name="Change Canvas Background Color via Hex Code",
    tc_id="TC-180",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='55a47698-ccca-4d16-9581-3dd116a8e006'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button in the top-left header', instruction_id='6c0976ca-318a-4963-8305-7cfc126401ab'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last rightmost colour square after the divider', instruction_id='3e5fe0d2-bb65-4e99-b20a-445bc77aff3a'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Reading whether the colour picker is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {116: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(116).querySelector(\'input[aria-label="Canvas background"]\') && el(116).textContent.includes(\'Hex code\') ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether the open colour picker dialog contains a Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether a colour picker with a Hex code text box is open is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('Waiting for the plan steps to complete', instruction_id='7a6d3cec-ac66-4dd7-97a5-cd730b2dcf0d'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='42250114-da36-4d94-bb1d-9ec5c9c5e59e'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='a21e0454-d40a-4dd6-9b16-7cac2b3698d7'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting 2 seconds after pressing Tab', instruction_id='a25f046e-9866-40da-a73c-b86918102f39'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)