import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="21d7f789-6619-4534-9697-60218db76fb0",
    name="Change Canvas Background Color Using Hex Code",
    tc_id="TC-164",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='01ea7bb5-5753-456e-80ac-1dce1f338a01'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button in the top-left corner', instruction_id='75aa9bd6-93f1-4af5-b264-e74bd003d096'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last colour square on the right in the Canvas background swatches', instruction_id='547ca633-fae9-414d-b556-dcc0a430c469'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Reading whether the colour picker with Hex code is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {115: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(115).querySelector(\'input[aria-label="Canvas background"]\') && el(115).querySelector(\'input[aria-label="Canvas background"]\').getClientRects().length > 0 && el(115).innerText.includes(\'Hex code\')) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether an open colour picker dialog contains the Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='whether "a colour picker with a Hex code text box is open" is true right now is stored as {{ready}} as exactly yes or no'))
    
    async with testmu.step('Waiting for the queued plan to start', instruction_id='edce7242-1296-4ab5-967d-36af3282255a'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='2f807972-3c2d-4275-bf5a-70eb07cbacd1'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='94ef9b75-c399-4116-8fd6-c6edbad253de'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting for 2 seconds', instruction_id='3da93238-623b-422f-8632-879a06b67be8'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)